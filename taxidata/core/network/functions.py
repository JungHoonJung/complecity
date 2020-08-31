import pyproj
import numpy as np

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

def seg_check(grid_set, seg_set):
    """check formaer gird if it in later grid set.
    =======
    """Short summary.

    Parameters
    ----------
    grid_set : np.ndarray
        grid set of trajectory
    seg_set : np.ndarray
        grid set of segment

    Returns
    -------
    bool
        Return True when segment grid in trajectory return False other

    """
    return np.in1d(seg_set, grid_set,assume_unique=True).all()

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
