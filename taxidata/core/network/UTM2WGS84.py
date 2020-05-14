import pyproj

def UTM2WGS84(dataX,dataY):
    """"
    convert from UTM coord to WGS84 coord
    
    input longitude, latitude UTM coordinate
    return longitude, latitude WGS84 coordinate
    """"
    KoreaZone = 52
    p = pyproj.Proj(proj = 'utm', zone = KoreaZone, ellps='WGS84')
    dataX, dataY = p(dataX, dataY, inverse = True,dtype=np.float32)
    return dataX,dataY  # lon, lat

SeoulWGS84 = UTM2WGS84(Seoul['XCoord'],Seoul['YCoord']) # conver to WGS84_lon,lat