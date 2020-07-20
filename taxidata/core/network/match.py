import networkx as nx
import numpy as np
from ..object import taxiarray, trajectory, Dataset
from .ksegment import *
from tqdm import tqdm

class PathContainer:
    """class for mapmatching. It save the path and its cost."""

    def __init__(self, segment_id, cost):
        self.segments = [segment_id]
        self.cost   = cost
        self.index  = 1

    def __lt__(self, other):
        '''sorting'''
        return self.cost<other.cost

    def __gt__(self, other):
        '''sorting'''
        return self.cost>other.cost

    def __le__(self, other):
        '''sorting'''
        return self.cost<=other.cost

    def __ge__(self, other):
        '''sorting'''
        return self.cost>=other.cost

    def __del__(self):
        del self.cost, self.index

    def optimize(self, path, delta_cost):
        assert delta_cost<0, "optimize must reduce cost."
        self.segments[:path.index] = path.segments
        self.cost += delta_cost

    def copy(self):
        temp = self.__class__(0, self.cost)
        temp.segments = self.segments.copy()
        temp.index = self.index
        return temp

    def update(self, segment, cost):
        self.segments.append(segment.id)
        self.cost += cost
        self.index += 1




class SingleTrackMapMatching:
    """object for single-track map matching."""
    _default_segment_func = k_segments_strict_bfs_with_length

    def __init__(self, trajectory, road_network):
        #argument
        self.map = road_network
        self.target = trajectory

        #segment generation
        self.segment_set        =   []          # list of segments
        self.node_segments      =   {}          # node to segment dictionay
        self.segments_index     =   0
        self.candidate          =   []

        #dynamic programming (save results of each calculation to reuse)
        self.distance_map       =   []          # this will be double dictionay (i.e. distance_map[index][(index_of_seg)])
        self.stitching_map      =   {}          # this will be double dictionay (i.e. stitching_map[(index_of_seg1)][(index_of_seg2)])

        #mathcing algorithm will be implemented as bfs manner.
        self.length             =   len(self.trajectory)

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
        ***Every generated segment must be in a `self.stitching_map` as a key with an empty dictionary as a value.
        """
        if seg_func is None:
            gen = SingleTrackMapMatching._default_segment_func
        else: gen = seg_func

        for node in self.map.nodes:
            self.node_segments[node] = gen(self.map, node, k)
            for i in self.node_segments[node]:
                self.segment_set.append(i)
                self.node_segments[temp.segments_index]=i

                i.id = self.segments_index
                self.segments_index+=1

    def make_candidate_set(self, d_max = 200):
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
        self.d_max = d_max
        raise NotImplemtedError


    def path_optimizing(dis_weight=1, stitch_weight=10):
        """Find a optimized path through minimizing
        the sum of distance and stitching score.

        Parameters
        ----------
        dis_weight : `float`
            a cost weight of distance.
        stitch_weight : `float`
            a cost weight of stitching score.

        Returns
        -------
        (`path`, `float`)
            a list of index of selected segments, and its cost.

        A map matching is pretty heavy calculation because
        basically the number of opertunity exponentially will be increasing
        via the size of sequence.
        So, we need to reduce the calculation time through dynamic programming
        or so-called **Dijkstra algorithm** which is the algoritm for finding the shortest path.
        Through set a cost as a huristic(c.f. length in finding shortest path),
        we can optimize the problem as same as minimizing distance.
        It reduces time complexity from `O(n^l)` to `O(l*n^2)` where
        `n` denotes the mean cardinality of each candidate set, and
        `l` denotes the length of sequence.
        """
        #weights
        alpha   =   dis_weight
        beta    =   stitch_weight

        length  =   len(self.targets)

        #cost and path
        cost    =   [np.zeros([layer[1].shape[0]],dtype = np.float64) for layer in self.distance_map]
        path    =   [{} for i in range(length-1)]

        #initialize
        for seg in self.distance_map[0]:
            cost[0][seg] += alpha * self.distance_map[0][1]

        for i in tqdm(range(len(self.target))-1):
            order = i+1
            start_node_num  = self.distance_map[i][1].shape[0]
            end_node_num    = self.distance_map[i+1][1].shape[0]

            #(n)->(m) costs minimization
            costs    = np.zeros([start_node_num, end_node_num], dtype = np.float64)
            #computed minimum costs of last node
            costs   += cost[i]
            costsT   = costs.T
            #adding distance cost of next nodes
            costsT  += alpha * self.distance_map[i+1][1]
            for j,start_seg in enumerate(self.distance_map[i][0]):
                for k,end_seg in enumerate(self.distance_map[i+1][0]):
                    self.stitching_map[j][k] = self.stitching_map[j].get(k, self.segment_set[j].stitch_score(self.segment_set[k]))
                    costs[j][k]             += self.stitching_map[j][k]
            minimum = costs.argmin(axis = 1)
            cost[order] = costs.T[minimum]
            for k,end_seg in enumerate(self.distance_map[i+1][0]):
                path[i][end_seg] = self.distance_map[i][0][minimum[k]]

        #results
        min_index       = cost[-1].argmin()
        cost_min        = cost[-1][min_index]
        selected_path   = [self.distance_map[-1][0][min_index]]
        for i in range(length-1):
            inv = length - 1 - i
            selected_path.append(path[inv][selected_path[-1]])
        selected_path.reverse()
        return selected_path, cost_min

    def path_stitching(self, segments):
        """Make a whole path with given segments.

        Parameters
        ----------
        segments : `list`
            a list of index of segment which will be stitched.

        Returns
        -------
        `taxidata.Segment`
            a whole path which is stitched by given segments.

        """
        Joint_node = segments[0].nodes()
        for seg in segments[1:]:
            start_overlap = np.where(Joint_node == seg.nodes()[0])[0]
            if len(start_overlap)>0:
                Joint_node = np.r_[Joint_node[:start_overlap[0]], seg.nodes()]
            else:
                shortest_path = nx.shortest_path(self.map, Joint_node[-1], seg.nodes()[0],'length')
                shortest_path_array = np.zeros([len(shortest_path)])
                for i in range(len(shortest_path)): shortest_path_array[i]=shortest_path[i]
                Joint_node = np.r_[Joint_node, shortest_path_array[1:], seg.nodes()[1:]]
        edge_in = (Joint_node[0],Joint_node[1],0,self.map.get_edge_data(Joint_node[0],Joint_node[1],0))
        Jointsegment = segment(edge_in)
        for edge_count in range(len(Joint_node)-2):
            edge_in = (Joint_node[edge_count+1],Joint_node[edge_count+2],0,self.map.get_edge_data(Joint_node[edge_count+1],Joint_node[edge_count+2],0))
            Jointsegment = Jointsegment.expand(edge_in)
        return Jointsegment

    def segment_to_line(self, segment):
        """
        segment -> pos_array [x_node,y_ndoe]

        Parameter
        ----------
        self : road network
        segment


        Return
        -------
        pos_array
        np.array([x1,y1],[x2,y2],...)
        """
        pos_list = np.zeros([len(segment.nodes()),2])
        for c in range(len(segment.nodes())):
            pos_list[c] = self.map.nodes[segment.nodes()[c]]['pos']
        return pos_list

    def point_projection(self, path):
        """Find edges that points of `self.target` belong in.

        Parameters
        ----------
        path : `taxidata.Segment`
            A complete path which will be a map with projection.

        Returns
        -------
        `list`
            the list of tuples indicate the edges of road network.

        """
        edge_list = []
        path_line = segment_to_line(self,path)
        for target_point in self.target:
            distance_list = distance_line_point_new(path_line, target_point)
            edge_list.append(path.edges()[np.where(min(distance_list)==distance_list)[0][0]])
        return edge_list



class MultitrackMapMatching(SingleTrackMapMatching):
    """object for multi-track mapmatching."""

    def __init__(self, trajectory_list, road_network):
        super(MultitrackMapMatching, self).__init__(trajectory_list,road_network)


    def matching(self):
        pass
