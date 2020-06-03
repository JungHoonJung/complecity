import networkx as nx
import numpy as np
from ..object import taxiarray, trajectory, Dataset
from .ksegment import *


class SingleTrackMapMatching:
    """object for single-track map matching."""
    _default_segment_func = k_segments_strict_bfs_with_length

    def __init__(self, trajectory, road_network):
        #heritage
        self.map = road_network

        #argument
        self.target = trajectory

        #segment generation
        self.segment_set        =   []          # list of segments
        self.node_segments      =   {}          # node to segment dictionay
        self.segments_index     =   0

        #dynamic programming (save results of each calculation to reuse)
        self.distance_map       =   {}          # this will be double dictionay (i.e. distance_map[node][(index_of_seg)])
        self.stitching_map      =   {}          # this will be double dictionay (i.e. stitching_map[(index_of_seg1)][(index_of_seg2)])

    def generate_ksegment(self, seg_func = None, k = 800):
        """Segment generating function. return dictionary of segments by node.

        Parameters
        ----------
        seg_func : `func`
            segment generation function. function must be defined as the form of `function(Graph, node, k)`
        k : `int` or `float`
            a length threshold of ksegment. default is 800(m).

        Returns
        -------
        `dict`
             a dictionary of node to segment whose key is the start node. return will be saved on `self.segments`

        ########## Please add a description of ksegment here. ##########

        #################################################################

        Each segment will have the identical index for comfortable calculation.
        we will save the cost of each matching cost based on the index of segments.
        """
        if seg_func is None:
            gen = SingleTrackMapMatching._default_segment_func
        else: gen = seg_func

        raise NotImplemtedError

    def find_candidate_set(self, d_max = 200):
        """Find a candidate segment set with stored ksegments through calculating the distance of curve.

        Parameters
        ----------
        trajectory : `taxidata.trajectory`
             a sequence of converted GPS data(UTM coordinate). It must have `pos` attribute.
        d_max : `int` or `float`
            a threshold of maximum distance between positions of trajectory and segments. the default value is 200 (m).

        Returns
        -------
        `list`
            a list with same cardinality of trajectory. Each component of list is a list of candidate segments(or index (not fixed.)).

        Please add a description of variable parametrization here.

        + each calculation must be saved on `self.distance_map`.
        """
        raise NotImplemtedError

    def matching(self):
        pass


class MultitrackMapMatching(SingleTrackMapMatching):
    """object for multi-track mapmatching."""

    def __init__(self, trajectory_list, road_network):
        super(MultitrackMapMatching, self).__init__(trajectory_list,road_network)


    def matching(self):
        pass
