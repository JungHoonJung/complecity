import pyproj
import numpy as np
import taxidata as td

def toUTM(dataX,dataY, inverse = False):
    """
    convert from UTM coord to WGS84 coord

    input longitude, latitude UTM coordinate
    return longitude, latitude WGS84 coordinate
    """
    KoreaZone = 52
    p = pyproj.Proj(proj = 'utm', zone = '52N', ellps='WGS84')
    dataX, dataY = p(dataX, dataY, inverse = inverse)
    return dataX,dataY  # lon, lat

def distance(line, point):
    """return distance between taxi data's position and given point.
    Parameters
    ----------
    point : array,tuple,list
        the point where you want to know how far from each point from trajectories.

    Returns
    -------
    float
        result of distance from point from trajectories.

    """
    lines=line[:-1]-line[1:]
    a=-lines[:,1]
    b=lines[:,0]
    c=-a*line[:,0][:-1]-b*line[:,1][:-1]

    shortest=np.abs(a*point[0]+b*point[1]+c)/np.sqrt(a*a+b*b)
    m1=-a/(b+1e-12)
    m2=-1/(m1+1e-12)

    x=(m1*line[:,0][:-1]-m2*point[0]-line[:,1][:-1]+point[1])/(m1-m2)
    y=m2*(x-point[0])+point[1]

    yesorno=(line[:,0][:-1]-x)*(line[:,0][1:]-x)+(line[:,1][:-1]-y)*(line[:,1][1:]-y)

    len1=np.sqrt((line[:,0][:-1]-point[0])**2+(line[:,1][:-1]-point[1])**2)
    len2=np.sqrt((line[:,0][1:]-point[0])**2+(line[:,1][1:]-point[1])**2)

    short=shortest*(yesorno<=0)+np.minimum(len1,len2)*(yesorno>0)

    return np.min(short)

def make_node():
    """return all nodes in seoul.
    Parameters
    ----------
    None

    Returns
    -------
    List

    Two lists of node's position and node's id.

    """

    Seoul = td.Roadnetwork()
    for l, e in s_elist.iterrows():
        geom = s_link['geometry'][int(e['EDGE'])-1]
        Seoul.add_edge(int(e['START_NODE']),int(e['END_NODE']),ID = int(e['EDGE']), length = float(e['LENGTH']), geometry = geom)
        Seoul.nodes[int(e['START_NODE'])]['pos'] = (float(e['XCoord']),float(e['YCoord']))
    def angle(G, node1, node2):
        '''aspect of node1 as origin, return angle of node2 in sence of polar coordinates.'''
        p1 = G.nodes[node1]['pos']
        p2 = G.nodes[node2]['pos']
        p2_ = (p2[0]-p1[0],p2[1]-p1[1])
        return np.arctan2(p2_[1],p2_[0])
    for edge in Seoul.edges(data = True):
        edge[-1]['angle']=angle(Seoul, edge[0],edge[1])
    
    pos = Seoul.pos

    return Seoul


def k_position(start_node):
    """return all segment position.
    Parameters
    ----------
    Node id

    Returns
    -------
    List

    List of node's position in segment.

    """
    seg = td.k_segments_strict_bfs_with_length(Seoul, start_node, 800)
    len_seg = len(seg)
    list_seg = [[start_node]for l in range(len_seg)]
    n = 0
    for i in seg:
        for j in i.edges():
            list_seg[n].append(j[1])
        n += 1

    position = []
    for i in list_seg:
        node=np.array([seoul_dict[j] for j in i])
        position.append(node)
    return position

def node_in_grid(grid_set):
    """return nodes in grid set.
    Parameters
    ----------
    Grid

    Returns
    -------
    List

    List of node's in grid.

    """
    node = []
    for i in grid_set:
        node.append(grid_200[i])
    return node