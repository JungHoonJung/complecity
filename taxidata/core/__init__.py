from .object import *
from .network.functions import toUTM
from .network.ksegment  import *
from .network.match import *

import numpy as np

def array(*arg, **kwarg):
    x = np.array(*arg, **kwarg)
    x = x.view(taxiarray)
    x.pos = ([],[])
    x.taxi_id = []
    return x

def load(file):
    '''From hdf5 file, load dataset'''
    pass
