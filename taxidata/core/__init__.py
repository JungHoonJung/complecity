from .object import *

def taxis(x):
    x = np.array(x)
    return x.view(taxiarray)
