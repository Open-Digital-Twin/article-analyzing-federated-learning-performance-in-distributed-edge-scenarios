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