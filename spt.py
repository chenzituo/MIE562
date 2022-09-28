import numpy as np
import pandas as pd

def construct(x):
    global g
    g[x[0]-1,x[1]-1] = 1
    return 0
def release(x, rnumber):
    global queue, record
    for k in range(len(x)):
        y = -1
        for i,j in enumerate(queue[rnumber[k]]):
            if j == x[k]:
                y = i
                break
        if y != -1:
            del queue[rnumber[k]][y]
        # pop x[k] in queue[rnumber[k]]
        record[x[k]] = makespan
        # record start time
    return 0
def victim():
    global g
    for i in range(n):
        if makespan == (record[i] + p[i]):
            g[i,:] = np.zeros(n)
            # delete x[k]'s sons' father x[k]
    return 0
def generate():
    global bl, rtime, makespan
    time = [x for i,x in enumerate(rtime) if bl[i]]
    makespan = min(time)
    victim()
    # count events starts at time point: makespan
    notes = []
    iss = []
    for i in range(r):
        bl[i] = 0 # at this time point, no work will be start
        if makespan >= rtime[i]:
            # resource constraint
            temp = [j for j in queue[i] if max(g[:,j]) == 0] # now roots
            if len(temp) > 0:# exist roots in resource i
                pt = [p[j] for j in temp]
                note = temp[np.argmin(pt)]
                # SPT - shortest processing time
                rtime[i] = makespan + p[note]
                bl[i] = 1
                notes.append(note)
                iss.append(i)
        else:
            bl[i] = 1
    if len(notes) > 0:
        release(notes, iss)
    return 0
n = 9
p = [15, 50, 60, 50, 50, 15, 30, 15, 20]
r = 3
res = [0, 1, 2, 1, 0, 2, 0, 1, 2]
queue = {}
for i in range(r):
    queue[i] = [j for j,x in enumerate(res) if x == i]
g = np.zeros([n, n])
m = 6
pairs = [[1,2],[2,3],[4,5],[5,6],[7,8],[8,9]]
for x in pairs:
    construct(x)
makespan = 0
bl = np.ones(r) 
rtime = np.zeros(r)
record = - np.ones(n)
while True:
    generate()
    det = 0
    for i in range(r):
        det = max(det, len(queue[i]))
    if not det:
        break
endt = record + p
print('Sj = ', record)
print('Cmax = {:.0f}'.format(max(endt)))