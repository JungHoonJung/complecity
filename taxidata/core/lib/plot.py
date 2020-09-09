import matplotlib.pyplot as plt
import pkg_resources
import numpy as np
from ast import literal_eval
from .taxipoint import point
from ..network.functions import toUTM

__all__ = ['district', 'plot_seoul']


district_file = pkg_resources.resource_stream(__name__,"district.DAT")
raw_district_file = pkg_resources.resource_filename(__name__,"TL_SCCO_SIG_W.gml")
dist_position = []#dist_pos
dist_name = []#fname
dist_id = []#fid



class dist:
    id = []
    name = []
    position = []

    def __init__(self):
        self.index = None
        self.__pos = ('lat', 'lon')

    def __call__(self, key):
        '''In old version, plot some district or seoul is somehow hard.
            So, Here is Solution. Only need is typing name or
            id or number of order. then this instance will give you proper things.'''
        try:
            key = int(key)
        except:
            for n in dist.name:
                if key in n:
                    ret = dist.name.index(n)
                    return self.set(ret)
            raise KeyError('Wrong input')
        ret = dist.id.index(key)
        return self.set(ret)

    def __repr__(self):
        return "<district object set as {}({})>".format(dist.id[self.index],dist.name[self.index])

    def __getitem__(self, key):
        return self.set(key)

    def get_list(self):
        di = {}
        for i,j in zip(dist.id, dist.name):
            di[j]=i
        return di
    
    @property
    def pos(self):
        return self.__pos
    @pos.getter
    def pos(self):
        return np.array([self.x, self.y]).T


    def set(self, key):
        if self.index == key:
            return self
        if key>=25:
            raise KeyError("Out of range.")
        self.index = key
        self.id = dist.id[self.index]
        self.name = dist.name[self.index]
        self.y, self.x = self.position[key].T
        self.x, self.y = toUTM(self.x, self.y)
        return self

    def plot(self, *arg, **kwarg):
        plt.plot(self.x, self.y, *arg,**kwarg)
    
    def raycast(self, points):
        xmin = self.x.min()
        ymin = self.y.min()
        xmax = self.x.max()
        ymax = self.y.max()

        if not isinstance(points, np.ndarray):
            points = np.array(points)
        if len(points.shape) == 1:
            points.reshape([-1,2])
        mask = ((points.T[0] - xmin)*(points.T[0]-xmax)<0) & ((points.T[1] - ymin)*(points.T[1]-ymax)<0)
        cand = points[mask]
        chnb = np.zeros([cand.shape[0]], dtype = np.int32)
        for i in range(len(self.x)-1):
            if self.x[i] <self.x[i+1]: # set l1x is always lower than l2x
                l1x = self.x[i]
                l2x = self.x[i+1]
                l1y = self.y[i]
                l2y = self.y[i+1]
            else:
                l1x = self.x[i+1]
                l2x = self.x[i]
                l1y = self.y[i+1]
                l2y = self.y[i]

            masky = ((cand.T[1] - l1y)*(cand.T[1] - l2y)<0) # check y range
            candp = cand[masky]
            chnbp = np.zeros(candp.shape[0],dtype= np.int32)

            maskx = (candp.T[0] -  l1x)<=0               # check points left side of box
            chnbp[maskx] += 1
            
            maskx = ~maskx&((candp.T[0] -  l2x)<=0)
            if maskx.any():
                d_ang = np.arctan2(l2y-l1y,l2x-l1x)
                p_ang = np.arctan2(candp.T[1][maskx]-l1y,candp.T[0][maskx]-l1x)
                chnbp[maskx] += ((abs(p_ang)-abs(d_ang))>0).astype(np.int32)
            chnb[masky] += chnbp
        mask = np.asarray(mask)
        mask[mask] = (mask[mask]& ((chnb%2).astype(np.bool)))
        return mask



        


district = dist()

with open(raw_district_file, encoding="utf8") as f:
    sig_cd      = []
    sig_kor_nm  = []
    sig_eng_nm  = []
    posList     = []
    ch          = False
    for line in f:
        if line[:12] == r'<fme:SIG_CD>':
            sig_cd.append(int(line[12:].split("<")[0]))
        if line[:16] == r'<fme:SIG_KOR_NM>':
            sig_kor_nm.append((line[16:].split("<")[0]))
        if line[:16] == r'<fme:SIG_ENG_NM>':
            sig_eng_nm.append((line[16:].split("<")[0]))
            ch = True
        if ch and line[:13] == r"<gml:posList>":
            posList.append(np.array((line[13:].split("<")[0]).split()).reshape([-1,2]).astype(np.float32))
            ch = False

dist.id = sig_cd
dist.name = sig_kor_nm
dist.position = posList

"""for i in range(25):
    dist.id.append(int(district_file.readline().decode()))
    dist.name.append(district_file.readline().decode("utf-8").split()[0])
    position = district_file.readline().decode().split()
    dpos = []
    for pos in position:
        #print(pos.split(","))
        dpos.append(point(pos.split(","), ctype = int))
    dist.position.append(dpos)
"""
dist_max = max([len(comp) for comp in dist.position])
seoul = np.zeros([dist_max,25,2])

for i in range(dist_max):
    for j in range(25):
        try:
            seoul[i][j] = np.array([dist.position[j][i].x,dist.position[j][i].y])
        except:
            seoul[i][j] = np.array([None,None])
seoul_X = seoul[:,:,0]
seoul_Y = seoul[:,:,1]

#plot = lambda taxi,*arg,**kwarg: plt.scatter(taxi['x'],taxi['y'],*arg,**kwarg) #move to taxidata/core/object.py

def plot_seoul(*arg,**kwarg):
    plt.plot(seoul_X, seoul_Y,*arg,**kwarg)
