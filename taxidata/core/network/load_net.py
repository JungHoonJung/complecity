import geopandas as gpd
import networkx as nx
import numpy as np
from .match import Roadnetwork
import pkg_resources

__all__= ['load_seoul',"load_RN","save_RN"]

def load_seoul(load_geom = False):
    Seoul = Roadnetwork()
    #print(pkg_resources.resource_filename(__name__, "nodelink/Seoul_Edgelist.csv"))
    s_elist = gpd.read_file(pkg_resources.resource_filename(__name__, "nodelink/Seoul_Edgelist.csv")) #get filename through a filesystem
    if load_geom:
        s_link = gpd.read_file(pkg_resources.resource_filename(__name__, "nodelink/Seoul_Links.shp"))
    #s_elist = gpd.read_file(r'.\taxidata\core\network\nodelink\Seoul_Edgelist.csv')
    #s_link = gpd.read_file(r".\taxidata\core\network\nodelink\Seoul_Links.shp")
    if load_geom:
        for l, e in s_elist.iterrows():
            geom = s_link['geometry'][int(e['EDGE'])-1]
            Seoul.add_edge(int(e['START_NODE']),int(e['END_NODE']),ID = int(e['EDGE']), length = float(e['LENGTH']), geometry = geom)
            Seoul.nodes[int(e['START_NODE'])]['pos'] = (float(e['XCoord']),float(e['YCoord']))
    else:
        for l, e in s_elist.iterrows():
            Seoul.add_edge(int(e['START_NODE']),int(e['END_NODE']),ID = int(e['EDGE']), length = float(e['LENGTH']))
            Seoul.nodes[int(e['START_NODE'])]['pos'] = (float(e['XCoord']),float(e['YCoord']))

    def angle(G, node1, node2):
        '''aspect of node1 as origin, return angle of node2 in sence of polar coordinates.'''
        p1 = G.nodes[node1]['pos']
        p2 = G.nodes[node2]['pos']
        p2_ = (p2[0]-p1[0],p2[1]-p1[1])
        return np.arctan2(p2_[1],p2_[0])
    for edge in Seoul.edges(data = True):
        edge[-1]['angle']=angle(Seoul, edge[0],edge[1])
    return Seoul


def load_RN(path = None, target = "Seoul", load_geom = False):
    if path is not None:
        fname = path
    else:
        fname = pkg_resources.resource_filename(__name__, f"nodelink/RN_{target.lower()}.npz")
    npz = np.load(fname)
    Graph = nx.from_edgelist(npz['edgelist'], create_using=Roadnetwork)
    for edge,l,a in zip(npz['edgelist'],npz['length'],npz['angle']):
        Graph.edges[[*edge]]['length'] = l 
        Graph.edges[[*edge]]['angle'] = a
    for n, x, y in npz['pos']:
        Graph.nodes[int(n)]['pos'] = (x,y)
    return Graph

def save_RN(path, Graph):
    data = np.empty([len(Graph.edges),5])
    data[:,:3] = np.array(Graph.edges)
    for i in data:
        line = Graph.edges[i[:3]]
        i[3] = line['length']
        i[4] = line['angle']
    pos = Graph.pos
    nppos = np.empty([len(pos),3])
    i = 0
    for key in pos:
        nppos[i] = (key[0],*key[1])
        i+=1
    np.savez(path, edgelist = data[:,:3].astype(np.int32), length = data[:,3], angle = data[:,4], pos = nppos)