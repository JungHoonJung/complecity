import numpy as np
import h5py
import networkx as nx
import datetime as dt
import matplotlib.pyplot as plt
import os
from ..rawfiles import rawfiles
import logging
from .lib.plot import plotseoul

__all__ = ['taxiarray', 'triparray', 'Dataset'] ## triparray == od_data(id, origin, destination) .npy => .hdf5

logging.basicConfig(format='%(asctime)s %(name)-10s : [%(levelname)-8s] %(message)s')


class taxiarray(np.ndarray):
    '''pratical data container based on structured array of numoy.
    traditionally, data type is '['id', 'x','y','time','passenger']'.
    please check datatype.'''


    @property
    def pos(self):
        return
    @pos.getter
    def pos(self):
        return self[self._posx],self[self._posy]
    @pos.setter
    def pos(self, value):
        self._posx = value[0]
        self._posy = value[1]

    @property
    def taxi_id(self):
        return self._taxi_id
    @taxi_id.setter
    def taxi_id(self, index_array):
        self._taxi_id = index_array
    @taxi_id.getter
    def taxi_id(self):
        return self._taxi_id

    def iterate_with(self, type='id'):
        '''other iteration method for usefulness.
        iterator of given taxi array.'''
        pass

    def plot(self, id='all', time ='all'):
        '''plot this data on seoul map.'''
        pass

    def range(self, **range):
        '''indexing with field and its range.
        for example,

        .. code-block::
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
        self.file = file
        with h5py.File(file, 'r') as f:
            self.date = dt.datetime.fromtimestamp(f.attrs['date']*86400+54000).date()

    def id_list():
        doc = "The id_list of saved taxis."
        def fget(self):
            if self._id_list is None:
                self._id_list = self.file['id_list'][:]
            return self._id_list
        return locals()
    id_list = property(**id_list())

    def fields():
        doc = "The id_list of saved taxis."
        def fget(self):
            return [field for field in self.file['taxidata']]
        return locals()
    fields = property(**fields())


    def get_array(target = None, start_time = None, end_time = None, **kwarg):
        '''return array from file.
        start_time and end_time specify the output data size.
        if integer is given, regard as hours
        or time instance of datetime module.

        if None, whole data will be returned.

        kwargs
        ---------
        num : integer
            total taxi number fixed as given integer.
            same option of Dataset.set_taxis(num, random)
        random : bool (optional)
            same option of Dataset.set_taxis(num, random)
            default is `True`.
        time : tuple
            set start_time and end_time

        dtype : np.dtype with field name
            set return dtypes.
            if None, return whole field and saved dtypes.
        fields : list
            set return fields.
            if None, return whole field
        position : str
            specify position default is latitude and longitude
        '''
        set_taxis = False
        fields = self.fields
        dtypes =
        for key in kwarg:
            if key == 'num':
                if kwarg.get('random',False):
                    self.set_taxis(kwarg['num'],kwarg['random'])
                else:
                    self.set_taxis(kwarg['num'])
                set_taxis = True
            if key == 'time':
                start_time = kwarg[key][0]
                end_time = kwarg[key][1]
            if key == 'fields':
                fields = kwarg['fields']
            if key == 'dtypes':
                dtypes = kwarg[key]


        if kwarg.get('num',False):
            if kwarg.get('random',False):
                self.set_taxis(kwarg['num'],kwarg['random'])
            else:
                self.set_taxis(kwarg['num'])
        if self.targets is None:
            raise TypeError("No taxi specified.")

        if kwarg.get('fields',False):

        else:
            fields = self.fields

        if target is not None:
            self.set_taxi_id(target)

        if isinstance(start_time,dt.datetime.datetime):
            if self.date == start_time.date:
                start_time = start_time.time()
        if isinstance(start_time,dt.datetime.time):
            start = start_time.hour*360+start_time.minute*6+start_time.second//10
        elif isinstance(start_time, int):
            start = start_time*360

        if isinstance(end_time,dt.datetime.datetime):
            if self.date == end_time.date:
                end_time = end_time.time()
        if isinstance(end_time,dt.datetime.time):
            end = end_time.hour*360+end_time.minute*6+end_time.second//10
        elif isinstance(end_time, int):
            end = end_time*360

        time = slice(start, end)

        timetable = self.file['TimeTable'][:]
        ids = {ii:i for i, ii in enumerate(self.id_list)}
        target = [ids[taxiid] for taxiid in self.targets]
        target.sort()
        indices = []
        #reading data indices from timetable
        for i in target:
            indices.append(timetable[i][time])
        array = np.array()



    def set_taxis(self, num, random = True):
        '''setting number of taxis to extract.
        if random is False, the order is same as id_list.'''
        if random:
            self.targets = np.random.choice(self.id_list, num, replace = False)
        else:
            self.targets = self.id_list[:num]

    def set_taxi_id(self, ids):
        '''ids = list of id. setting target with given id'''
        self.targets = ids

    def set_scope(self, **scope):
        '''if you want specific data, you can customizing scope of data.
        after setting scope class will automatically limit the data within scope.
        for now, it only for geometric.
        the definition of scope follow below.'''
        if self._scope is None:
            print(None)
            return
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
            self.hdf['id_list'].resize((len(id_list),))
            self.hdf['id_list'][:] = ids

            self.logger.debug('Time table resize')
            self.hdf['TimeTable'].resize((8640,len(id_list)))

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
