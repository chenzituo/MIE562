import numpy as np
import pandas as pd

n = 14
p = [5, 6, 9, 12, 7,
     12, 10, 6, 10, 9,
     7, 8, 7, 5]
p = np.array(p)
relation_dic = np.array(pd.read_csv('./cpm.csv'))
depth = relation_dic.shape[0]
leaf = np.ones(n)
root = np.ones(n)
relation_mat = np.zeros([n, n])
for i in range(n):
    for head in range(depth):
        if not(np.isnan(relation_dic[head, i])):
            leaf[i] = 0
            root[int(relation_dic[head, i])-1] = 0
            relation_mat[i, int(relation_dic[head, i])-1 ] = 1
            print(i+1, '->', int(relation_dic[head, i]))
print(leaf)
print(root)
gcp = relation_mat.copy()
def remove(i):
    global gcp
    gcp[:,i] = np.zeros(n)
    gcp[i,:] = np.zeros(n)
print(gcp)
def achieve(head):
    t = 0
    if max(gcp[head]) == 0:
        if leaf[head] == 1:
            t = 1
    else:
        temp = 0
        for i in range(n):
            if gcp[head, i]:
                temp = max(temp, achieve(i))
        t = temp
    return t
minset = {}
count = 0
defi = np.ones((n+1)**3)
for i in range(n):
    if root[i] == 1:
        count += 1
        minset[count] = i+1
        defi[i+1] = 0
    elif leaf[i] == 1:
        count += 1
        minset[count] = i+1
        defi[i+1] = 0
def test1():
    global gcp, count
    for i in range(n):
        if defi[i+1]:
            remove(i)
            if not achieve(0):
                count += 1
                minset[count] = i+1
                defi[i] = 0
            gcp = relation_mat.copy()
test1()
def test2():
    global gcp, count
    for i in range(n):
        if defi[i+1]:
            for j in range(i+1, n):
                if defi[j+1]:
                    remove(i)
                    remove(j)
                    if not achieve(0):
                        count += 1
                        minset[count] = [i+1,j+1]
                        defi[(i+1)*(n+1)+(j+1)] = 0
                    gcp = relation_mat.copy()
test2()
def test3():
    global gcp, count
    for i in range(n):
        if defi[i+1]:
            for j in range(i+1, n):
                if defi[j+1] and defi[(i+1)*(n+1)+(j+1)]:
                    for k in range(j+1,n):
                        if defi[k+1] and defi[(i+1)*(n+1)+(k+1)] and defi[(j+1)*(n+1)+(k+1)]:
                            remove(i);remove(j);remove(k);
                            if not achieve(0):
                                count+=1
                                minset[count] = [i+1, j+1, k+1]
                                defi[(i+1)*n**2+(j+1)*n+(k+1)] = 0
                            gcp = relation_mat.copy()
test3()
print(minset)
    