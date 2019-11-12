# taxipoint.py
# coding: utf-8


import math
#import matplotlib.pyplot as plt
#import pkg_resources
import numpy as np
#from ast import literal_eval

'''
#data_file = pkg_resources.resource_stream(__name__,"TL_SCCO_SIG_W.gml")
district = pkg_resources.resource_stream(__name__,"district.DAT")
#a =  data_file
'''
'''
cd = 'SIG_CD'
name = 'SIG_KOR_NM'
pos = 'gml:posList'


cdch = False
namech = False
ex = []
for line in a:
    line = str(line)
    if cd in line:
        ex.append(line)
        cdch = True
    if cdch:
        if name in line:
            ex.append(line)
            cdch = False
            namech = True
    if namech:
        if pos in line:
            ex.append(line)
            namech = False

sig_id = ex[0::3]
sig_name = ex[1::3]
sig_pos = ex[2::3]


fid = []
fname =[]
fpos = []
for comp1, comp2, comp3 in zip(sig_id,sig_name,sig_pos):
    fid.append(comp1[14:19])
    fname.append(comp2[comp2.find('>')+1:comp2.find('<',comp2.find('>'))])
    fpos.append(comp3[comp3.find('>')+1:comp3.find('<',comp3.find('>'))])


for i in range(25):
    fid[i] = int(fid[i])
'''
########## class ##########            
class point:
    '''point class is take 2 argument or length 2 object
    they must be integer or float, 
    if not some calculation will be error.
    So, if you want convert input type, than ctype can be type of class'''
    
    '''dist_position = []#dist_pos
    dist_name = []#fname
    dist_id = []#fid
    seoul_X = []
    seoul_Y = []
    ###########plotting method##########
    def district_X(index):
        X = []
        for comp in point.dist_position[index]:
            X.append(comp.x)
        return X
    
    def district_Y(index):
        X = []
        for comp in point.dist_position[index]:
            X.append(comp.y)
        return X
    
    def seoul():
        return plt.plot(point.seoul_X,point.seoul_Y)
    
    def district(index):
        return plt.plot(point.district_X(index),point.district_Y(index))
        '''
    
    
    def __init__(self, x, y= None, ctype = None):
        if y is not None:
            self.x = x
            self.y = y
            return
        if len(x) == 2:
            if ctype is None:
                self.x = x[0]
                self.y = x[1]
            else:
                self.x = ctype(x[0])
                self.y = ctype(x[1])
        
        
    
    def atX(self, other, target_y):
        try:
            c  = (self.x - other.x)*(target_y-other.y)/(self.y-other.y) + other.x
        except ZeroDivisionError as e:
            print(self, other)
            c = -999999999999
        return c
    
    
    def __del__(self):
        del self.x, self.y
    
    
    
    def distance(self, other):
        R = 6371
        if type(other) != type(self):
            raise TypeError(str(type(other))+"is not class point")
        dlon = self.x - other.x
        dlat = self.y - other.y
        dlon = dlat * (math.pi/180)
        dlat = dlon * (math.pi/180)
        a = math.sin(dlat/2) * math.sin(dlat/2) +  math.cos(self.x*(math.pi)/180) * math.cos(other.x*(math.pi)/180) *math.sin(dlon/2) * math.sin(dlon/2)
     
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        d = R * c
        return d
    
    def __repr__(self):
        return "({}, {})".format(self.x, self.y)
    
    def __add__(self, other):
        return (point(self.x+other.x,self.y+other.y))
    
    def __sub__(self, other):
        return (point(self.x-other.x,self.y-other.y))
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    #def plot(self, detail = False):
    #    if detail and self.dist_i:
    #        plt.plot([i.x for i in self.dist_position[self.dist_i] ],[i.y for i in self.dist_position[self.dist_i] ])
    #        plt.scatter(self.x, self.y, linewidths=2, c = 'r')
    #        return
    #    else:
    #        for a in range(25):
    #        #plt.figure()
    #            plt.plot([i.x for i in self.dist_position[a] ],[i.y for i in self.dist_position[a] ])
    #            plt.scatter(self.x, self.y, linewidths=2, c = 'r')
        






'''
dist_pos = []
i = 0
temp =None
for raw in fpos:
    district = []
    i = 0
    for comp in raw.split():
        pos = float(comp)
        i+=1
        if i%2:
            temp = pos
            continue
        if temp<20 or pos <100 :
            continue
        
        district.append(pre_point(temp,pos))
    dist_pos.append(district)



class point(pre_point):
    #global dist_pos, fname, fid
    
    
    
    
    #def classify(self, res = False):
    #    dist = 0 
    #    test ={}
    #    for i in range(len(self.dist_position)):
    #        entry = len([i])
    #        crosses = 0pos.split()
    #        temp = None
    #        for pos in self.dist_position[i]:
    #            if temp is None:
    #                temp = pos
    #                continue
    #            if (self.y>pos.y) ^ (self.y>temp.y):
    #                if self.x < pos.atX(temp,self.y):
    #                    crosses += 1
    #                    #print(pos.x,temp.x)
    #            temp = pos
    #     dist_position = []#dist_pos
    dist_name = []#fname
    dist_id = []#fid
    seoul_X = []
    seoul_Y = []
    ###########plotting method##########
    def district_X(index):
        X = []
        for comp in point.dist_position[index]:
            X.append(comp.x)
        return X
    
    def district_Y(index):
        X = []
        for comp in point.dist_position[index]:
            X.append(comp.y)
        return X
    
    def seoul():
        return plt.plot(point.seoul_X,point.seoul_Y)
    
    def district(index):
        return plt.plot(point.district_X(index),point.district_Y(index))   if crosses%2:
    #            test[i] = (crosses, pos, temp)
    #            self.dist_i = i
    #            self.dist = 'name : %s, sig_cd : %d'%(self.dist_name[self.dist_i], self.dist_id[self.dist_i])
    #            if res:
    #                print(self.dist)
    #            return self.dist_id[i]
    #    return
            
    #def print_dist(self):
    #    return self.dist#print(pos.split(","))
    
    def plot(self, detail = False):
        if detail and self.dist_i:
            plt.plot([i.x for i in self.dist_position[self.dist_i] ],[i.y for i in self.dist_position[self.dist_i] ])
            plt.scatter(self.x, self.y, linewidths=2, c = 'r')
            return
        else:
            for a in range(25):
            #plt.figure()
                plt.plot([i.x for i in self.dist_position[a] ],[i.y for i in self.dist_position[a] ])
                plt.scatter(self.x, self.y, linewidths=2, c = 'r')
'''
'''

for i in range(25):
    point.dist_id.append(int(district.readline().decode()))
    point.dist_name.append(district.readline().decode("utf-8").split()[0])
    position = district.readline().decode().split()
    dpos = []
    for pos in position:
        #print(pos.split(","))
        dpos.append(point(pos.split(","), ctype = int))
    point.dist_position.append(dpos)

dist_max = max([len(comp) for comp in point.dist_position])
seoul = np.zeros([dist_max,25,2])

for i in range(dist_max):
    for j in range(25):
        try:
            seoul[i][j] = np.array([point.dist_position[j][i].x,point.dist_position[j][i].y])
        except:
            seoul[i][j] = np.array([None,None])
point.seoul_X = seoul[:,:,0]
point.seoul_Y = seoul[:,:,1]

    
    

def plot_seoul(po=None):
    for a in range(25):
        #plt.figure()
        plt.plot([i.y for i in point.dist_position[a] ],[i.x for i in point.dist_position[a] ])
        if po is not None:
            plt.scatter(po.y,po.x, linewidths=2, c = 'r')

'''