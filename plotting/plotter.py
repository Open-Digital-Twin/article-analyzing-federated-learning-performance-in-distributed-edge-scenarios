import stats_service
import utilities
import matplotlib.pyplot as plot

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
    plot.scatter(packets_received, bytes_received, c=colors)
    for i, txt in enumerate(containers):
        plot.rcParams.update({'font.size': 6})
        plot.annotate(txt, (packets_received[i], bytes_received[i]), rotation=90)
    plot.show()

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
    plot.scatter(packets_transmitted, bytes_transmitted, c=colors)
    for i, txt in enumerate(containers):
        plot.rcParams.update({'font.size': 6})
        plot.annotate(txt, (packets_transmitted[i], bytes_transmitted[i]), rotation=90)
    plot.show()

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

# get_maximum_accuracies_plot("./averages/server/")
# get_transmitted_bytes_plot("./averages/clients/")
# get_average_cpu_plot("./averages/clients")
# get_time_to_achieve_best_accuracy_plot("./averages/server")
# get_packets_and_bytes_received_plot("./averages/server")
# get_packets_and_bytes_transmitted_plot("./averages/clients")
get_cpu_and_memory_plot("./averages/clients")