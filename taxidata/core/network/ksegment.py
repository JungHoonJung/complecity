import geopandas as gpd
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import shapely.geometry as geom
import h5py as h5
import tqdm

__all__ = ['Segment', 'KSegment', 'Roadnetwork', 'kseg_flattening', 'get_seg_id','k_segments', 'k_segments_strict_bfs', 'k_segments_semi_strict_bfs', 'k_segments_strict_bfs_with_length']

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
            return all([self.start_node == other.start_node, np.array_equal(self.path, other.path)])
            # ? start_node도 봐야하나?? path끼리만 비교해도 되지 않으려나?
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
            if np.array_equal(self.path[start_overlap[0]:], other.path[:len(self.path[start_overlap[0]:])]):
                overlap_length = sum(self.length[start_overlap[0]:])
                total_length = self.total_length + other.total_length - overlap_length
                stitchScore = 1 - overlap_length/total_length
            else:stitchScore = 1
        return stitchScore

class segment(np.ndarray):
    def nodes(self):
        a = np.empty([len(self)+1], dtype = np.int32)
        a[:-1] = self['start']
        a[-1] = self[-1]['end']
        return a

    @property
    def start(self):
        return
    @start.getter
    def start(self):
        return self['start']

    @property
    def end(self):
        return
    @end.getter
    def end(self):
        return self['end']

    @property
    def indices(self):
        return
    @indices.getter
    def indices(self):
        return self['indices']

    @property
    def length(self):
        return
    @length.getter
    def length(self):
        return self['length']

    @property
    def node(self):
        return
    @node.getter
    def node(self):
        return self.nodes()






def kseg_flattening(*ksegments):
    """ return k segment array, length_array, and total length to calculate d_curve
    Parameters
    ----------
    ksegments : `taxidata.segment`
        ksegment of RoadNetwork

    Return
    --------
    `list`
        the returned list contain three components.
        - segment_array : `np.ndarray` flatten nodes of all of given k-segments.
        - length_array : `np.ndarray` array with lengths of given k-segments.
        - total_length : `int` total number of given k-segments.
    """
    length          = np.array([len(seg)+1 for seg in ksegments])
    segment_array   = np.empty([length.sum()], dtype = np.int32)
    total_length    = len(length)
    lcum            = length.cumsum()
    for i, seg in enumerate(ksegments):
        if i ==0:
            segment_array[0:lcum[0]] = seg.nodes()
        else:
            segment_array[lcum[i-1]:lcum[i]] = seg.nodes()
    return segment_array, length, total_length

def get_seg_id(*ksegments):
    """return segment id from k-segment list.

    Parameters
    -----------
    ksegments : `taxidata.segment`
        ksegment of RoadNetwork

    Return
    --------
    `list`
        a list of tuple form as (start_node, index).
    """
    return [(s.start[0],s.seg_id) for s in ksegments]

class KSegment():
    def __init__(self, hdf5):
        self.file = hdf5
        self._object = {}
        self._nodes = {}
        with h5.File(self.file, 'r+') as f:
            for i in f:
                self._nodes[int(i)] = True
        self.mask = np.vectorize(self.__contains__)
        self.__contains__ = self.mask
        #self.add_meta_data()

    def get_nodes(self):
        """return full nodes list in this file.

        Returns:
            `list` : nodes as integer id.
        """
        return list(self._nodes.keys())

    def __contains__(self, node):
        return self._nodes.get(node, False)


    def mask(self, node):
        return self._nodes.get(node, False)

    def filtrate(self, nodes):
        if not isinstance(nodes, np.ndarray):
            nodes = np.array(nodes, dtype=np.int32)
        return nodes[np.vectorize(self.__contains__)(nodes)]

    def add_meta_data(self):
        with h5.File(self.file, 'r+') as f:
            for i,n in enumerate(f):
                if i == 0:
                    if f[n].get('seg_len',False):
                        return
                    break
            for node in tqdm.tqdm(f):
                folder = f[node]
                mask = (folder['node'][:]!=-1)
                seg_len = mask.astype(np.uint8).sum(axis=1)+1
                folder.create_dataset('seg_len',data = seg_len, compression = 'lzf')
                assert folder['node'].shape[0] == seg_len.shape[0], f"{folder['node'].shape[0]} != {seg_len.shape[0]}"

    def _load_node(self, start_nodes): # from start_nodes `list` get array of
        nodes = []
        with h5.File(self.file, 'r') as f:
            for snode in start_nodes:
                shape = f[f'{snode}']['node'].shape
                buf = np.empty([shape[0], shape[1]+1],dtype = np.int32)
                buf[:,0] = snode
                buf[:,1:] = f[f'{snode}']['node'][:]
                nodes.append(buf)
        return nodes

    def _load_length(self, start_nodes):
        nodes = []
        with h5.File(self.file, 'r') as f:
            for snode in start_nodes:
                nodes.append(f[f'{snode}']['length'][:])
        return nodes

    def _load_edge(self, start_nodes,length = False, fn_tqdm= None):
        with h5.File(self.file, 'r') as f:
            edges = []
            if fn_tqdm is None:
                fn_tqdm = lambda x:x
            for snode in fn_tqdm(start_nodes):
                shape = f[f'{snode}']['node'].shape
                buf = np.empty([shape[0], shape[1]+1],dtype = np.int32)
                buf[:,0] = snode
                buf[:,1:] = f[f'{snode}']['node'][:]
                if length:
                    edge = np.empty(shape, dtype = [('start','i4'),('end','i4'),('indices','i1'),('length','f4')])
                    edge['length'] = f[f'{snode}']['length'][:]
                else:
                    edge = np.empty(shape, dtype = [('start','i4'),('end','i4'),('indices','i1')])
                edge['start'] = buf[:,:-1]
                edge['end'] = buf[:,1:]
                edge['indices'] = f[f'{snode}']['index'][:]
                edges.append(edge.view(segment))
        return edges

    def loads(self, start_nodes, length = True):
        if start_nodes =='*':
            start_nodes = self.get_nodes()
        edges = self._load_edge(start_nodes, length, fn_tqdm=tqdm.tqdm)
        for s, e in zip(start_nodes, edges):
            self._object[s] = e

    def clear(self):
        self._object.clear()

    def get_segment_nodes(self, start_node):
        s_n = start_node
        if self._object.get(s_n, None) is None:
            self._object[s_n] = self._load_edge(s_n)
        data = self._object[s_n]
        edges = []
        seg_len = (data['start']!=-1).astype(np.uint8).sum(axis=1)
        for d, l in zip(data, seg_len):
            edges.append(d[:l])
        return edges

    def __getitem__(self, value):
        """
        docstring
        """
        if isinstance(value, (tuple, np.ndarray)):
            s_n, ind = value
            if self._object.get(s_n, None) is None:
                self._object[s_n] = self._load_edge([s_n])[0]
            data =  self._object[s_n][ind]
            edge = data[data['end']!=-1]
            edge.seg_id = ind
            return edge
        else:
            s_n = value
            if self._object.get(s_n, None) is None:
                self._object[s_n] = self._load_edge([s_n])[0]
            data = self._object[s_n]
            edges = []
            seg_len = (data['end']!=-1).astype(np.uint8).sum(axis=1)
            for i, (d, l) in enumerate(zip(data, seg_len)):
                edge = d[:l]
                edge.seg_id = i
                edges.append(edge)
            return edges

    def _stitch_score(self, seg1, seg2):
        """A function which is calculating stitching score from seg1 to seg2.

        Parameters
        ------------
        seg1 : `tuple (start_node, order)`
            Segment.
        seg2 : `tuple (start_node, order)`
            Segment.

        Return
        ------------
        stitch score(float)

        When the overlap between the last part of `seg1` and the initial part of `seg2`
        exists, `seg2` is consistent with `seg1`. The stitching score measure the consistency
        with quantifying the size of overlap. If `seg1` is same as `seg2`,
        the size of overlap goes whole segment which is jointed with `seg1` and `other`,
        and the stitching score can be measured as 0.
        The other hand, when `seg1` and `seg2` is not consistent, the stitching score will be 1
        as maximum score.

        """
        seg1 = self[seg1]
        seg2 = self[seg2]
        l1 = seg1['length'].sum()
        l2 = seg2['length'].sum()
        n1 = seg1.shape[0]
        n2 = seg2.shape[0]
        for i, edge in enumerate(seg1):
            if edge == seg2[0]:
                if n2>=n1-i and seg2[n1-i-1]==seg1[-1]:
                    if (seg1[i:]==seg2[:n1-i]).all():
                        ol = seg1[i:]['length'].sum()
                        return 1 - ol/(l1+l2-ol)
        return 1




    def stitch_score(self, seg1, seg2):
        """A function which is calculating stitching score.

        Parameters
        ------------
        seg1 : `tuple (start_node, order)`
            Segment.
        seg2 : `tuple (start_node, order)`
            Segment.

        """
        if seg1==seg2:
            return 0
        return min(self._stitch_score(seg1, seg2), self._stitch_score(seg2, seg1))

    def stitch_score_with_firstOverlap(self, seg1, seg2, first_overlap):
        """
        we firstly made stitching_map. So we know where is the first overlap position between seg1 & seg2,
        should not check where is overlaping
        """
        seg1 = self[seg1]
        seg2 = self[seg2]
        
        last_overlap = len(seg1) - first_overlap - 1
        if (seg1[first_overlap:] == seg2[:last_overlap]).all():
            ol = seg1[first_overlap:]['length'].sum()
            l1 = seg1['length'].sum()
            l2 = seg1['length'].sum()
            return 1 - ol/(l1+l2-ol)
        else: return 1


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
        node_pos = pos[node]

        self.edge_plot(sub)
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
    """k_segment with no overlap within single segment.
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


def k_segments_with_shortest_path(G, node, k = 100):
    """generate k_segment which is the shortest path of node i,j with length under k.
    Parameters
    ----------
    G : `RoadNetwork(nx.MultiDiGraph)`

    node : `int`
        node which starts point of k_segment

    k : `int`
        segment's length

    Returns
    -------
    `dict`
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
