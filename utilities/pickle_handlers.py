import pickle

def unpickle(file):
    with open(file, 'rb') as handle:
        dict = pickle.load(handle, encoding='bytes')
    return dict

def save_pickled(dict, filename):
    with open(filename, 'wb') as handle:
        pickle.dump(dict, handle, protocol=pickle.HIGHEST_PROTOCOL)