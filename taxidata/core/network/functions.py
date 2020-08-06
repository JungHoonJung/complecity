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
