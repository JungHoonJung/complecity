import geopandas as gpd
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import shapely.geometry as geom
import h5py as h5

__all__ = ['Segment', 'Roadnetwork', 'k_segments', 'k_segments_strict_bfs', 'k_segments_semi_strict_bfs', 'k_segments_strict_bfs_with_length']

class Segment:
    def __init__(self, edge = None):
        if edge is None:
            #Do nothing
            pass
        else:
            #initialize with given node as segment
            self.start_node = edge[0]
            self.num = 1
            self.path = np.empty([2], dtype = [('node','i4'),('id','i4')])
            self.path[0] = tuple((edge[0], 0))
            self.path[1] = tuple(edge[1:3])
            self.past_node = self.start_node
            self.last_node = edge[1]
            self.total_length = edge[-1]['length']
            self.length = [edge[-1]['length']]
            self.angle = edge[-1]['angle']
            self.edgelist = {edge[:3]:True}
            self.total_angle  = np.array([0],dtype = np.float32)
            #index
            self.id =None

    def expand(self, edge):
        """return copy of segment appending extra edge

        Parameters
        ----------
        edge : road network edege
            (start_node, end_node, {'ID', 'length', 'geometry', 'angle'})

        Returns
        -------
        type
            Description of returned object.

        When segment expand by new edge(road), this function add some edge's information
        to segment.
        """
        temp = Segment()
        temp.start_node = self.start_node
        temp.past_node = edge[0]
        temp.last_node = edge[1]
        temp.num = self.num+1
        temp.path = np.empty([temp.num+1],dtype = [('node','i4'),('id','i4')])
        temp.path[:-1] = self.path
        temp.path[-1] = edge[1:3]
        temp.total_length = self.total_length + edge[-1]['length']
        temp.length = self.length.copy()
        temp.length.append(edge[-1]['length'])
        temp.angle =  edge[-1]['angle']
        temp.edgelist = {edge[:3]:True}
        for e in self.edgelist:
            temp.edgelist[e] = True
        temp.total_angle = np.zeros([temp.num],dtype = np.float32)
        temp.total_angle[:-1] = self.total_angle + temp.angle- self.angle
        return temp

    def check(self, k):
        """check condition of k segments
        Parameters
        ----------
        k : int
            limited path length
        Returns
        -------
        type
            Description of returned object.

        """

        return self.total_length> k or self.total_angle[-1]<-2*np.pi or self.total_angle[-1]>2*np.pi #(self.total_angle <-2*np.pi).any() or (self.total_angle > 2*np.pi).any()

    def overlap(self, edge):
        '''check overlap with given edge'''
        if self.num == 1:
            return False
        return edge[:3] in self.edgelist

    def __repr__(self):
        return "<segment from node '{}' to '{}', total num : {}>".format(self.start_node, self.last_node, self.num)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.start_node == other.start_node and (self.path==other.path).all()
        else:
            return False

    def __lt__(self, other):
        '''sorting'''
        return self.total_length<other.total_length

    def __gt__(self, other):
        '''sorting'''
        return self.total_length>other.total_length

    def __le__(self, other):
        '''sorting'''
        return self.total_length<=other.total_length

    def __ge__(self, other):
        '''sorting'''
        return self.total_length>=other.total_length

    def edges(self):
        '''return edgelist'''
        e = []
        temp = self.start_node
        for p in self.path[1:]:
            e.append((temp,p['node'],p['id']))
            temp = p['node']
        return e

    def nodes(self):
        '''return node list'''
        return self.path['node']

    def plot(self, pos, *arg,**kwarg):
        """Short summary.
        '''plot segment in aspect of graph'''
        Parameters
        ----------
        pos : node_pos

        *arg : type
            Description of parameter `*arg`.
        **kwarg : type
            Description of parameter `**kwarg`.

        Returns
        -------
        Road segment plot(Using networkx.draw).
        """

        temp = nx.path_graph(self.num+1,create_using=nx.DiGraph)
        position = {}
        for i,n in enumerate(self.nodes()):
            position[i] = pos[n]
        nx.draw(temp, position, *arg, **kwarg)

    def stitch_score(self, other):
        """Calculate stitch score with `self` and other.

        Parameters
        ----------
        other : taxidata.segment
            a segment which will be compared with `self`

        Returns
        -------
        stitch score : float
            returns a consistency score which is cost of jointing self and other

        When the overlap between the last part of `self` and the initial part of `other`
        exists, `other` is consistent with `self`. The stitching score measure the consistency
        with quantifying the size of overlap. If `self` is same as `other`,
        the size of overlap goes whole segment which is jointed with `self` and `other`,
        and the stitching score can be measured as 0.
        The other hand, when `self` and `other` is not consistent, the stitching score will be 1
        as maximum score.
        """
        if self == other: return 0
        start_overlap = np.where(self.path == other.path[0])[0]
        # seg2 start node doesn't match with seg1
        if len(start_overlap) == 0: stitchScore = 1
        # seg2 start node in seg1
        else:
            if (self.path[start_overlap[0]:] == other.path[:len(self.path[start_overlap[0]:])]).all():
                overlap_length = sum(self.length[start_overlap[0]:])
                total_length = self.total_length + other.total_length - overlap_length
                stitchScore = 1 - overlap_length/total_length
            else:stitchScore = 1
        return stitchScore




class Roadnetwork(nx.MultiDiGraph):

    def __init__(self, *arg ,**kwarg):
        super(Roadnetwork, self).__init__(*arg ,**kwarg)

    def pos():
        doc = '''return position dictionary'''
        def fget(self):
            return self.nodes(data = 'pos')
        return locals()
    pos = property(**pos())


    def subgraph_of_node(self, node, depth_limit = 2):
        """return subgraph of given node with bfs manner

        Parameters
        ----------
        node : int
            start path node which on the network
        depth_limit : int
            depth of path from start node

        Returns
        -------
        type
            subgraph of path

        """
        nodes = {node : 0}
        for edge in nx.bfs_edges(self, node, depth_limit= depth_limit):
            nodes[edge[1]] = 0

        nodes = list(nodes.keys())
        if depth_limit == 0:
            nodes = [node]
        return self.subgraph(nodes)

    def nn_nodes(self, node, depth_limit = 2):
        """Short summary.
        '''return nodes from given node with bfs manner'''
        Parameters
        ----------
        node : int
            G's node
        depth_limit : int
            depth of path from start node

        Returns
        -------
        type list
            node list

        """

        nodes = {node : 0}
        for edge in nx.bfs_edges(self, node, depth_limit= depth_limit):
            nodes[edge[1]] = 0

        nodes = list(nodes.keys())
        if depth_limit == 0:
            nodes = [node]
        return nodes



    def edge_plot(self):
        """Short summary.
        '''plot edges in given graph'''
        """

        for i in self.edges(data = 'geometry'):
            plt.plot(*i[2].xy)

    def edgelist_plot(self, edgelist):
        """Short summary.
        '''plot edges in given edgelist '''
        Parameters
        ----------
        edgelist : geopandas

        Returns
        -------
        type
            plot edges

        """

        for edge in edgelist:
            plt.plot(*self.edges[edge]['geometry'].xy)

    def subgraph_plot(self, node, depth_limit = 2):
        """Short summary.
        '''making subgraph and plot'''
        Parameters
        ----------
        node : int
            start node of path
        depth_limit : int
            depth of path from start node

        Returns
        -------
        type
            subgraph bfs_edges
        """
        sub = self.subgraph_of_node(node, depth_limit)
        node_pos = pos(sub)[node]

        edge_plot(sub)
        plt.scatter(*node_pos, s= 100)





def k_segments(G, node, k= 100):
    """Short summary.
    '''k_segments with only breadth-first searching'''
    Parameters
    ----------
    G : Network

    node : int
        node which starts point of k_segment
    k : int
        segment's length

    Returns
    -------
    type dictionay
        k-segments
    """
    segments = [Segment(edge) for edge in G.edges(node,keys = True, data = True)]
    k_segments = []
    iter_num  = 0
    while segments:
        iter_num += 1
        target = segments.pop(0)
        ch = False
        #print("target : {},{}".format(target.past_node, target.last_node))
        for edge in G.edges(target.last_node, keys = True, data = True):
            if edge[1] == target.past_node or target.overlap(edge): continue
            #print("to : {}, {}".format(edge[0], edge[1]))
            ch = True
            temp = target.expand(edge)
            if temp.check(k):
                k_segments.append(temp)
            else:
                segments.append(temp)
        if not ch:
            k_segments.append(target)
        if iter_num == 1e5:
            print(node)
        #print(k_segments)
    return k_segments

def k_segments_strict_bfs(G, node, k= 100):
    """Short summary.
    '''k_segment with no overlapping node'''
    Parameters
    ----------
    G : Network
        Description of parameter `G`.
    node : int
        node which starts point of k_segment
    k : int
        segment's length

    Returns
    -------
    type dictionay
        k-segments with no overlapping node

    """

    segments = [Segment(edge) for edge in G.edges(node,keys = True, data = True)]
    k_segments = []
    nodes = {node :True}
    iter_num  = 0
    while segments:
        iter_num += 1
        target = segments.pop(0)
        ch = False
        #print("target : {},{}".format(target.past_node, target.last_node))
        for edge in G.edges(target.last_node, keys = True, data = True):
            if edge[1] in nodes: continue
            #print("to : {}, {}".format(edge[0], edge[1]))
            ch = True
            nodes[edge[1]] = True
            temp = target.expand(edge)
            if temp.check(k):
                k_segments.append(temp)
            else:
                segments.append(temp)
        #if not ch:
            #k_segments.append(target)
        if iter_num == 1e5:
            print(node)
        #print(k_segments)
    return k_segments

def k_segments_strict_bfs_with_length(G, node, k= 100):
    """Short summary.
    '''k_segment with no overlapping node and search with length.'''
    Parameters
    ----------
    G : Network

    node : int
        node which starts point of k_segment
    k : int
        segment's length

    Returns
    -------
    type dictionay
        k-segments with no overlapping node and search with length

    """

    segments = [Segment(edge) for edge in G.edges(node,keys = True, data = True)]
    k_segments = []
    nodes = {node :True}
    iter_num  = 0
    segments.sort()
    while segments:
        iter_num += 1
        target = segments.pop(0)
        ch = False
        #print("target : {},{}".format(target.past_node, target.last_node))
        for edge in G.edges(target.last_node, keys = True, data = True):
            if edge[1] in nodes: continue
            #print("to : {}, {}".format(edge[0], edge[1]))
            ch = True
            nodes[edge[1]] = True
            temp = target.expand(edge)
            if temp.check(k):
                k_segments.append(temp)
            else:
                segments.append(temp)
        if not ch:
            k_segments.append(target)
        if iter_num == 1e5:
            print(node)
        #print(k_segments)
        segments.sort()
    return k_segments

def k_segments_semi_strict_bfs(G, node, k= 100):
    """Short summary.
    '''k_segment with no overlap within single segment.'''
    Parameters
    ----------
    G : Network

    node : int
        node which starts point of k_segment
    k : int
        segment's length

    Returns
    -------
    type dictionay
        k-segments with no overlapping node and search with length

    """

    segments = [Segment(edge) for edge in G.edges(node,keys = True, data = True)]
    k_segments = []
    nodes = {node :True}
    iter_num  = 0
    while segments:
        iter_num += 1
        target = segments.pop(0)
        ch = False
        #print("target : {},{}".format(target.past_node, target.last_node))
        for edge in G.edges(target.last_node, keys = True, data = True):
            if edge[1] in target.nodes(): continue
            #print("to : {}, {}".format(edge[0], edge[1]))
            ch = True
            nodes[edge[1]] = True
            temp = target.expand(edge)
            if temp.check(k):
                k_segments.append(temp)
            else:
                segments.append(temp)
        #if not ch:
            #k_segments.append(target)
        if iter_num == 1e5:
            print(node)
        #print(k_segments)
    return k_segments
