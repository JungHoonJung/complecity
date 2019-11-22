from .object import *
import numpy as np

def array(*arg, **kwarg):
    x = np.array(*arg, **kwarg)
    return x.view(taxiarray)

def load(file):
    '''From hdf5 file, load dataset'''
    pass
