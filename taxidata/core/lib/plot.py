import matplotlib.pyplot as plt
import pkg_resources
import numpy as np
from ast import literal_eval
from .taxipoint import point


__all__ = ['district', 'plot_seoul','plot']


district_file = pkg_resources.resource_stream(__name__,"district.DAT")
dist_position = []#dist_pos
dist_name = []#fname
dist_id = []#fid



class dist:
    id = []
    name = []
    position = []

    def __init__(self):
        self.index = None

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

    def set(self, key):
        if self.index == key:
            return self
        if key>=25:
            raise KeyError("Out of range.")
        self.index = key
        self.id = dist.id[self.index]
        self.name = dist.name[self.index]
        self.x = [i.x for i in self.position[key]]
        self.y = [i.y for i in self.position[key]]
        return self

    def plot(self, *arg, **kwarg):
        plt.plot(self.x, self.y, *arg,**kwarg)

district = dist()

for i in range(25):
    dist.id.append(int(district_file.readline().decode()))
    dist.name.append(district_file.readline().decode("utf-8").split()[0])
    position = district_file.readline().decode().split()
    dpos = []
    for pos in position:
        #print(pos.split(","))
        dpos.append(point(pos.split(","), ctype = int))
    dist.position.append(dpos)

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

plot = lambda taxi,*arg,**kwarg: plt.scatter(taxi['x'],taxi['y'],*arg,**kwarg)

def plot_seoul(*arg,**kwarg):
    plt.plot(seoul_X, seoul_Y,*arg,**kwarg)
