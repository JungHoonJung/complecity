import geopandas as gpd
import numpy as np
from .match import Roadnetwork
import pkg_resources

__all__= ['load_seoul']

def load_seoul():
    Seoul = Roadnetwork()
    print(pkg_resources.resource_filename(__name__, "nodelink/Seoul_Edgelist.csv"))
    s_elist = gpd.read_file(pkg_resources.resource_filename(__name__, "nodelink/Seoul_Edgelist.csv")) #get filename through a filesystem
    s_link = gpd.read_file(pkg_resources.resource_filename(__name__, "nodelink/Seoul_Links.shp"))
    #s_elist = gpd.read_file(r'.\taxidata\core\network\nodelink\Seoul_Edgelist.csv')
    #s_link = gpd.read_file(r".\taxidata\core\network\nodelink\Seoul_Links.shp")
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
    return Seoul