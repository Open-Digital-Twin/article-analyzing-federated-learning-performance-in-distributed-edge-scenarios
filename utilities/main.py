import pickle_handlers

# This was used to separate the 5 data batches from
# the original cifar-10 into 500 separate batches.
# To achieve this, download the batches, then place them
# in a folder called cifar-10-batches inside utilities.

dict1 = pickle_handlers.unpickle("./cifar-10-batches/data_batch_1")
dict2 = pickle_handlers.unpickle("./cifar-10-batches/data_batch_2")
dict3 = pickle_handlers.unpickle("./cifar-10-batches/data_batch_3")
dict4 = pickle_handlers.unpickle("./cifar-10-batches/data_batch_4")
dict5 = pickle_handlers.unpickle("./cifar-10-batches/data_batch_5")

full_data = [*dict1[b'data'], *dict2[b'data'], *dict3[b'data'], *dict4[b'data'], *dict5[b'data']]
full_labels = [*dict1[b'labels'], *dict2[b'labels'], *dict3[b'labels'], *dict4[b'labels'], *dict5[b'labels']]
full_filenames = [*dict1[b'filenames'], *dict2[b'filenames'], *dict3[b'filenames'], *dict4[b'filenames'], *dict5[b'filenames']]

for i in range(500):
    dump_filename = "data_batch_" + str(i+1)
    index_start = i*100
    index_end = index_start + 100
    new_dict = {
        'batch_label': "b'training batch " + str(i+1) + " of 500",
        'labels': full_labels[index_start:index_end],
        'data': full_data[index_start:index_end],
        'filenames': full_filenames[index_start:index_end]
    }
    pickle_handlers.save_pickled(new_dict, dump_filename)