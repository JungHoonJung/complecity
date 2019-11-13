import numpy as np
import h5py
import networkx as nx
import datetime as dt
import matplotlib.pyplot as plt
import os
import ..rawfiles

__all__ = ['taxiarray', 'triparray', 'Dataset']

class taxiarray(np.ndarray):
    '''pratical data container based on structured array of numoy.
    traditionally, data type is '['id', 'x','y','time','passenger']'.
    please check datatype.'''

    def iterate_with(self, type='id'):
        '''other iteration method for ussefulness.
        iterative taxi array given.'''
        pass

    def plot(self, id='all', time ='all'):
        '''plot this data on seoul map.'''
        pass

    def range(self, **range):
        '''indexing with field and its range.
        for example,
        taxiarray.range(
            x = (xstart, xend),
            y = (ystart, yend),
            time = (tstart, tend)
        )
        will return index array.
        if there is no name in dtype field, it raise nameerror.
        '''
        pass

    def mapping(self, mapper):
        pass

    def split(self, arg):
        pass

class triparray(taxiarray):
    """this array is specific data types for taxi data.
    a component of triparray is consist of two taxiarray components.
    so we call one of them to origin and the other as destination.
    to manage that property, we provide trajectory and,
    length or some other method for trip."""

    def __init__(self,  arg, dataset = None):
        super(triparray, self).__init__()
        self.arg = arg
        if dataset is not None:
            self.dataset = dataset

    def origins():
        doc = "origin is start point of trip. this property gives origin points as taxiarray form."
        def fget(self): # IDEA: return origin points of this instance as taxi array
            return taxidata(_origins)
        return locals()
    origins = property(**origins())

    def destination():
        doc = "destination is end point of trip. this this property gives origin points as taxiarray form."
        def fget(self):
            return self._destination
        def fset(self, value):
            self._destination = value
        def fdel(self):
            del self._destination
        return locals()
    destination = property(**destination())


    def trajectory(self, index):
        '''it will give i-th trip's trajectory from original dataset. return is taxiarray.'''
        pass

    def plot(self, arg):
        raise NotImplementedError

    def range(self, arg):
        pass

class Dataset:
    '''this class will take FileManager and read from file make many objects of processing data.
    so that you can get taxi object or network object easily with this class. '''
    def __init__(self, file = None):
        if files is not None:
            self.open(file)
        self._scope = None


    def open(self, file):
        '''open hdf5 file to load data.'''
        self.filesystem = h5py.File(file, 'r+')

    def set_scope(self, **scope):
        '''if you want specific data, you can customizing scope of data.
        after setting scope class will automatically limit the data within scope.
        for now, it only for geometric.
        the definition of scope follow below.'''
        if self._scope is None:
            print(None)
            return
        pass

    def show_scope(self):
        '''if you set scope before, then this method will make geometric scope,
        and time.'''
        pass

    def range(self, **range):
        '''equivalent to taxiarray.range()''''
        pass

    def snapshot(self, time, target = 'point'):
        '''this method will make snapshot of data.
        you can set target of snapshot as network, point, etc.
        default is point.'''
        pass

    def __getitems__(self,  key):
        pass



class FileManager:
    '''controll whole type of files, keep file IO to save or read new things.'''
    def __init__(self, date = None):
        '''if you set date FileManager class will check date of data default is None'''
        self.date = date
        self.hdf = None
        self.npy = None
        self.RAW = None
        self.shp = None

    def create_h5py(self, file):
        self.hdf = h5py.File(file, 'w')

    def load_h5py(self, file):
        self.hdf = h5py.File(file, 'r+')

    def set_RAW_path(self, path):
        if rawfiles(path).checkfiles():
            self.RAW = rawfiles(path)
        else:
            raise FileExistsError("RAW file doesn't exist")

    def set_npy(self, file):
        '''In previous work, we provide data with numpy binary file(.npy),
        So, this class will take that data to make new format to analyze.'''
        pass

    def set_shp(self, file):
        '''to make new network, there needs some GIS data for node and link,
        Generally, many institude provide above with shape file(.shp).
        so this class will parse that information so that automatically
        consist network. Using that network, one can easily mapping data
        into arbitrary network which is useful to analyze through SM.'''
        pass

    def extract(self, arg):
        pass

    def read(self, arg):
        pass
