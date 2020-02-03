import numpy as np
import h5py
import networkx as nx
import datetime as dt
import matplotlib.pyplot as plt
import os
from ..rawfiles import rawfiles
import logging


__all__ = ['taxiarray', 'triparray', 'Dataset'] ## triparray == od_data(id, origin, destination) .npy => .hdf5

logging.basicConfig(format='%(asctime)s %(name)-10s : [%(levelname)-8s] %(message)s')


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
    def __init__(self, file):
        self.file = FileManager()
        self.file.load_h5py(file)
        self.date = self.file.date
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
        '''equivalent to taxiarray.range()'''
        pass

    def snapshot(self, time, target = 'point'):
        '''this method will make snapshot of data.
        you can set target of snapshot as network, point, etc.
        default is point.'''
        pass

    def __getitems__(self,  key):
        pass



class DataProcessor:
    '''controll whole type of files, keep file IO to save or read new things.'''

    def __init__(self, log_level = logging.DEBUG):
        '''if you set date FileManager class will check date of data default is None'''
        self.hdf = None
        self._npy = None
        self.npydtype = None
        self.RAW = None
        self.shp = None
        self._date = None
        self.logger = logging.getLogger('DataProcessor')
        self.logger.setLevel(log_level)
        self.logger.addHandler(logging.FileHandler('processing.log'))
        #DataProcessor.counts += 1


    def date():
        doc = "The date is usual information of whole data, we will seperate timestamp with date part and 'hms' part."
        def fget(self):
            if self._date is None:
                if self.hdf.attrs.get('Date', False):
                    self._date = self.hdf.attrs['Date']
            return dt.datetime.fromtimestamp(self._date*86400+54000).date()
        return locals()
    date = property(**date())

    def set_date(self, year, month, day):
        date = dt.datetime(year, month, day)
        self._date = int(date.timestamp()-54000)/86400

    def load(self, hdf = None, npy = None, RAW = None, shp = None):
        if hdf is not None:
            self.hdf = h5py.File(hdf, 'r+')
            self.logger.info("'{}' file loaded by hdf5 handler".format(hdf))
        if npy is not None:
            self.set_npy(npy)
            self.logger.info("'{}' file loaded by numpy handler".format(npy))
        if RAW is not None:
            self.set_RAW_path(RAW)
            self.logger.info("'{}' folder loaded by RAW handler".format(RAW))
        if shp is not None:
            pass

    def set_hdf(self, file):
        self.hdf = h5py.File(file)

    def set_RAW_path(self, path):
        if rawfiles(path).file_check():
            self.RAW = rawfiles(path)
        else:
            raise FileNotFoundError("RAW file doesn't exist")

    def set_npy(self, file, dtype = None):
        '''In previous work, we provide data with numpy binary file(.npy),
        So, this class will take that data to make new format to analyze.'''
        if os.path.isfile(file):
            self.npy = file
            if dtype is None:
                self.npydtype = np.load(file).dtype
            else:
                self.npydtype = dtype
        else:
            np.load(file)

    def set_shp(self, file):
        '''to make new network, there needs some GIS data for node and link,
        Generally, many institude provide above with shape file(.shp).
        so this class will parse that information so that automatically
        consist network. Using that network, one can easily mapping data
        into arbitrary network which is useful to analyze through SM.'''
        pass

    def npytohdf(self, path = None):
        if self.npy is None:
            raise ValueError("No .npy file")
        if self.hdf is None:
            self.set_hdf(path)



    def RAWtohdf(self, path = None):
        if self.RAW is None:
            self.logger.error('Attempt to make hdf before setting RAW file.')
            raise ValueError("No RAW files.")
        if self.hdf is None:
            self.set_hdf(path) # self.hdf = h5py.File(file)
        if self._date == None:
            self.logger.error('Attempt to make hdf before setting date.')
            raise ValueError("'date' is None.")

        self.logger.info('Starting process converting RAW to hdf5.')

        if not self.hdf.get('id_list',False):
            self.hdf.create_dataset('id_list',(1,), maxshape=(None,), dtype = np.int32)
            self.hdf.create_dataset('TimeTable',(8640,1000), maxshape=(8640,None), dtype = np.int32)
            self.logger.info('hdf handler start to initializing')
            self.hdf.attrs['Date'] = self._date
            self.logger.info('Collecting id.')
            ids = self.RAW.col_unique(0)
            ids.sort()
            self.logger.info('Saving id_list')
            self.hdf['id_list'].resize((len(ids),))
            self.hdf['id_list'][:] = ids

            self.logger.debug('Time table resize')
            self.hdf['TimeTable'].resize((8640,len(ids)))

        taxidata = self.hdf.require_group('taxidata')
        #errors = self.hdf.require_group('Errors')
        remains = self.hdf.require_group('remains')
        for i, typename in enumerate(self.RAW.dtype.names):
            if typename == 'id' or typename =='time':continue
            if not taxidata.get(typename, False):
                self.logger.debug("'{}' Dataset created.".format(typename))
                ta = taxidata.create_dataset(typename, (1,), maxshape=(None,), dtype = self.RAW.dtype[i], compression='gzip')
                #ta.attrs['Nonesign'] = -1
                #errors.create_dataset(typename, (1,), maxshape=(None,), dtype = self.RAW.dtype[i], compression='gzip')
                re = remains.create_dataset(typename, (1,), maxshape=(None,), dtype = self.RAW.dtype[i], compression='gzip')
                #ta.attrs['Nonesign'] = -1

        ids = self.hdf['id_list'][:]
        id_list = dict()
        for i,j in enumerate(ids):
            id_list[j] = i

        files = 0
        lines = 0
        id_count = 0
        #err_c = 0
        rem_c = 0
        timetable = -np.ones([8640,len(id_list)], dtype = np.int32)

        date = self._date*86400 + 54000
        totalfile = len(self.RAW)
        self.logger.debug('total file : {}'.format(totalfile))
        full = np.empty([int(4e8)],dtype = self.RAW.dtype)
        check = 0

        for npy in self.RAW.to_npy():
            self.logger.debug('File \t{} ({}/{}) '.format(files+1,files+1, totalfile))

            #self.logger.debug('\tCurrent total taxi number : {}'.format(len(id_list)))

            self.logger.debug('\tSorting npy')
            np.sort(npy, order=['time','id'])
            full[check:check+npy.shape[0]] = npy
            check += npy.shape[0]
            files +=1
        self.logger.debug('total : {}'.format(check))
        full = full[:check]

        self.logger.debug('Time converting')
        times = ((time_converter(full['time']) - (self._date*86400+54000))/10).astype(np.int32)

        self.logger.debug('Masking start')
        mask = np.logical_and(times>=0, times<8640)

        self.logger.debug('id converting')
        ids = [id_list[i] for i in full['id'][mask]]
        datalen = len(ids)

        self.logger.debug('Time table update')
        timetable[times[mask], ids] = lines+i

        self.logger.debug('Data collecting')
        for types in npy.dtype.names:
            if types == 'id' or types =='time':continue
            self.logger.debug('\t\t{}'.format(types))
            taxidata[types].resize((datalen,))
            taxidata[types][lines:] = full[types][mask]
            remains[types].resize((rem_c+full.shape[0]-datalen,))
            remains[types][rem_c:] = full[types][np.logical_not(mask)]

        #files+=1
        #lines+=datalen
        #rem_c+= len(npy)-datalen
        self.logger.debug('total files length : {}, data : {}. remains : {}'.format(len(npy), datalen, len(npy)-datalen))

        self.logger.info('Saving time table.')
        self.hdf['TimeTable'] = timetable
        self.hdf.attrs['TotalNumber'] = len(id_list)
        self.logger.info('Finished!')
        self.hdf.flush()




    def extract(self, arg):
        pass

    def read(self, arg):
        pass

class HDFManager:
    """HDFManager for certain data structure."""

    def __init__(self, file):
        self.file = h5py.File(file, 'r+')
        self._initialized = True if self.file.attrs.get(date,False) else False
        self.taxidata = self.file.require_group('Taxidata')
        self.errors = self.file.require_group('Errors')
        self.remains = self.file.require_group('Remains')
        #self.shp = self.file.require_group('shp')
        #self.trip = self.file.require_group('trip')

    def __getitem__(self, arg):
        if arg =='errors':
            pass
        if arg == 'remains':
            pass

        pass

    def field(self, arg):
        return self.file['taxidata'][arg]

    def a_get(self, arg):
        return self.file.attrs[arg]

    def a_set(self, name, val):
        self.file.attrs[name] = val





@np.vectorize
def time_converter(strtime):
    return dt.datetime.strptime(strtime.decode(), '%Y%m%d%H%M%S').timestamp()


if __name__ == '__main__':
    b = dt.datetime(1900,1,1)
    a = dt.datetime.strptime('121212',"%H%M%S")
    t = np.array(['20190515234512'],dtype='S14')
    test = h5py.File('test.hdf5')
    test.create_dataset('test', (8640,20000), maxshape = (8640,None))
    test['test'].resize([8640,10000])
    test['test'][0,:] = np.arange(10000)
    test['test'][0,3000:]
    logging.error('test')
    logging.warning('hi')
    a = logging.getLogger('test')
    a = logging.getLogger().getChild('test')
    np.arange(100,200).reshape(10,10)[[3,2,1],np.array([2,3,4])]
    a = h5py.File('test.hdf5')
    a['test'].resize((8640,200))
    a['test'][[1,2,3,4,5,6,7,8]]
    a['test'][1]
    a.setLevel(logging.INFO)
    a.info('ho')
    logging.info('test')
    rlog = logging.getLogger()
    a = np.zeros([1],dtype =[('id','i4'), ('x','u4')])
    a.dtype
    for i in a.dtype.fields:
        print(a.dtype.fields[i])
    dt.timedelta(123).total_seconds()
    dt.datetime.strptime('121212',"%H%M%S")
    t[0][-6:]
    dt.datetime(2015,5,8).timestamp()/86400
    # IDEA: timestamp of date of module 'datetime' is consist of (integer of day) * 86400(seconds/oneday) + 54000(IDK what it is)
    dt.datetime.fromtimestamp(16560*86400+54000)
    86400*0.625
    54000/3600
    1<<31
    17751966
