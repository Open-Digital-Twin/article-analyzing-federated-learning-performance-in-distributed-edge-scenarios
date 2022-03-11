import json
import os
import datetime as DT
from dateutil import parser

def open_file(file_path):
    with open(file_path) as json_file:
        data = json.load(json_file)
        return data

def get_memory_percentage(container_stat):
    used_memory = container_stat['memory_stats']['usage'] - container_stat['memory_stats']['stats']['cache']
    available_memory = container_stat['memory_stats']['limit']
    return (used_memory / available_memory) * 100.0

def get_cpu_percentage(container_stat):
    cpu_delta = container_stat['cpu_stats']['cpu_usage']['total_usage'] - container_stat['precpu_stats']['cpu_usage']['total_usage']
    system_cpu_delta = container_stat['cpu_stats']['system_cpu_usage'] - container_stat['precpu_stats']['system_cpu_usage']
    number_cpus = container_stat['cpu_stats']['online_cpus']
    return (cpu_delta / system_cpu_delta) * number_cpus * 100.0

def get_time_from_start(container_stat, starting_timestamp):
    to = parser.parse(container_stat['read'])
    starting = parser.parse(starting_timestamp)
    time_delta = to - starting
    return time_delta.total_seconds()

def get_average(list):
    return sum(list)/len(list)

# For a given container of a given experiment, returns an object
# with arrays for relevant stats for each tick for every
# container that ran with that image in that experiment
def get_arrays_for_stats(experiment_name, image_name):
    all_stats = { 'memories': [], 'cpus': [], 'timestamps': [], 'bytes_received': [], 'bytes_transmitted': [] }
    dir = f'../../../../{experiment_name}/{image_name}'
    for file in os.listdir(dir):
        image_memory = []
        image_cpu = []
        image_timestamp = []
        image_bytes_received = []
        image_bytes_transmitted = []
        data = open_file(f'{dir}/{file}')
        starting_timestamp = data[0]['read']
        data.pop() # Removing last element as it usually contains erroneous stats
        for container_stat in data:
            image_memory.append(get_memory_percentage(container_stat))
            image_cpu.append(get_cpu_percentage(container_stat))
            image_timestamp.append(get_time_from_start(container_stat, starting_timestamp))
            image_bytes_received.append(container_stat['networks']['eth0']['rx_bytes'])
            image_bytes_transmitted.append(container_stat['networks']['eth0']['tx_bytes'])
        all_stats['memories'].append(image_memory)
        all_stats['cpus'].append(image_cpu)
        all_stats['timestamps'].append(image_timestamp)
        all_stats['bytes_received'].append(image_bytes_received)
        all_stats['bytes_transmitted'].append(image_bytes_transmitted)
    return all_stats

# Receives an array containing arrays of stats ticks
# And returns an array with the average for each tick
# Example: [[1,2,3], [5,0,7]] -> [3,1,5]
def get_average_stats(all_stats):
    max_len = 0
    for stats in all_stats:
        current_len = len(stats)
        max_len = max(max_len, current_len)
    
    stats_per_tick = []

    for i in range(max_len):
        stats_per_tick.append([])

    for stats in all_stats:
        for i in range(len(stats)):
            stats_per_tick[i].append(stats[i])

    average_stats = []

    for tick in stats_per_tick:
        average_stats.append(get_average(tick))

    return average_stats