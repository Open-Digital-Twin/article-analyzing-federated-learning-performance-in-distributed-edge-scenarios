import re
import stats_service
import json

def define_color(container_name):
    if ('green' in container_name):
        return 'green'
    if ('red' in container_name):
        return 'red'
    return 'blue'

def get_total_experiment_count(dir):
    print(len(stats_service.list_experiments_files(dir)))

def save_server_averages_to_file(root_dir, to_dir):
    average = stats_service.create_average_stats_log_object(root_dir, True)
    with open(to_dir, "w") as file:
        file.write(json.dumps(average))

def save_client_averages_to_file(root_dir, to_dir):
    average = stats_service.create_average_stats_log_object(root_dir, False)
    with open(to_dir, "w") as file:
        file.write(json.dumps(average))

def container_stats_to_file(root_dir, to_dir):
    stats = stats_service.get_container_stats(root_dir)
    with open(to_dir, "w") as file:
        file.write(json.dumps(stats))

def get_all_experiments_ran_over_one_hour(dir):
    files = stats_service.list_experiments_files(dir)
    for file in files:
        with open(file) as json_file:
            data = json.load(json_file)
            if data[-1]['timestamps'] < 3600:
                print(file, data[-1]['timestamps'])

def get_all_number_of_rounds(dir):
    files = stats_service.list_experiments_files(dir)
    for file in files:
        count = 0
        with open(file) as json_file:
            data = json.load(json_file)
            current_accuracy = 0
            for data_point in data:
                if data_point and 'accuracy' in data_point and data_point['accuracy'] != current_accuracy:
                    count += 1
                    current_accuracy = data_point['accuracy']
            print(file, count)

def get_first_number_in_string(string):
    first_number = re.search('red(\d+)', string) or re.search('green(\d+)', string)
    if first_number:
        return first_number.group(1)
    return "10"

def get_number_of_epochs_from_container(string):
    first_number = re.search('Epoch(\d+)', string)
    if first_number:
        return first_number.group(1)
    return "1"

def get_marker(number):
    if number == "10":
        return "8"
    if number == "8" or number=="5":
        return ">"
    if number == "6" or number=="25":
        return "<"
    if number == "4" or number == "1":
        return "*"
    if number == "2":
        return "+"
    
def marker_if_exists(marker, marker_map):
    solution = False
    if marker in marker_map:
        solution = marker_map[marker]
        del marker_map[marker]
    marker_map[marker] = 1
    return solution

def get_label_for_epoch(marker):
    if marker == "8":
        return "10 client epochs and 20 server rounds"
    if marker == ">":
        return "5 client epochs and 35 server rounds"
    if marker == "<":
        return "25 client epochs and 10 server rounds"
    if marker == "*":
        return "1 client epoch and 100 server rounds"