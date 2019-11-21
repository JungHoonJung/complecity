import numpy as np
import os

class rawfiles:
    '''Cause number of taxi data file is ~600, it is almost linux file open limit.
       So, there needs more efficient controller for I/O file handler.
       This class share its file handler so that only class has files, not instance.
       So, you don`t need to check file is opened.
       Also, you can`t take control files keep open. Be careful to use this instance'''

    '''Last one is actually useless. so, this class contain only path of file.'''

    time = []
    h,m,s = 0,0,0
    while True:
        time.append("%02d%02d%02d"%(h,m,s)+".DAT")
        m += 2
        s += 30
        if s == 60:
            m+=1
            s=0
        if m == 60:
            m=0
            h += 1
        if (h == 24): break
    #raw='/'
    dtype = np.dtype({'names':('id','lat','lon','z','time','ang','vel','valid','psg'),
            'formats' :('u4','u4','u4','i4','S14','i4','i4','?','?') })

    def __init__(self, folder_path, dtype = None ,opt = 'r'):
        if type(folder_path)==str:
            self.path = [os.path.join(folder_path,t) for t in self.time]
        if type(folder_path)==list:
            self.path = folder_path

        self.opt = opt
        self.closed = True
        self.index = 0
        self._index = 0
        self.file = None
        self.valid = False
        if dtype is None:
            self.dtype = rawfiles.dtype
        else:
            self.dtype = dtype

    def __repr__(self):
        return "<I/O files handler from : %s, to : %s>\n"%(self.path[0],self.path[-1])

    def file_check(self):
        self.isfiles = []
        for path in self.path:
            valid = True
            try:
                with open(path) as f:
                    if not f.readable():
                        valid = False
            except:
                valid = False

            self.isfiles.append(valid)
        valid = True
        for v in self.isfiles:
            valid = valid and v
        self.valid = valid
        return valid

    def to_npy(self, index = None):
        if self.dtype is None:
            raise TypeError
        if index == None:
            for file in self.path:
                yield np.loadtxt(file, dtype = self.dtype, delimiter=',')
        else:
            return np.loadtxt(self.path[index], dtype = self.dtype)

    def col_unique(self, index):
        res = {}
        dtype = self.dtype[index]
        for file in self.path:
            for item in np.loadtxt(file, dtype = dtype, delimiter=',', usecols=(index,)):
                res[item] = 0

        return list(res.keys())

    def __iter__(self):
        self._index = 0
        valid = False

        if self.valid:
            valid = self.valid
        else:
            valid = self.file_check()

        if valid:
            return self
        else:
            raise FileExistsError("file doesn`t exists or not valid")


    def __next__(self):
        if self._index<len(self.path):
            self._index+=1
            return open(self.path[self._index-1], self.opt)
        else:
            raise StopIteration

    def __len__(self):
        return len(self.path)

    def __getitem__(self, key):
        return open(self.path[key],self.opt)
