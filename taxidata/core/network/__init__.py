import numpy as np
import networkx as nx
import os
import re
import matplotlib.pyplot as plt
<<<<<<< HEAD
<<<<<<< HEAD
import math

# edgelist data convert to npy
def convert2npy_edgelist(path,filename):
    """Short summary.
    Chengdu road linklist's raw data is csv format. This function convert to npy format.

    Parameters
    ----------
    path : string ex) '/home/dataset/'
        path of raw csv data

    filename : string ex) 'ChengduLink'
        new name of new file


    Returns
    -------
    type filename.npy
        np.array(dtype=[('Link', 'int'), ('Node_Start', 'int'), ('Longitude_Start', 'float'),
            ('Latitude_Start', 'float'),('Node_End', 'int'), ('Longitude_End', 'float'),('Latitude_End', 'float'),('LENGTH', 'float')])

    """
    data = np.genfromtxt(path, delimiter=',',skip_header=1,dtype=[('Link', 'int'), ('Node_Start', 'int'), ('Longitude_Start', 'float'),('Latitude_Start', 'float'),('Node_End', 'int'), ('Longitude_End', 'float'),('Latitude_End', 'float'),('LENGTH', 'float')])
    np.save(filename,data)

# speed data convert to npy
def convert2npy_linkspeed(Path):
    """Short summary.
    Chengdu road speed data's raw data is csv format. This function convert to npy format.

    Parameters
    ----------
    Path : string ex) '/home/dataset'
        path of raw csv data

    Returns
    -------
    type speed[monthDay]_[1or0].npy
        np.array(dtype=[('Period','U12'),('Link','int'),('Speed','float')])

    """
    path_dr = Path
    file_list = os.listdir(path_dr)
    file_list.sort()
    file_list = file_list[5:len((file_list))]
    for i in range(len(file_list)):
        path=file_list[i]
        data = np.genfromtxt(os.path.join(Path,path),delimiter=',',skip_header=1, dtype=[('Period','U12'),('Link','int'),('Speed','float')])
        filename=int(re.findall('\d+',path)[0])
        fileType=int(re.findall('\d+',path)[1])
        np.save('speed[{}]_[{}].npy'.format(filename,fileType),data)

# generate Street network
def genStreetNet(Edgelist):
    """Short summary.
    Geneate road network with 'No' direct.
    Parameters
    ----------
    Edgelist : np.array(dtype=[('Link', 'int'), ('Node_Start', 'int'), ('Longitude_Start', 'float'),
        ('Latitude_Start', 'float'),('Node_End', 'int'), ('Longitude_End', 'float'),('Latitude_End', 'float'),('LENGTH', 'float')])


    Returns
    -------
    type Graph()


    """
=======
=======
>>>>>>> graph module

# edgelist, speed data convert to npy
# def conver2npy_edgelist(path,filename):
#     data = np.genfromtxt(path, delimiter=',',skip_header=1,dtype=[('Link', 'int'), ('Node_Start', 'int'), ('Longitude_Start', 'float'),('Latitude_Start', 'float'),('Node_End', 'int'), ('Longitude_End', 'float'),('Latitude_End', 'float'),('LENGTH', 'float')])
#     np.save(filename,data)
# def convert2npy_linkspeed(path):
#     path_dr = path
#     file_list = os.listdir(path_dr)
#     file_list.sort()
#     re_file_list = file_list[5:len((file_list))]
#     for path_file in re_file_list:
#         data = np.genfromtxt(path_file,delimiter=',',skip_header=1, dtype=[('Period','U12'),('Link','int'),('Speed','float')])
#         filename=int(re.findall('\d+',path_file)[0])
#         np.save('{}.npy'.format(filename),data)

# generate Street network
def genStreetNet(Edgelist):
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> graph module
=======
    """Short summary.

    Parameters
    ----------
    Edgelist : type
        Description of parameter `Edgelist`.

    Returns
    -------
    type
        Description of returned object.

    """
>>>>>>> docstring test
=======
>>>>>>> graph module
    # node label & number
    node_list = np.unique(Edgelist['Node_Start'])
    # network generating
    G = nx.DiGraph()
    # add nodes
    G.add_nodes_from(node_list)
    # add edges
    for i in range(len(Edgelist)):
        G.add_edge(Edgelist['Node_Start'][i],Edgelist['Node_End'][i],label=Edgelist['Link'][i])
    return G

# generate newowrk nodes' position
def network_pos(Edgelist):
<<<<<<< HEAD
<<<<<<< HEAD
    """Short summary.
    Generate network node position.
    ex) pos=network_pos(Edgelist)
        nx.draw_networkx(network, pos=pos, ...)

    Parameters
    ----------
    Edgelist : np.array(dtype=[('Link', 'int'), ('Node_Start', 'int'), ('Longitude_Start', 'float'),
        ('Latitude_Start', 'float'),('Node_End', 'int'), ('Longitude_End', 'float'),('Latitude_End', 'float'),('LENGTH', 'float')])

    Returns
    -------
    type tuple


    """
=======
>>>>>>> graph module
=======
>>>>>>> graph module
    # assign pos for nodes
    return {i:[Edgelist[Edgelist['Node_Start']==i]['Longitude_Start'][0],Edgelist[Edgelist['Node_Start']==i]['Latitude_Start'][0]]for i in range(len(np.unique(Edgelist['Node_Start'])))}

# get max velocity each street link
def Max_velocity(velocity0,velocity1):
<<<<<<< HEAD
<<<<<<< HEAD
    """Short summary.
    Find each link's fatest speed in whole day.
    The reason why it takes two speed array is Chengdu's speed data splice day in two Period. 03:00~13:00, 13:00~23:00
    Parameters
    ----------
    velocity0 : np.array(dtype=[('Period','U12'),('Link','int'),('Speed','float')])
    velocity1 : np.array(dtype=[('Period','U12'),('Link','int'),('Speed','float')])

    Returns
    -------
    type np.array(dtype=[('Period','U12'),('Link','int'),('Speed','float')])

    """
=======
>>>>>>> graph module
=======
>>>>>>> graph module
    max_velo = np.zeros(len(np.unique(velocity0['Link'])))
    for i in range(len(max_velo)):
        max_velo[i] = max([max(velocity0[velocity0['Link'] == i+1]['Speed']),max(velocity1[velocity1['Link'] == i+1]['Speed'])])
    return max_velo

# get relative velocity
def relativeVelocity(Period,velocity0,velocity1):
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
    """Short summary.
    Divide road's each period speed by Fastest speed, get relative velocity each road

    Parameters
    ----------
    Period : string
        ex) '03:00-03:02'
    velocity0 : np.array(dtype=[('Period','U12'),('Link','int'),('Speed','float')])
    velocity1 : np.array(dtype=[('Period','U12'),('Link','int'),('Speed','float')])

    Returns
    -------
    type np.array(dtype=[('Period','U12'),('Link','int'),('Speed','float')])


    """
=======
>>>>>>> graph module
=======
    """Short summary.

    Parameters
    ----------
    Period : type
        Description of parameter `Period`.
    velocity0 : type
        Description of parameter `velocity0`.
    velocity1 : type
        Description of parameter `velocity1`.

    Returns
    -------
    type
        Description of returned object.


    dkdfef

    .. note::
        test note
    """
>>>>>>> docstring test
=======
>>>>>>> graph module
    return np.array(velocity0[velocity0['Period']==Period]['Speed']/Max_velocity(velocity0,velocity1))

# generate network given weight by relative speed
def genStreetNet_speed(Edgelist,reVelo):
<<<<<<< HEAD
<<<<<<< HEAD
    """Short summary.
    Generate road network assigned relative velocity as weight on each link

    Parameters
    ----------
    Edgelist : np.array(dtype=[('Link', 'int'), ('Node_Start', 'int'), ('Longitude_Start', 'float'),
        ('Latitude_Start', 'float'),('Node_End', 'int'), ('Longitude_End', 'float'),('Latitude_End', 'float'),('LENGTH', 'float')])

    reVelo : type np.array(dtype=[('Period','U12'),('Link','int'),('Speed','float')])

    Returns
    -------
    type Graph()

    """
=======
>>>>>>> graph module
=======
>>>>>>> graph module
    # node label & number
    node_list = np.unique(Edgelist['Node_Start'])
    # network generating
    G = nx.DiGraph()
    # add nodes
    G.add_nodes_from(node_list)
    # add edges
    for i in range(len(Edgelist)):
        G.add_edge(Edgelist['Node_Start'][i],Edgelist['Node_End'][i],label=Edgelist['Link'][i],weight=reVelo[i])
    return G
<<<<<<< HEAD
<<<<<<< HEAD

# remove link under parameter q
def remove_qRoad(q,Edgelist,reVelo):
    """Short summary.
    Generate road network that cutted links(roads) which weight(relative velocity) smaller than q

    Parameters
    ----------
    q : float

    Edgelist : np.array(dtype=[('Link', 'int'), ('Node_Start', 'int'), ('Longitude_Start', 'float'),
        ('Latitude_Start', 'float'),('Node_End', 'int'), ('Longitude_End', 'float'),('Latitude_End', 'float'),('LENGTH', 'float')])

    reVelo : type np.array(dtype=[('Period','U12'),('Link','int'),('Speed','float')])

    Returns
    -------
    type Graph()

    """
=======
# remove link under parameter q
def remove_qRoad(q,Edgelist,reVelo):
>>>>>>> graph module
=======
# remove link under parameter q
def remove_qRoad(q,Edgelist,reVelo):
>>>>>>> graph module
    orign_net = genStreetNet_speed(Edgelist,reVelo)
    return_net = genStreetNet_speed(Edgelist,reVelo)
    Edge = np.array(orign_net.edges)
    for i in range(len(Edge)):
        if list(orign_net.edges.data('weight'))[i][2] < q:
            return_net.remove_edge(*Edge[i])
    return return_net

# get weakly connected components
def weaklycc(network):
<<<<<<< HEAD
<<<<<<< HEAD
    """Short summary.
    Generate weakly connected cluster distribution

    Parameters
    ----------
    network : Graph()

    Returns
    -------
    type list

    """
    return [len(c) for c in sorted(nx.weakly_connected_components(network), key=len, reverse=True)]

# measuring GCC, SCC, CPoint, and generating graph
def criticalGraph(day,Period,edgelist,speedlist0,speedlist1):
    """Short summary.
    calculate critical q point when second giant connected component was max.
    Parameters
    ----------
    day : string
        ex) '10' input data's day
    Period : string
        ex) '08:00-08:02' time period
    edgelist : np.array(dtype=[('Link', 'int'), ('Node_Start', 'int'), ('Longitude_Start', 'float'),
        ('Latitude_Start', 'float'),('Node_End', 'int'), ('Longitude_End', 'float'),('Latitude_End', 'float'),('LENGTH', 'float')])
    speedlist0 : np.array(dtype=[('Period','U12'),('Link','int'),('Speed','float')])
    speedlist1 : np.array(dtype=[('Period','U12'),('Link','int'),('Speed','float')])

    Returns
    -------
    type
        fgure.png
    """
=======
=======
>>>>>>> graph module
    return [len(c) for c in sorted(nx.weakly_connected_components(network), key=len, reverse=True)]

# measuring GCC, SCC, CPoint, and generating graph
def criticalGraph(Period,edgelist,speedlist0,speedlist1):
<<<<<<< HEAD
>>>>>>> graph module
=======
>>>>>>> graph module
    # relative velocity
    rv = relativeVelocity(Period,speedlist0,speedlist1)
    # get GCC, SCC each q
    h = 101
    cc = np.zeros([2,h])
    # control parameter q
    q,a = np.linspace(0,1,h),0
    for i in q:
        dist=weaklycc(remove_qRoad(i,edgelist,rv))
        cc[0,a] = dist[0]
        if len(dist)>=2:cc[1,a]=dist[1]
        a+=1
    # get critical point(SCC max size)
    criticalPoint=q[np.where(cc[1]==max(cc[1]))][0]
    # Graph
    fig, ax1 = plt.subplots(figsize=(12,9))
    ax2 = ax1.twinx()
    curve1 = ax1.errorbar(q,cc[0]/1902,marker='s',markersize=20,label='GCC')
    curve2 = ax2.errorbar(q,cc[1]/1902,marker='^',markersize=20,label='SCC',c='orange')
    curves=[curve1,curve2]
    ax1.legend(curves,[curve.get_label()for curve in curves],fontsize='x-large')
<<<<<<< HEAD
<<<<<<< HEAD
    plt.savefig('Chengdu_june{}_{}_ciritcalpoint_{}.png'.format(day,Period,criticalPoint),transparent=True,dpi=300)
    plt.close()

# log binning
def logBinning(dist,base):
    """Short summary.
    Generate logbinning histogram array tuple.

    Parameters
    ----------
    dist : list
        ex) clsuter size distribution
    base : int
        ex) log_{base}
    Returns
    -------
    type
        Description of returned object.

    """
    # histogram
    maximum=int(math.log(dist[0],base))+1
    hist=np.zeros(maximum)
    # add cluster size each range
    for x in dist:
        hist[int(math.log(x,base))]+=1
    # generate x axis
    x_hist=np.zeros(maximum)
    for i in range(maximum):
        x_hist[i]=(base**(i+1)+base**(i))*0.5
    # divide by range
    for i in range(maximum):
        hist[i]/=(base**(i+1)-base**i)
    return x_hist,hist
=======
    plt.savefig('Chengdu_june1_{}_ciritcalpoint_{}.png'.format(Period,criticalPoint),transparent=True,dpi=300)
    plt.close()
>>>>>>> graph module
=======
    plt.savefig('Chengdu_june1_{}_ciritcalpoint_{}.png'.format(Period,criticalPoint),transparent=True,dpi=300)
    plt.close()
>>>>>>> graph module
