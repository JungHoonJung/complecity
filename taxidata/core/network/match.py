import networkx as nx
import numpy as np
from ..object import taxiarray, trajectory, Dataset
from .ksegment import *

class MapMatchingBase:
    '''class for map matching algorithm, we target the multi-track map matching.
    we will heritage this class to mapmatching
    '''
    def __init__(self, trajectory_list, map):
        pass

    def matching(self, arg):
        pass

    def segment_generating(self, seg_func = None):
        pass

    def 
