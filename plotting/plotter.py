import stats_service
import utilities
import matplotlib.pyplot as plot
import matplotlib.lines as mlines


def get_memory_and_cpu_plot(dir):
    memories = []
    cpus = []
    timestamps = []
    stats = stats_service.open_file(dir)
    for stat in stats:
        memories.append(stat['memories'])
        cpus.append(stat['cpus'])
        timestamps.append(stat['timestamps'])
    plot.title("Average CPU and memory usage for red data distribution clients with 25 epochs and 10 server rounds", fontsize="8")
    plot.xlabel("Total experiment time (s)")
    plot.ylabel("Resource usage (%)")
    plot.plot(timestamps, memories, label="Average memory usage per client")
    plot.plot(timestamps, cpus, label="Average CPU usage per client")
    plot.legend(fontsize="6.5")
    plot.show()

def get_maximum_accuracies_plot(dir):
    files = stats_service.list_experiments_files(dir)
    maximum_accuracies = []
    accuracies_array = []
    experiments_array = []
    for file in files:
        accuracy = stats_service.get_maximum_accuracy(file)
        maximum_accuracies.append({ 'accuracy': accuracy, 'experiment': file.split('_')[1] })
    maximum_accuracies = sorted(maximum_accuracies, key=lambda d: d['accuracy']) 
    for accuracy in maximum_accuracies:
        accuracies_array.append(accuracy['accuracy'])
        experiments_array.append(accuracy['experiment'])
    plot.rcParams.update({'font.size': 6})
    plot.barh(experiments_array, accuracies_array)
    plot.show()

def get_average_cpu_plot(dir):
    files = stats_service.list_experiments_files(dir)
    cpu_usages = []
    cpu_usages_array = []
    experiments_array = []
    for file in files:
        cpu_usage = stats_service.get_average_cpu_usage(file)
        cpu_usages.append({ 'cpu_usage': cpu_usage, 'experiment': file.split('_')[1] })
    cpu_usages = sorted(cpu_usages, key=lambda d: d['cpu_usage']) 
    for cpu_usage in cpu_usages:
        cpu_usages_array.append(cpu_usage['cpu_usage'])
        experiments_array.append(cpu_usage['experiment'])
    plot.rcParams.update({'font.size': 6})
    plot.barh(experiments_array, cpu_usages_array)
    plot.show()

def get_average_memory_plot(dir):
    files = stats_service.list_experiments_files(dir)
    memory_usages = []
    memory_usages_array = []
    experiments_array = []
    for file in files:
        memory_usage = stats_service.get_average_memory_usage(file)
        memory_usages.append({ 'memory_usage': memory_usage, 'experiment': file.split('_')[1] })
    memory_usages = sorted(memory_usages, key=lambda d: d['memory_usage']) 
    for memory_usage in memory_usages:
        memory_usages_array.append(memory_usage['memory_usage'])
        experiments_array.append(memory_usage['experiment'])
    plot.rcParams.update({'font.size': 6})
    plot.barh(experiments_array, memory_usages_array)
    plot.show()

## Has a 2% margin of error
def get_time_to_achieve_best_accuracy_plot(dir):
    files = stats_service.list_experiments_files(dir)
    accuracies_and_timestamps = []
    accuracies = []
    timestamps = []
    containers = []
    colors = []
    for file in files:
        accuracies_and_timestamps.append(stats_service.get_accuracy_and_timestamp(file))
    for accuracy_and_timestamp in accuracies_and_timestamps:
        container_name = accuracy_and_timestamp[2].split('_')[1]
        accuracies.append(accuracy_and_timestamp[0])
        timestamps.append(accuracy_and_timestamp[1])
        containers.append(container_name)
        colors.append(utilities.define_color(container_name))
    plot.scatter(accuracies, timestamps, c=colors)
    for i, txt in enumerate(containers):
        plot.rcParams.update({'font.size': 6})
        plot.annotate(txt, (accuracies[i], timestamps[i]), rotation=90)
    plot.show()

def get_packets_and_bytes_received_plot(dir):
    files = stats_service.list_experiments_files(dir)
    packets_and_bytes_received = []
    packets_received = []
    bytes_received = []
    containers = []
    colors = []
    for file in files:
        packets_and_bytes_received.append(stats_service.get_packets_and_bytes_received(file))
    for packet_and_byte in packets_and_bytes_received:
        container_name = packet_and_byte[2].split('_')[1]
        packets_received.append(packet_and_byte[0])
        bytes_received.append(packet_and_byte[1])
        containers.append(container_name)
        colors.append(utilities.define_color(container_name))
    for i in range(len(bytes_received)):
        marker = utilities.get_marker(utilities.get_number_of_epochs_from_container(containers[i]))
        plot.scatter(packets_received[i], bytes_received[i]/1000000, c=colors[i], marker=marker)
    for i, txt in enumerate(containers):
        plot.annotate(utilities.get_first_number_in_string(txt), (packets_received[i], bytes_received[i]/1000000), fontsize="7")
    plot.title("Average amount of bytes and packets received by the server applications")
    one = mlines.Line2D([], [], color='black', marker='*', ls='', label='1 client epoch and 100 server rounds')
    five = mlines.Line2D([], [], color='black', marker='>', ls='', label='5 client epochs and 35 server rounds')
    ten = mlines.Line2D([], [], color='black', marker='8', ls='', label='10 client epochs and 20 server rounds')
    twentyfive = mlines.Line2D([], [], color='black', marker='<', ls='', label='25 client epochs and 10 server rounds')
    txt = "^n"
    clients = mlines.Line2D([], [], color='black', marker=f'${txt}$', ls='', label='Number of clients in the experiment')
    plot.legend(handles=[one, five, ten, twentyfive, clients], fontsize="6")
    plot.xlabel("Packets received")
    plot.ylabel("Megabytes received")
    plot.savefig("plots/data-received.png", dpi=300)

def get_packets_and_bytes_transmitted_plot(dir):
    files = stats_service.list_experiments_files(dir)
    packets_and_bytes_transmitted = []
    packets_transmitted = []
    bytes_transmitted = []
    containers = []
    colors = []
    for file in files:
        packets_and_bytes_transmitted.append(stats_service.get_packets_and_bytes_transmitted(file))
    for packet_and_byte in packets_and_bytes_transmitted:
        container_name = packet_and_byte[2].split('_')[1]
        packets_transmitted.append(packet_and_byte[0])
        bytes_transmitted.append(packet_and_byte[1])
        containers.append(container_name)
        colors.append(utilities.define_color(container_name))
    marker_map = {}
    for i in range(len(bytes_transmitted)):
        marker = utilities.get_marker(utilities.get_number_of_epochs_from_container(containers[i]))
        if marker not in marker_map:
            marker_map[marker] = 1
            plot.scatter(packets_transmitted[i], bytes_transmitted[i]/1000000, c=colors[i], marker=marker, label=utilities.get_label_for_epoch(marker))
        else:
            plot.scatter(packets_transmitted[i], bytes_transmitted[i]/1000000, c=colors[i], marker=marker)
    for i, txt in enumerate(containers):
        plot.annotate(utilities.get_first_number_in_string(txt), (packets_transmitted[i], bytes_transmitted[i]/1000000), fontsize="8")
    plot.title("Bytes and packets transmitted by green servers with 6 clients")
    plot.xlabel("Total packets transmitted")
    plot.ylabel("Total megabytes transmitted")
    one = mlines.Line2D([], [], color='green', marker='*', ls='', label='1 client epoch and 100 server rounds')
    five = mlines.Line2D([], [], color='green', marker='>', ls='', label='5 client epochs and 35 server rounds')
    ten = mlines.Line2D([], [], color='green', marker='8', ls='', label='10 client epochs and 20 server rounds')
    twentyfive = mlines.Line2D([], [], color='green', marker='<', ls='', label='25 client epochs and 10 server rounds')
    txt = "^n"
    clients = mlines.Line2D([], [], color='black', marker=f'${txt}$', ls='', label='Number of clients in the experiment')
    # etc etc
    plot.legend(handles=[one, five, ten, twentyfive, clients], fontsize="7")
    plot.savefig("./plots/bytes-and-pkts-green-six.png", dpi=300)

def get_cpu_and_memory_plot(dir):
    files = stats_service.list_experiments_files(dir)
    cpus_and_memories = []
    cpu = []
    memory = []
    containers = []
    colors = []
    for file in files:
        cpus_and_memories.append(stats_service.get_cpu_and_memory(file))
    for cpu_and_memory in cpus_and_memories:
        container_name = cpu_and_memory[2].split('_')[1]
        cpu.append(cpu_and_memory[0])
        memory.append(cpu_and_memory[1])
        containers.append(container_name)
        colors.append(utilities.define_color(container_name))
    plot.scatter(cpu, memory, c=colors)
    for i, txt in enumerate(containers):
        plot.rcParams.update({'font.size': 6})
        plot.annotate(txt, (cpu[i], memory[i]), rotation=90)
    plot.show()

def get_memory_and_time_plot(dir):
    files = stats_service.list_experiments_files(dir)
    memories_and_times = []
    memory = []
    time = []
    containers = []
    colors = []
    for file in files:
        memories_and_times.append(stats_service.get_memory_and_time(file))
    for memory_and_time in memories_and_times:
        container_name = memory_and_time[2].split('_')[1]
        memory.append(memory_and_time[0])
        time.append(memory_and_time[1])
        containers.append(container_name)
        colors.append(utilities.define_color(container_name))
    for i in range(len(memory)):
        marker = utilities.get_marker(utilities.get_number_of_epochs_from_container(containers[i]))
        plot.scatter(time[i], memory[i], c=colors[i], marker=marker)
    for i, txt in enumerate(containers):
        plot.annotate(utilities.get_first_number_in_string(txt), (time[i], memory[i]), fontsize="7")
    one = mlines.Line2D([], [], color='black', marker='*', ls='', label='1 client epoch and 100 server rounds')
    five = mlines.Line2D([], [], color='black', marker='>', ls='', label='5 client epochs and 35 server rounds')
    ten = mlines.Line2D([], [], color='black', marker='8', ls='', label='10 client epochs and 20 server rounds')
    twentyfive = mlines.Line2D([], [], color='black', marker='<', ls='', label='25 client epochs and 10 server rounds')
    txt = "^n"
    clients = mlines.Line2D([], [], color='black', marker=f'${txt}$', ls='', label='Number of clients in the experiment')
    # etc etc
    plot.legend(handles=[one, five, ten, twentyfive, clients], fontsize="7")
    plot.title("Average memory usage per client through time")
    plot.xlabel("Total experiment time (s)")
    plot.ylabel("Average memory usage per client in the experiment(%)")
    plot.savefig("mem-time.png", dpi=300)

def get_cpu_and_time_plot(dir):
    files = stats_service.list_experiments_files(dir)
    cpus_and_times = []
    cpu = []
    time = []
    containers = []
    colors = []
    for file in files:
        cpus_and_times.append(stats_service.get_cpu_and_time(file))
    for cpu_and_time in cpus_and_times:
        container_name = cpu_and_time[2].split('_')[1]
        cpu.append(cpu_and_time[0])
        time.append(cpu_and_time[1])
        containers.append(container_name)
        colors.append(utilities.define_color(container_name))
    for i in range(len(cpu)):
        marker = utilities.get_marker(utilities.get_number_of_epochs_from_container(containers[i]))
        plot.scatter(time[i], cpu[i], c=colors[i])
    for i, txt in enumerate(containers):
        plot.annotate(utilities.get_first_number_in_string(txt), (time[i], cpu[i]), fontsize="7")
    one = mlines.Line2D([], [], color='black', marker='*', ls='', label='1 client epoch and 100 server rounds')
    five = mlines.Line2D([], [], color='black', marker='>', ls='', label='5 client epochs and 35 server rounds')
    ten = mlines.Line2D([], [], color='black', marker='8', ls='', label='10 client epochs and 20 server rounds')
    twentyfive = mlines.Line2D([], [], color='black', marker='<', ls='', label='25 client epochs and 10 server rounds')
    txt = "^n"
    clients = mlines.Line2D([], [], color='black', marker=f'${txt}$', ls='', label='Number of clients in the experiment')
    plot.legend(handles=[clients], fontsize="7")
    plot.title("Average CPU usage per client through time by clients with 1 epoch and 100 server rounds", fontsize="8")
    plot.xlabel("Total experiment time (s)")
    plot.ylabel("Average CPU usage per client in the experiment(%)")
    plot.savefig("cpu-time.png", dpi=300)

def get_two_accuracy_lines_plot(dir1, dir2):
    accuracy1 = []
    timestamp1 = []
    dir1Stats = stats_service.create_average_stats_log_object_from_averages(dir1)
    break_point = 0
    for i in range(len(dir1Stats)):
        accuracy1.append(dir1Stats[i]['accuracy'])
        timestamp1.append(dir1Stats[i]['timestamps'])
        if (dir1Stats[i]['timestamps'] > 5000):
            break_point = i
            break
    accuracy2 = []
    timestamp2 = []
    dir2Stats = stats_service.create_average_stats_log_object_from_averages(dir2)
    for stat in dir2Stats:
        accuracy2.append(stat['accuracy'])
        timestamp2.append(stat['timestamps'])
    plot.plot(timestamp1[:break_point], accuracy1[:break_point], c="green", label="Green experiments")
    plot.plot(timestamp2[:break_point], accuracy2[:break_point], c="red", label="Red experiments")
    plot.title("Average accuracy with 10 clients through time")
    plot.xlabel("Total experiment time (s)")
    plot.ylabel("Accuracy")
    plot.show()
    plot.savefig("acc-with-ten.png", dpi=300)

def get_accuracy_lines_for_epochs_plot(dir1, dir2, dir3, dir4):
    accuracy1 = []
    timestamp1 = []
    dir1Stats = stats_service.create_average_stats_log_object_from_averages(dir1)
    for i in range(len(dir1Stats)):
        accuracy1.append(dir1Stats[i]['accuracy'])
        timestamp1.append(dir1Stats[i]['timestamps'])
    accuracy2 = []
    timestamp2 = []
    dir2Stats = stats_service.create_average_stats_log_object_from_averages(dir2)
    for stat in dir2Stats:
        accuracy2.append(stat['accuracy'])
        timestamp2.append(stat['timestamps'])
    accuracy3 = []
    timestamp3 = []
    dir3Stats = stats_service.create_average_stats_log_object_from_averages(dir3)
    for stat in dir3Stats:
        accuracy3.append(stat['accuracy'])
        timestamp3.append(stat['timestamps'])
    accuracy4 = []
    timestamp4 = []
    dir4Stats = stats_service.create_average_stats_log_object_from_averages(dir4)
    for stat in dir4Stats:
        accuracy4.append(stat['accuracy'])
        timestamp4.append(stat['timestamps'])

    plot.plot(timestamp1, accuracy1, label="1 client epoch and 100 server rounds")
    plot.plot(timestamp2, accuracy2, label="5 client epochs and 35 server rounds")
    plot.plot(timestamp3, accuracy3, label="10 client epochs and 20 server rounds")
    plot.plot(timestamp4, accuracy4, label="25 client epochs and 10 server rounds")
    plot.title("Average accuracy for experiments with clients through time for each epoch layout", fontsize="8")
    plot.xlabel("Total experiment time (s)")
    plot.ylabel("Accuracy")
    plot.legend(fontsize="8")
    plot.savefig("acc-by-epoch.png", dpi=300)


# get_maximum_accuracies_plot("./averages/server")
# get_time_to_achieve_best_accuracy_plot("./averages/server")
# utilities.save_server_averages_to_file("../../../../reports/red", "./average_red_server")
# get_cpu_and_memory_plot("./averages/clients")
# utilities.container_stats_to_file("../../../../reports/redEpoch25/red-client-3/2022-04-12T16:23:18.724Z-ffremde01", "a_redEpoch25_client")
# get_two_accuracy_lines_plot("./averages/ten-divided-by-color/green/", "./averages/ten-divided-by-color/red/") # good
# get_two_accuracy_lines_plot("./averages/four-divided-by-color/green/", "./averages/four-divided-by-color/red/") # good
# get_accuracy_lines_for_epochs_plot("./averages/divided-by-epoch/1", "./averages/divided-by-epoch/5", "./averages/divided-by-epoch/10", "./averages/divided-by-epoch/25") # good

get_packets_and_bytes_received_plot("./averages/full/server") # good

# get_packets_and_bytes_transmitted_plot("./averages/full/server") # good
# get_packets_and_bytes_transmitted_plot("./averages/six-green-servers/") # good
# get_packets_and_bytes_transmitted_plot("./averages/redsEpoch1/servers") # good

# get_memory_and_cpu_plot("./averages/full/clients/epoch25/red/average_redEpoch25_client")
# get_cpu_and_time_plot("./averages/full/clients/epoch1") # good
# get_memory_and_time_plot("./averages/full/clients") # good