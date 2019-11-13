import numpy as np
import h5py
import networkx as nx
import datetime as dt
import matplotlib.pyplot as plt
import os
import ..rawfiles


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



class Dataset:
    '''this class will take FileManager and read from file make many objects of processing data.
    so that you can get taxi object or network object easily with this class. '''
    def __init__(self, files):
        self.filesystem = files
        self._scope = None
        pass

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
