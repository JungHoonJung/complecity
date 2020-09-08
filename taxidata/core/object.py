import numpy as np
import h5py
import networkx as nx
from .network import functions
import datetime as dt
import matplotlib.pyplot as plt
import os
from ..rawfiles import rawfiles
import logging
from .lib.plot import plot_seoul

__all__ = ['taxiarray', 'triparray', 'Dataset','trajectory'] ## triparray == od_data(id, origin, destination) .npy => .hdf5

logging.basicConfig(format='%(asctime)s %(name)-10s : [%(levelname)-8s] %(message)s')

class taxiarray(np.ndarray):
    '''pratical data container based on structured array of numoy.
    traditionally, data type is '['id', 'x','y','time','passenger']'.
    please check datatype.'''

    def pos():
        doc = """position of taxi.

        Returns
        -------
        np.ndarray
            in taxiarray, return np.array([x_array ,y_array])

        """
        def fget(self):
            return np.array([self[self._posx],self[self._posy]]).T
        def fset(self, value):
            self._posx = value[0]
            self._posy = value[1]
        def fdel(self):
            return
        return locals()
    pos = property(**pos())

    def taxi_id():
        doc = """id of taxi.

                Returns
                -------
                np.index_array
                    in taxiarray, return np.array([id_array])

                """
        def fget(self):
            return [id for id,_ in self._taxi_id]
        def fset(self, index_array):
            self._taxi_id = index_array
        def fdel(self):
            del self._taxi_id
        return locals()
    taxi_id = property(**taxi_id())


    def iterate_with(self, type='id'):
        '''other iteration method for usefulness.
        iterator of given taxi array.
        *only id for now*'''
        i = 0
        for taxi_id, index in self._taxi_id:
            temp = self[i:index]
            temp.pos = (self._posx, self._posy)
            yield taxi_id, temp
            i = index

    def plot(self, id='all', time ='all'):
        """Short summary.

        Parameters
        ----------
        id : list
            id of taxi.
        time : tuple
            time set (start,end).

        Returns
        -------
        plt.figure

            plot taxi in time set


        """
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




class trajectory(taxiarray):
    '''a set of continuous point of single taxi. time gap may be 10 seconds.
    interaction with segment, other trajectories. map matching.
    '''
    def taxi_id():

        doc ="""The taxi_id property.

                Returns
                -------
                np.index_array
                    in taxiarray, return np.array([id_array])
                """
        def fget(self):
            return self._taxi_id
        def fset(self, value):
            self._taxi_id = value
        def fdel(self):
            del self._taxi_id
        return locals()
    taxi_id = property(**taxi_id())


    def get_trajectories(self):
        """return trajectories list by taxi_id.

        Returns
        -------
        np.ndarray
            in taxiarray, return np.array([trajectory_array])

        """
        t = []
        for taxi_id, array in self.iterate_with('id'):
            taxi = array.view(trajectory)
            taxi.taxi_id = taxi_id
            t.append(taxi)
        return t

    def distance_of_curve(self, i, segment):
        """return max distance between trajectory point and segment

        Parameters
        ----------
        i : `int`
            index of trajectory
        segment : list
            list of segment-points

        Returns
        -------
        'float'
            max distance between trajectory point and segment

        """
        d_p = []
        d_v = functions.distance(segment, self[i])

        for k in segment:
            d_p.append(functions.distance(self, k))

        max_d_p = np.max(d_p)
        d_curve = max(d_v, max_d_p)
        return d_curve

    def trajectory_grid(self, point=False):
        """Return grid trajectory.

        Parameters
        ----------
        point : bool
            If calculate not a trajetory but a point, set True.

        Returns
        -------
        np.ndarray
            Array of trajectory grids

        """
        l = []
        if point:
            l.append(int(self[0]//200-1234 + (self[1]//200-20400)*734))
        else:
            for j in self:
                l.append(int(j[0]//200-1234 + (j[1]//200-20400)*734))
        return np.unique(l)

    def grid_set(self, point=False):
        """grid set surrounding the trajectory.

        Parameters
        ----------
        point : bool
            If calculate not a trajetory but a point, set True.

        Returns
        -------
        np.ndarray
            Array of trajectory grid sets.

        """
        tot = []

        if point:
            i = trajectory.trajectory_grid(self, point=True)
            grid_list = [i+733, i+734, i+735,\
                         i-1,   i,     i+1,  \
                         i-735, i-734, i-733]
            for j in grid_list:
                tot += [j]
        else:
            grid_raw = trajectory.trajectory_grid(self)
            for i in grid_raw:
                 grid_list = [i+733, i+734, i+735,\
                              i-1,   i,     i+1,  \
                              i-735, i-734, i-733]
                 for j in grid_list:
                    tot += [j]
        return np.unique(tot)

class triparray(taxiarray):
    """

        Parameters
        ----------
        arg : type
            Description of parameter `arg`.
        dataset : type
            Description of parameter `dataset`.

        Returns
        -------
        type
            Description of returned object.

        this array is specific data types for taxi data.
        a component of triparray is consist of two taxiarray components.
        so we call one of them to origin and the other as destination.
        to manage that property, we provide trajectory and,
        length or some other method for trip.

        """

    """"""


    def __init__(self,  arg, dataset = None):

        super(triparray, self).__init__()
        self.arg = arg
        if dataset is not None:
            self.dataset = dataset

    def origins():
        doc = """origin is start point of trip. this property gives origin points as taxiarray form.

        Returns
        -------
        tdarray
            origin points as taxiarray form

        """

        def fget(self): # IDEA: return origin points of this instance as taxi array
            return array(self._origins)
        return locals()
    origins = property(**origins())

    def destination():
        doc = "destination is end point of trip. this property gives origin points as taxiarray form."
        def fget(self):
            return self._destination
        def fset(self, value):
            self._destination = value
        def fdel(self):
            del self._destination
        return locals()
    destination = property(**destination())


    def trajectory(self, index):
        '''it will give i-th trip's trajectory from original dataset. return is trajectory.'''
        pass

    def plot(self, arg):
        raise NotImplementedError

    def range(self, arg):
        pass




class Dataset:
    '''this class will take FileManager and read from file make many objects of processing data.
    so that you can get taxi object or network object easily with this class. '''

    dtype_presets = {'lat':'f8','lon':'f8','time':'i8','id':'i4', 'x':'i4','y':'i4','psg':'?','ang':'i4','valid':'?','vel':'i4','z':'i4'}

    def __init__(self, file):
        self.file = file
        self.targets = None
        self._id_list = None
        with h5py.File(self.file, 'r') as f:
            self.date = dt.datetime.fromtimestamp(f.attrs['Date']*86400+54000)

    def open(self):
        """open h5py file

        Returns
        -------
        type
            Description of returned object.

        """
        self.h5py = h5py.File(self.file,'r')

    def close(self):
        self.h5py.close()
        del self.h5py

    def id_list():

        doc ="""id list of saved taxi

                Returns
                -------
                array
                    array([id of taxies]).

                """
        def fget(self):
            if self._id_list is None:
                with h5py.File(self.file, 'r') as f:
                    self._id_list = f['id_list'][:]
            return self._id_list
        return locals()
    id_list = property(**id_list())

    def fields():

        doc ="""return fields of saved taxis array.

                Returns
                -------
                list
                    list[fields]

                """
        def fget(self):
            with h5py.File(self.file, 'r') as f:
                return [field for field in f['taxidata']]
        return locals()
    fields = property(**fields())

    def get_array(self, target = None, start_time = None, end_time = None, **kwarg):
        '''return array from file.  

        start_time and end_time specify the output data size.
        if integer is given, each argument will be regarded as hours
        or time must be instance of datetime module.

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

        date : bool  
            if True, timestamp of date will be added.

        dtype : list of (field_name, dtype)  
            set return dtypes.
            if None, return whole field and saved dtypes.
        fields : list  
            set return fields.
            if None, return whole field
        position : tuple of str (field_name_of_x, field_name_of_y)  
            specify position default is ('lon','lat')
        '''
        set_taxis   = False
        fields      = None
        dtypes      = None
        fd_ol       = False
        start       = None
        end         = None
        position    = ('lon','lat')

        if target is not None:
            self.set_taxi_id(target)

        for key in kwarg:
            if key == 'num':
                if not kwarg.get('random',True):
                    self.set_taxis(kwarg['num'],kwarg['random'])
                else:
                    self.set_taxis(kwarg['num'])
                set_taxis = True
            if key == 'time':
                start_time = kwarg[key][0]
                end_time = kwarg[key][1]
            if key == 'fields':
                fields = kwarg['fields']
                dtypes = [(key, self.dtype_presets[key]) for key in fields]
                if fd_ol:
                    raise KeyError("fields and dtypes cannot be mentioned together.")
                fd_ol = True
            if key == 'dtypes':
                dtypes = kwarg[key]
                fields = []
                for dtype in dtypes:
                    fields.append(dtype[0])
                if fd_ol:
                    raise KeyError("fields and dtypes cannot be mentioned together.")
                fd_ol = True
            if key == 'position':
                position = kwarg['position']

        if fields is None:
            fields = self.fields
            fields.insert(0,'time')
            fields.insert(0,'id')
            dtypes = [(key,self.dtype_presets[key]) for key in fields]

        else:
            if not 'time' in fields:
                dtypes.insert(0,('time',self.dtype_presets['time']))

            if not 'id' in fields:
                dtypes.insert(0,('id',self.dtype_presets['id']))


        if self.targets is None:
            self.targets = self.id_list



        if isinstance(start_time,dt.datetime):
            if self.date == start_time.date:
                start_time = start_time.time()
        if isinstance(start_time,dt.time):
            start = start_time.hour*360+start_time.minute*6+start_time.second//10
        elif isinstance(start_time, int):
            start = start_time*360

        if isinstance(end_time,dt.datetime):
            if self.date == end_time.date:
                end_time = end_time.time()
        if isinstance(end_time,dt.time):
            end = end_time.hour*360+end_time.minute*6+end_time.second//10
        elif isinstance(end_time, int):
            end = end_time*360


        time = slice(start, end)
        ids = {ii:i for i, ii in enumerate(self.id_list)}
        target = [ids[taxiid] for taxiid in self.targets]
        target.sort()
        indices = []
        nums = []
        times = []

        date = self.date.timestamp()

        #timetable loads
        if len(self.targets)<=50:
            with h5py.File(self.file, 'r') as f:
                timetable = f['TimeTable'][:].T
        else:
            with h5py.File(self.file, 'r') as f:
                timetable = {}
                for i in target:
                    timetable[i] = f['TimeTable'][:,i]



        # partial reading is optimal when len(target) < 1000
        #reading data indices from timetable
        for i in target:
            mask = timetable[i][time]
            taxi = mask[mask != -1]

            if taxi.shape[0] == 0:
                continue

            tlist = np.arange(8640)[time][mask != -1]*10
            if kwarg.get('date',False):
                tlist+= date*86400+54000
            times.append(tlist)
            indices.append(taxi)
            nums.append(taxi.shape[0])
        
        
        
        if not nums:
            raise ValueError("Data is Empty. Please check the data range.")
        else:
            print(f"{len(nums)} taxis founded in data with given condition.")
        #print(dtypes) ## check

        Array = np.zeros(sum(nums),dtype = dtypes)
        cumnum = np.array(nums).cumsum()
        order = np.empty([cumnum[-1],2],dtype = np.int32)
        order[:,1] = np.arange(cumnum[-1])
        number = 0
        for index in indices:
            order[:,0][number:number + len(index)] = index
            number += len(index)
        ind_min = order[:,0].min()
        ind_max = order[:,0].max()
        #order = np.sort(order, 0)

        ch_len = 0
        order[:,0] -= ind_min

        with h5py.File(self.file, 'r') as f:
            for field, _ in dtypes:
                if field == 'id' or field == 'time':continue
                Array[field] = f['taxidata'][field][ind_min:ind_max+1][order.T[0]]

            for start_index, dlen, taxi_id, tlist, index in zip(cumnum, nums, self.targets, times, indices):
                tarr = Array[start_index-dlen: start_index]
                ch_len+=dlen
                tarr['id'] = taxi_id
                tarr['time'] = tlist

        assert ch_len == cumnum[-1]

        res = Array.view(taxiarray)
        if 'lat' in fields:
            res['lat']/=1e7
        if 'lon' in fields:
            res['lon']/=1e7
        res.pos = position
        res.taxi_id = [(id, index) for id, index in zip(self.targets, cumnum)]
        self.targets = None
        return res


    def set_taxis(self, num, random = True):
        '''setting number of taxis to extract.
        if random is False, the order is same as id_list.'''
        if random:
            self.targets = np.random.choice(self.id_list, num, replace = False)
        else:
            self.targets = self.id_list[:num]


    def set_taxi_id(self, ids):
        """setting target with given id.

        Parameters
        ----------
        ids : list of integer
            list of ids that you want to extract from hdf5



        """
        self.targets = ids
    def get_target_id(self):
        """ return current targetted ids

        Returns
        -------
        list
            [id of taxies]

        """

        return self.targets
    def set_scope(self, **scope):
        """Short summary.

        Parameters
        ----------
        **scope : type
            Description of parameter `**scope`.

        Returns
        -------
        type
            Description of returned object.

        """
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

    def __len__(self):
        with h5py.File(self.file, 'r') as f:
             return f['taxidata']['valid'].shape[0]


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
        date = dt.datetime(int(year), int(month), int(day))
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
            self.hdf = h5py.File(path, 'w') # self.hdf = h5py.File(file)
            self.hdf.attrs['Date'] = self._date
        if self._date == None:
            self.logger.error('Attempt to make hdf before setting date.')
            raise ValueError("'date' is None.")

        self.logger.info('Starting process converting RAW to hdf5.')



        taxidata = self.hdf.require_group('taxidata')
        remains = self.hdf.require_group('remains')

        files = 0
        lines = 0
        id_count = 0
        rem_c = 0

        date = self._date*86400 + 54000
        totalfile = len(self.RAW)
        self.logger.debug('total file : {}'.format(totalfile))
        full = np.empty([int(4e8)],dtype = self.RAW.dtype)
        check = 0

        for npy in self.RAW.to_npy():
            self.logger.debug('File \t{} ({}/{}) '.format(files+1,files+1, totalfile))

            #self.logger.debug('\tCurrent total taxi number : {}'.format(len(id_list)))

            #self.logger.debug('\tSorting npy')
            np.sort(npy, order=['time','id'])
            full[check:check+npy.shape[0]] = npy
            check += npy.shape[0]
            files +=1
        self.logger.debug('total : {}'.format(check))
        full = full[:check]


        self.logger.info('Collecting id.')

        ids = np.unique(full['id'])
        timetable = -np.ones([8640,len(ids)], dtype = np.int32)

        self.logger.info('Saving id_list')
        self.hdf.create_dataset('id_list', data = ids)
        #ids.sort()
        id_list = dict()
        for i,j in enumerate(ids):
            id_list[j] = i

        self.logger.debug('Time converting')
        times = ((time_converter(full['time']) - (self._date*86400+54000))/10).astype(np.int32)

        self.logger.debug('Masking start')
        mask = np.logical_and(times>=0, times<8640)
        tdata = full[mask]
        rdata = full[np.logical_not(mask)]

        self.logger.debug('id converting')
        ids = [id_list[i] for i in tdata['id']]
        datalen = len(ids)

        self.logger.debug('Time table update')
        timetable[times[mask], ids] = np.arange(len(ids))
        self.logger.debug('Time table collecting')
        self.hdf.create_dataset('TimeTable', data = timetable, compression = 'gzip')


        self.logger.debug('Data collecting')
        for i, typename in enumerate(self.RAW.dtype.names):
            if typename == 'id' or typename =='time':continue
            if not taxidata.get(typename, False):
                self.logger.debug("\t'{}' Dataset created.".format(typename))
                ta = taxidata.create_dataset(typename, data = tdata[typename], compression='gzip')

                #ta.attrs['Nonesign'] = -1
                #errors.create_dataset(typename, (1,), maxshape=(None,), dtype = self.RAW.dtype[i], compression='gzip')
                re = remains.create_dataset(typename, data = rdata[typename], compression='gzip')
        r'''
        for types in npy.dtype.names:
            if types == 'id' or types =='time':continue
            self.logger.debug('\t\t{}'.format(types))
            taxidata[types].resize((datalen,))
            taxidata[types][:] = tdata[types]
            remains[types].resize((full.shape[0]-datalen,))
            remains[types][:] = rdata[types]
        '''
        #files+=1
        #lines+=datalen
        #rem_c+= len(npy)-datalen
        self.logger.debug('total files length : {}, data : {}. remains : {}'.format(len(tdata), datalen, len(rdata)))
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

def array(*arg, **kwarg):
    x = np.array(*arg, **kwarg)
    x = x.view(taxiarray)
    x.pos = ([],[])
    x.taxi_id = []
    return x

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
