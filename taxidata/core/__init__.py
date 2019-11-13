from .object import *

def taxis(x):
    x = np.array(x)
    return x.view(taxiarray)
    
def load(file):
    '''From hdf5 file, load dataset'''
    pass
