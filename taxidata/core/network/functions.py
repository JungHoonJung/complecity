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
