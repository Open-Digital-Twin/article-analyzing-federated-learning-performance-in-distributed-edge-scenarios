from email.mime import image
import json
import os
import datetime as DT
from dateutil import parser
import pandas as pd
from collections import Counter

def open_file(file_path):
    with open(file_path) as json_file:
        data = json.load(json_file)
        return data

def get_memory_percentage(container_stat):
    if container_stat and 'memory_stats' in container_stat:
        used_memory = container_stat['memory_stats']['usage'] - container_stat['memory_stats']['stats']['cache']
        available_memory = container_stat['memory_stats']['limit']
        return (used_memory / available_memory) * 100.0

def get_cpu_percentage(container_stat):
    if container_stat and 'cpu_stats' in container_stat:
        cpu_delta = container_stat['cpu_stats']['cpu_usage']['total_usage'] - container_stat['precpu_stats']['cpu_usage']['total_usage']
        system_cpu_delta = container_stat['cpu_stats']['system_cpu_usage'] - container_stat['precpu_stats']['system_cpu_usage']
        number_cpus = container_stat['cpu_stats']['online_cpus']
        return (cpu_delta / system_cpu_delta) * number_cpus * 100.0

def get_time_from_start(container_stat, starting_timestamp):
    if container_stat and 'read' in container_stat:
        to = parser.parse(container_stat['read'])
        starting = parser.parse(starting_timestamp)
        time_delta = to - starting
        return time_delta.total_seconds()

def get_average(list):
    return sum(list)/len(list)

# For a given container, returns an object
# with arrays for relevant stats
def get_container_stats(file_path):
    if (not os.path.exists(file_path)):
        return
    image_stats = []
    data = open_file(file_path)
    starting_timestamp = data[0]['read']
    data.pop() # Removing last element as it usually contains erroneous stats
    for container_stat in data:
        if container_stat:
            image_stats.append({
                'memories': get_memory_percentage(container_stat),
                'cpus': get_cpu_percentage(container_stat),
                'timestamps': get_time_from_start(container_stat, starting_timestamp),
                'bytes_received': container_stat['networks']['eth0']['rx_bytes'],
                # 'accuracy': float(container_stat['accuracy']),
                'bytes_transmitted': container_stat['networks']['eth0']['tx_bytes'],
                'packets_received': container_stat['networks']['eth0']['rx_packets'],
                'packets_transmitted': container_stat['networks']['eth0']['tx_packets']
            })
    return image_stats

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

def list_experiments_files(root_dir):
    r = []
    for root, dirs, files in os.walk(root_dir):
        for name in files:
            r.append(os.path.join(root, name))
    return r

# Receives directory containing folders with logs and returns an
# array with an average of every stats file.
# The main usage is to average every client from an experiment
def create_average_stats_log_object(root_dir, for_server):
    file_paths = []
    all_stats_objects = []
    averaged_stats_objects = []
    for root, dirs, files in os.walk(root_dir):
        if (root.endswith("server") == for_server):
            for name in files:
                file_paths.append(os.path.join(root, name))

    for file in file_paths:
        stats_objects = get_container_stats(file)
        all_stats_objects.append(stats_objects)

    # find maximum length to make sure we iterate through all indexes
    maximum_length = 0
    for stats_array in all_stats_objects:
        maximum_length = max(maximum_length, len(stats_array))
    
    i = 0
    while i < maximum_length:
        local_object_array = []
        for stats_array in all_stats_objects:
            if (i < len(stats_array)):
                local_object_array.append(stats_array[i])
        df = pd.DataFrame(local_object_array)
        averaged_stats_objects.append(dict(df.mean()))
        i += 1
    
    return averaged_stats_objects

# Receives directory containing folders with logs already averaged 
# and returns an array with an average of every stats file.
def create_average_stats_log_object_from_averages(root_dir):
    file_paths = []
    all_stats_objects = []
    averaged_stats_objects = []
    for root, dirs, files in os.walk(root_dir):
        for name in files:
            file_paths.append(os.path.join(root, name))

    for file in file_paths:
        stats_objects = open_file(file)
        all_stats_objects.append(stats_objects)

    # find maximum length to make sure we iterate through all indexes
    maximum_length = 0
    for stats_array in all_stats_objects:
        maximum_length = max(maximum_length, len(stats_array))
    
    i = 0
    while i < maximum_length:
        local_object_array = []
        for stats_array in all_stats_objects:
            if (i < len(stats_array)):
                local_object_array.append(stats_array[i])
        df = pd.DataFrame(local_object_array)
        averaged_stats_objects.append(dict(df.mean()))
        i += 1
    
    return averaged_stats_objects
def get_maximum_accuracy(file):
    maximum_accuracy = 0
    data = open_file(file)
    for data_point in data:
        maximum_accuracy = max(maximum_accuracy, data_point['accuracy'])
    return maximum_accuracy

def get_transmitted_bytes(file):
    data = open_file(file)
    print(data[-1])
    return data[-1]['bytes_transmitted']

def get_average_cpu_usage(file):
    cpu_usage_sum = 0
    data = open_file(file)
    for data_point in data:
        cpu_usage_sum += data_point['cpus']
    return cpu_usage_sum/len(data)

def get_average_memory_usage(file):
    memory_usage_sum = 0
    data = open_file(file)
    for data_point in data:
        memory_usage_sum += data_point['memories']
    return memory_usage_sum/len(data)

def get_accuracy_and_timestamp(file):
    max_accuracy = get_maximum_accuracy(file)
    data = open_file(file)
    for data_point in data:
        if data_point['accuracy'] >= max_accuracy*0.98:
            return [data_point['accuracy'], data_point['timestamps'], file]

def get_packets_and_bytes_received(file):
    data = open_file(file)
    return [data[-1]['packets_received'], data[-1]['bytes_received'], file]
        
def get_packets_and_bytes_transmitted(file):
    data = open_file(file)
    return [data[-1]['packets_transmitted'], data[-1]['bytes_transmitted'], file]

def get_cpu_and_memory(file):
    return [get_average_cpu_usage(file), get_average_memory_usage(file), file]

def get_cpu_and_time(file):
    data = open_file(file)
    return [get_average_cpu_usage(file), data[-1]['timestamps'], file]

def get_memory_and_time(file):
    data = open_file(file)
    return [get_average_memory_usage(file), data[-1]['timestamps'], file]