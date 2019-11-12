#lib.__init__.py
import numpy as np
from .taxipoint import point
import datetime as dt
from .plot import *

        
dtype = [('id', 'i4'), ('x', 'i4'), ('y', 'i4'), ('time', np.uint32),
        ('vel', 'i4'), ('psg', np.bool), ('district', 'i4')]

univ = point(37.5825764944, 127.0599900508)
#functions
timestamp = lambda timestr: int(dt.datetime.strptime(timestr,"%Y%m%d%H%M%S").timestamp()/10)
    
rotate1 = np.array([[np.cos(-univ.y*np.pi/180),-np.sin(-univ.y*np.pi/180),0],
    [np.sin(-univ.y*np.pi/180),np.cos(-univ.y*np.pi/180),0],[0,0,1]])
rotate2 = np.array([[np.cos(-univ.x*np.pi/180),0,-np.sin(-univ.x*np.pi/180)],
    [0,1,0],[np.sin(-univ.x*np.pi/180),0,np.cos(-univ.x*np.pi/180)]])
#functions
rotate = lambda vector: rotate2.dot(rotate1.dot(vector.T))
    
    
def carte(lat, lon):  
    lat, lon = lat*np.pi/180,lon*np.pi/180
    c = np.cos(lat)
    return np.array([c*np.cos(lon), c*np.sin(lon), np.sin(lat)])
    
def mapping(key, opt = None):
    if type(key) == point:
        return np.array(6371e3*rotate(carte(key.x, key.y))[1:],dtype=np.int32)
    if opt:
        return np.array(6371e3*rotate(carte(key, opt))[1:],dtype=np.int32)
    
linetoarray = lambda x,y,line:np.array([(line[0],x,y,timestamp(line[4]),int(line[6]),int(line[-2]),line[-1])],dtype= dtype)


def logical_and(*args):
    """the extension of np logical_and.

    :*args: TODO
    :returns: TODO

    """
    assert len(args) >=2, "argument length must be greater than 1."
    temp = np.logical_and(args[0],args[1])
    if len(args) ==2:
        return temp
    for i in args:
        temp = np.logical_and(temp,i)
    return temp

def logical_or(*args):
    """the extension of np logical_or.

    :*args: TODO
    :returns: TODO

    """
    assert len(args) >=2, "argument length must be greater than 1."
    temp = np.logical_and(args[0],args[1])
    if len(args) ==2:
        return temp
    for i in args:
        temp = np.logical_or(temp,i)
    return temp
