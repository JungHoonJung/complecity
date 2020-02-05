import numpy as np
import matplotlib.pylab as plt
import math

# data
Seoul = np.load('./SeoulConvertEdgelist.npy')
# Seoul['EDGE'] = np.arange(len(Seoul)) # edge 라벨 재설정(방향이 다른 경우 같으 라벨링이 되어있어서)
node_Seoul = np.unique(Seoul['START_NODE']) # node 집합


def next_node(input):
    index_find = [k for k, x in enumerate(input[0]) if x == "+"][-1]
    next_edge = Seoul[np.where(Seoul['START_NODE']==int(input[0][(index_find+1):]))]
    a=[]
    for i in range(len(next_edge)):
        a.append(input)
    b=[]
    for n in range(len(next_edge)):
        turning_angle=0
        # measuring turning angle
        if input[0].count('+') >= 2:
            cal_turningAg = input[0].split('+')[1:]
            if len(cal_turningAg)>=2:
                X_1, Y_1 = Seoul[np.where(Seoul['START_NODE']==int(cal_turningAg[-2]))][0][0],Seoul[np.where(Seoul['START_NODE']==int(cal_turningAg[-2]))][0][1]
                X_2, Y_2 = Seoul[np.where(Seoul['START_NODE']==int(cal_turningAg[-1]))][0][0], Seoul[np.where(Seoul['START_NODE']==int(cal_turningAg[-1]))][0][1]
                X_3, Y_3 = Seoul[np.where(Seoul['START_NODE']==next_edge['END_NODE'][n])][0][0], Seoul[np.where(Seoul['START_NODE']==next_edge['END_NODE'][n])][0][1]
                turning_angle = math.asin(((X_2-X_1)*(Y_3-Y_2)-(Y_2-Y_1)*(X_3-X_2))/(((X_2-X_1)**2+(Y_2-Y_1)**2)*((X_3-X_2)**2+(Y_3-Y_2)**2))**0.5)
        b.append([a[n][0] + "+" + str(next_edge['END_NODE'][n]), a[n][1] + next_edge['LENGTH'][n],a[n][2]+turning_angle])
    return b

def node_cycle(input):
    output=[]
    for i in range(len(input)):
        output = output + next_node(input[i])
    return output

# k
k = 800
segment = []

for SN in node_Seoul: # input Seoul node
#[+node+node+..., total_length, turning_angle]
    input=[["+" + str(SN), 0, 0]]
    count=0
    while count < 100 :
        input = node_cycle(input)
        pop_parameter=0
        # pop segment and add to segment list
        for i in range(len(input)):
            i-=pop_parameter
            # if path's length exceed k
            if input[i][-2]>k:
                segment.append(input[i])
                input.pop(i)
                pop_parameter+=1
            # if turning angle exceed 2pi
            elif abs(input[i][-1])>2*np.pi:
                segment.append(input[i])
                input.pop(i)
                pop_parameter+=1

        # if count%10==0:print(count)
        count += 1
        if len(input) == 0: break
