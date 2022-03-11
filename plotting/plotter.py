from stats_service import get_arrays_for_stats, get_average_stats
import matplotlib.pyplot as plot

images = ['client1', 'client2', 'server']

for image in images:
    all_stats = get_arrays_for_stats('green', image)
    average_memories_stats = get_average_stats(all_stats['memories'])
    average_cpus_stats = get_average_stats(all_stats['cpus'])
    average_bytes_received = get_average_stats(all_stats['bytes_received'])
    average_bytes_transmitted = get_average_stats(all_stats['bytes_transmitted'])
    average_timestamps = get_average_stats(all_stats['timestamps'])
    average_packets_received = get_average_stats(all_stats['packets_received'])
    average_packets_transmitted = get_average_stats(all_stats['packets_transmitted'])
    plot.plot([0] + average_timestamps, [0] + average_cpus_stats)
    plot.title(image)
    plot.xlabel('Time (s)')
    plot.ylabel('Packets Transmitted')
    plot.show()