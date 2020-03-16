from .core.object import DataProcessor
from .rawfiles import rawfiles
import pyproj
import numpy as np

def RAW_to_hdf(hdf_filename, RAW_path, date):
    processor = DataProcessor()
    processor.load(RAW = RAW_path)
    processor.set_date(date[0],date[1],date[2])
    processor.RAWtohdf(hdf_filename)



def npy_to_hdf(hdf_filename, npy):
    """Test.

    Parameters
    ----------
    hdf_filename : ``string``
        Description of parameter `hdf_filename`.
    npy : type
        Description of parameter `npy`.

    Returns
    -------
    type
        Description of returned object.


    # NOTE: this is making note

    ..note::
        This is also making note
    """
    pass

def UTM(dataX,dataY):
    """
    convert to UTM coord from WGS84 coord

    input longitude, latitude WGS84 coordinate
    return longitude, latitude UTM coordinate
    """
    KoreaZone = 52
    p = pyproj.Proj(proj = 'utm', zone = '52N', ellps='WGS84')
    dataX, dataY = p(dataX, dataY,dtype=np.float32)
    return dataX,dataY  # XCoord, YCoord
