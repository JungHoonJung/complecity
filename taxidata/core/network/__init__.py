import numpy as np
import networkx as nx
import os
import re
import matplotlib.pyplot as plt
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> since problem6
=======
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> add docstring
=======
>>>>>>> add docstring
>>>>>>> since 11
=======
>>>>>>> last..
=======
>>>>>>> add docstring
=======
>>>>>>> add docstring
=======
>>>>>>> rebase
import math

<<<<<<< HEAD
<<<<<<< HEAD
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
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
=======
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> since_problem
=======
=======
=======
>>>>>>> graph module
=======
>>>>>>> since_problem2
=======
>>>>>>> add network docstring
=======
>>>>>>> rebase
>>>>>>> since_problem
<<<<<<< HEAD
=======
>>>>>>> rebase2

<<<<<<< HEAD
>>>>>>> rebase
=======
=======
>>>>>>> to rebase

<<<<<<< HEAD
>>>>>>> last..
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
<<<<<<< HEAD
=======
# edgelist data convert to npy
def convert2npy_edgelist(path,filename):
    """Short summary.
    Chengdu road linklist's raw data is csv format. This function convert to npy format.
>>>>>>> since_problem3
=======
>>>>>>> last..

# generate Street network
def genStreetNet(Edgelist):
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> graph module
=======
    """Short summary.
=======
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
>>>>>>> Adding 'raw csv data' conver to npy format.
=======
=======
>>>>>>> last..
>>>>>>> since_problem

    Parameters
    ----------
    Path : string ex) '/home/dataset'
        path of raw csv data

    Returns
    -------
    type speed[monthDay]_[1or0].npy
        np.array(dtype=[('Period','U12'),('Link','int'),('Speed','float')])

    """
<<<<<<< HEAD
>>>>>>> docstring test
=======
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
=======
# edgelist data convert to npy
def convert2npy_edgelist(path,filename):
    """
    Chengdu road linklist's raw data is csv format. This function convert to npy format.
<<<<<<< HEAD
>>>>>>> to rebase
=======
=======
>>>>>>> rebase
=======

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
<<<<<<< HEAD
>>>>>>> last..
<<<<<<< HEAD
>>>>>>> last..
=======
=======
>>>>>>> rebase
>>>>>>> rebase

# generate Street network
def genStreetNet(Edgelist):
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> Adding 'raw csv data' conver to npy format.
=======
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
>>>>>>> add network docstring
=======
>>>>>>> graph module
>>>>>>> rebase
=======
=======
>>>>>>> since_problem
=======
>>>>>>> since_problem2
=======
>>>>>>> last..
=======
>>>>>>> rebase2
=======
>>>>>>> since_problem
=======
>>>>>>> since_problem2
=======
>>>>>>> rebase2
>>>>>>> graph module
<<<<<<< HEAD
<<<<<<< HEAD
=======
=======
>>>>>>> rebase2
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
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> since_problem3
>>>>>>> docstring test
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> rebase2
=======
=======
>>>>>>> graph module
<<<<<<< HEAD
>>>>>>> since_problem
=======
=======
>>>>>>> docstring test
<<<<<<< HEAD
>>>>>>> since_problem2
=======
=======
>>>>>>> since_problem3
=======
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
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> Adding 'raw csv data' conver to npy format.
<<<<<<< HEAD
>>>>>>> since_problem3
=======
=======
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
>>>>>>> add network docstring
>>>>>>> since_problem4
=======
>>>>>>> last..
=======
=======
>>>>>>> graph module
>>>>>>> since_problem
=======
>>>>>>> since_problem2
=======
>>>>>>> Adding 'raw csv data' conver to npy format.
<<<<<<< HEAD
>>>>>>> since_problem3
=======
=======
>>>>>>> docstring test
>>>>>>> last..
<<<<<<< HEAD
>>>>>>> last..
=======
=======
>>>>>>> add network docstring
>>>>>>> add network docstring
=======
>>>>>>> rebase
=======
>>>>>>> docstring test
>>>>>>> rebase2
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
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> add network docstring
=======
>>>>>>> rebase
=======
>>>>>>> since_problem
=======
=======
>>>>>>> add network docstring
>>>>>>> since_problem4
=======
>>>>>>> last..
=======
=======
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> since_problem
>>>>>>> since_problem
=======
>>>>>>> since_problem2
=======
>>>>>>> rebase
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
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> since_problem4
=======
>>>>>>> graph module
=======
>>>>>>> add network docstring
=======
=======
>>>>>>> graph module
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> rebase
=======
=======
>>>>>>> graph module
=======
>>>>>>> since_problem2
>>>>>>> since_problem
=======
=======
>>>>>>> add network docstring
>>>>>>> since_problem4
=======
>>>>>>> last..
=======
=======
=======
>>>>>>> graph module
=======
>>>>>>> graph module
>>>>>>> since_problem
=======
>>>>>>> last..
=======
>>>>>>> add network docstring
=======
>>>>>>> rebase
>>>>>>> since_problem
=======
>>>>>>> last..
=======
>>>>>>> add network docstring
=======
=======
>>>>>>> graph module
>>>>>>> rebase
    # assign pos for nodes
    return {i:[Edgelist[Edgelist['Node_Start']==i]['Longitude_Start'][0],Edgelist[Edgelist['Node_Start']==i]['Latitude_Start'][0]]for i in range(len(np.unique(Edgelist['Node_Start'])))}

# get max velocity each street link
def Max_velocity(velocity0,velocity1):
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> add network docstring
=======
>>>>>>> rebase
=======
>>>>>>> since_problem
=======
=======
>>>>>>> add network docstring
>>>>>>> since_problem4
=======
>>>>>>> last..
=======
=======
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> since_problem
>>>>>>> since_problem
=======
>>>>>>> since_problem2
=======
>>>>>>> rebase
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
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> since_problem4
=======
>>>>>>> graph module
=======
>>>>>>> add network docstring
=======
=======
>>>>>>> graph module
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> rebase
=======
=======
>>>>>>> last..
=======
>>>>>>> graph module
>>>>>>> since_problem
=======
<<<<<<< HEAD
=======
>>>>>>> add network docstring
>>>>>>> since_problem4
=======
>>>>>>> last..
=======
=======
=======
>>>>>>> since_problem2
=======
>>>>>>> rebase
=======
>>>>>>> graph module
=======
>>>>>>> add network docstring
=======
>>>>>>> graph module
>>>>>>> since_problem
>>>>>>> since_problem
=======
>>>>>>> last..
<<<<<<< HEAD
>>>>>>> last..
=======
=======
>>>>>>> add network docstring
>>>>>>> add network docstring
=======
=======
>>>>>>> graph module
>>>>>>> rebase
    max_velo = np.zeros(len(np.unique(velocity0['Link'])))
    for i in range(len(max_velo)):
        max_velo[i] = max([max(velocity0[velocity0['Link'] == i+1]['Speed']),max(velocity1[velocity1['Link'] == i+1]['Speed'])])
    return max_velo

# get relative velocity
def relativeVelocity(Period,velocity0,velocity1):
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> rebase2
=======
>>>>>>> add network docstring
=======
=======
>>>>>>> rebase
=======
>>>>>>> since_problem3
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> add network docstring
=======
>>>>>>> rebase
=======
>>>>>>> rebase2
=======
>>>>>>> since_problem
=======
>>>>>>> since_problem2
=======
>>>>>>> since_problem3
=======
=======
>>>>>>> add network docstring
>>>>>>> since_problem4
=======
>>>>>>> last..
=======
<<<<<<< HEAD
>>>>>>> to rebase
=======
>>>>>>> to rebase
=======
=======
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> since_problem
>>>>>>> since_problem
=======
>>>>>>> since_problem2
=======
>>>>>>> since_problem3
>>>>>>> since_problem3
=======
>>>>>>> add network docstring
>>>>>>> add network docstring
=======
>>>>>>> rebase
=======
>>>>>>> rebase2
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


<<<<<<< HEAD
    """
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> since_problem4
=======
>>>>>>> graph module
=======
=======
>>>>>>> docstring test
=======
>>>>>>> last..
=======
# get relative velocity
def relativeVelocity(Period,velocity0,velocity1):
>>>>>>> since_problem4
=======
=======
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> last..
>>>>>>> last..
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
<<<<<<< HEAD
>>>>>>> docstring test
<<<<<<< HEAD
=======
>>>>>>> Adding 'raw csv data' conver to npy format.
=======
>>>>>>> add network docstring
=======
=======
>>>>>>> graph module
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> rebase
=======
=======
=======
>>>>>>> to rebase
=======
=======
>>>>>>> rebase2
>>>>>>> rebase2
=======
>>>>>>> since_problem2
=======
<<<<<<< HEAD
>>>>>>> add network docstring
=======
>>>>>>> rebase
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
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> rebase2
=======
=======
>>>>>>> graph module
>>>>>>> since_problem
=======
=======
>>>>>>> docstring test
<<<<<<< HEAD
>>>>>>> since_problem2
=======
=======
>>>>>>> Adding 'raw csv data' conver to npy format.
<<<<<<< HEAD
>>>>>>> since_problem3
=======
=======
>>>>>>> add network docstring
>>>>>>> since_problem4
=======
>>>>>>> last..
=======
>>>>>>> rebase
>>>>>>> to rebase
=======
=======
>>>>>>> since_problem2
>>>>>>> rebase
>>>>>>> since_problem
>>>>>>> since_problem
=======
=======
>>>>>>> since_problem4
>>>>>>> rebase
>>>>>>> since_problem
>>>>>>> since_problem3
>>>>>>> since_problem3
=======
>>>>>>> rebase
>>>>>>> since_problem
>>>>>>> since_problem3
=======
>>>>>>> last..
<<<<<<< HEAD
>>>>>>> last..
=======
=======
>>>>>>> add network docstring
>>>>>>> add network docstring
=======
=======
>>>>>>> graph module
<<<<<<< HEAD
>>>>>>> rebase
=======
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
>>>>>>> rebase2
    return np.array(velocity0[velocity0['Period']==Period]['Speed']/Max_velocity(velocity0,velocity1))

# generate network given weight by relative speed
def genStreetNet_speed(Edgelist,reVelo):
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> since problem6
=======
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> add docstring
=======
>>>>>>> add docstring
>>>>>>> since 11
=======
>>>>>>> add docstring
=======
>>>>>>> add docstring
=======
>>>>>>> rebase
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
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> since_problem
=======
>>>>>>> add docstring
>>>>>>> since problem6
=======
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> graph module
=======
>>>>>>> graph module
=======
>>>>>>> add docstring
=======
>>>>>>> add docstring
>>>>>>> since 11
=======
>>>>>>> last..
=======
>>>>>>> add docstring
=======
>>>>>>> add docstring
=======
=======
>>>>>>> graph module
>>>>>>> rebase
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
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
=======
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> since 11
=======
>>>>>>> add docstring
=======
>>>>>>> add docstring

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
<<<<<<< HEAD
<<<<<<< HEAD
=======
# remove link under parameter q
def remove_qRoad(q,Edgelist,reVelo):
>>>>>>> graph module
>>>>>>> since_problem
=======
=======
>>>>>>> last..
=======
>>>>>>> rebase

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
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> add docstring
=======
>>>>>>> add docstring
>>>>>>> since problem6
=======
>>>>>>> last..
=======
>>>>>>> add docstring
=======
>>>>>>> add docstring
=======
=======
# remove link under parameter q
def remove_qRoad(q,Edgelist,reVelo):
>>>>>>> graph module
>>>>>>> rebase
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
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> since problem6
=======
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> add docstring
=======
>>>>>>> add docstring
>>>>>>> since 11
=======
>>>>>>> last..
=======
>>>>>>> add docstring
=======
>>>>>>> add docstring
=======
>>>>>>> rebase
    """Short summary.
    Generate weakly connected cluster distribution

    Parameters
    ----------
    network : Graph()

    Returns
    -------
    type list

    """
<<<<<<< HEAD
<<<<<<< HEAD
    return [len(c) for c in sorted(nx.weakly_connected_components(network), key=len, reverse=True)]

# measuring GCC, SCC, CPoint, and generating graph
<<<<<<< HEAD
<<<<<<< HEAD
def criticalGraph(day,Period,edgelist,speedlist0,speedlist1):
<<<<<<< HEAD
=======
def criticalGraph(Period,edgelist,speedlist0,speedlist1):
>>>>>>> graph module
=======
def criticalGraph(day,Period,edgelist,speedlist0,speedlist1):
<<<<<<< HEAD
>>>>>>> Adding 'raw csv data' conver to npy format.
=======
=======
>>>>>>> add docstring
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
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> add docstring
=======
>>>>>>> add docstring
=======
=======
>>>>>>> since problem6
=======
=======
>>>>>>> graph module
=======
>>>>>>> add docstring
=======
>>>>>>> last..
=======
>>>>>>> to rebase
=======
>>>>>>> to rebase
=======
>>>>>>> to rebase
=======
=======
=======
=======
>>>>>>> graph module
=======
>>>>>>> since_problem2
>>>>>>> since_problem
=======
>>>>>>> since_problem4
=======
>>>>>>> since 11
=======
>>>>>>> last..
=======
>>>>>>> rebase
>>>>>>> since_problem
>>>>>>> since problem6
=======
<<<<<<< HEAD
=======
=======
>>>>>>> graph module
=======
>>>>>>> add docstring
>>>>>>> since 11
=======
>>>>>>> last..
=======
>>>>>>> add docstring
=======
>>>>>>> add docstring
=======
=======
>>>>>>> rebase
    return [len(c) for c in sorted(nx.weakly_connected_components(network), key=len, reverse=True)]

# measuring GCC, SCC, CPoint, and generating graph
def criticalGraph(Period,edgelist,speedlist0,speedlist1):
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> graph module
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> rebase
=======
=======
def criticalGraph(day,Period,edgelist,speedlist0,speedlist1):
<<<<<<< HEAD
>>>>>>> Adding 'raw csv data' conver to npy format.
<<<<<<< HEAD
>>>>>>> since_problem3
=======
=======
>>>>>>> add docstring
<<<<<<< HEAD
>>>>>>> since problem6
=======
=======
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
>>>>>>> add docstring
>>>>>>> since 11
=======
>>>>>>> last..
=======
=======
def criticalGraph(day,Period,edgelist,speedlist0,speedlist1):
>>>>>>> Adding 'raw csv data' conver to npy format.
>>>>>>> since_problem3
=======
>>>>>>> since_problem4
=======
=======
>>>>>>> add docstring
>>>>>>> since problem6
>>>>>>> since problem6
=======
=======
>>>>>>> add docstring
>>>>>>> since problem6
=======
=======
>>>>>>> graph module
=======
def criticalGraph(day,Period,edgelist,speedlist0,speedlist1):
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> Adding 'raw csv data' conver to npy format.
=======
>>>>>>> add docstring
=======
=======
>>>>>>> add docstring
=======
>>>>>>> add docstring
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
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> add docstring
>>>>>>> since 11
<<<<<<< HEAD
>>>>>>> since 11
=======
=======
>>>>>>> graph module
>>>>>>> last..
<<<<<<< HEAD
>>>>>>> last..
=======
=======
>>>>>>> add docstring
<<<<<<< HEAD
=======
=======
>>>>>>> add docstring
<<<<<<< HEAD
>>>>>>> add docstring
=======
=======
>>>>>>> graph module
>>>>>>> rebase
>>>>>>> rebase
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
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
    plt.savefig('Chengdu_june{}_{}_ciritcalpoint_{}.png'.format(day,Period,criticalPoint),transparent=True,dpi=300)
=======
    plt.savefig('Chengdu_june1_{}_ciritcalpoint_{}.png'.format(Period,criticalPoint),transparent=True,dpi=300)
>>>>>>> graph module
=======
=======
>>>>>>> rebase
=======
>>>>>>> since_problem
=======
>>>>>>> since_problem3
    plt.savefig('Chengdu_june{}_{}_ciritcalpoint_{}.png'.format(day,Period,criticalPoint),transparent=True,dpi=300)
>>>>>>> Adding 'raw csv data' conver to npy format.
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
<<<<<<< HEAD
=======
    plt.savefig('Chengdu_june1_{}_ciritcalpoint_{}.png'.format(Period,criticalPoint),transparent=True,dpi=300)
    plt.close()
>>>>>>> graph module
=======
    plt.savefig('Chengdu_june1_{}_ciritcalpoint_{}.png'.format(Period,criticalPoint),transparent=True,dpi=300)
=======
=======
>>>>>>> last..
=======
>>>>>>> to rebase
=======
=======
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> since_problem
>>>>>>> since_problem
=======
>>>>>>> since_problem2
=======
=======
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> since_problem3
>>>>>>> since_problem3
=======
>>>>>>> since_problem4
=======
>>>>>>> last..
=======
>>>>>>> rebase
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
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> since_problem
=======
<<<<<<< HEAD
=======
    plt.savefig('Chengdu_june1_{}_ciritcalpoint_{}.png'.format(Period,criticalPoint),transparent=True,dpi=300)
>>>>>>> since 11
    plt.close()
>>>>>>> graph module
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> since_problem3
>>>>>>> since problem6
=======
>>>>>>> graph module
=======
=======
<<<<<<< HEAD
=======
>>>>>>> rebase
    plt.savefig('Chengdu_june{}_{}_ciritcalpoint_{}.png'.format(day,Period,criticalPoint),transparent=True,dpi=300)
    plt.close()
>>>>>>> last..

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
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> add docstring
=======
>>>>>>> add docstring
>>>>>>> since 11
=======
>>>>>>> last..
=======
>>>>>>> add docstring
=======
>>>>>>> add docstring
=======
=======
    plt.savefig('Chengdu_june1_{}_ciritcalpoint_{}.png'.format(Period,criticalPoint),transparent=True,dpi=300)
    plt.close()
>>>>>>> graph module
>>>>>>> rebase
