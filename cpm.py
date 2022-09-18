import numpy as np
import pandas as pd

n = 14
# p = [5, 6, 9, 12, 7,
#      12, 10, 6, 10, 9,
#      7, 8, 7, 5]
p = [5 , 5 , 9 ,12 , 7 ,11, 10 , 6, 10 , 9 , 4  ,5  ,7,  5]
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
# CPM
s1 = np.zeros(n)
c1 = np.zeros(n)
s2 = np.zeros(n)
c2 = 1e9 * np.ones(n)
# Forward search
degree = root.copy()
def forward(head):
    global degree
    degree[head] = 0
    post_list = [j for j in range(n) if relation_mat[head, j] == 1]
    for i,j in enumerate(post_list):
        s1[j] = max(s1[j], c1[head])
        c1[j] = p[j] + s1[j]
        degree[j] = 1
    return 0
for i in range(n):
    if root[i]:
        c1[i] = p[i]
while max(degree) > 0:
    for i in range(n):
        if degree[i]:
            forward(i)
print(c1)
cmax = max(c1)
# Backward search
degree = leaf.copy()
def backward(tail):
    global degree
    degree[tail] = 0
    pre_list = [j for j in range(n) if relation_mat[j, tail] == 1]
    for i,j in enumerate(pre_list):
        c2[j] = min(c2[j], s2[tail])
        s2[j] = c2[j] - p[j]
        degree[j] = 1
    return 0
for i in range(n):
    if leaf[i]:
        c2[i] = cmax
        s2[i] = c2[i] - p[i]
while max(degree) > 0:
    for i in range(n):
        if degree[i]:
            backward(i)
print(c2)
cp_nodes = [i for i in range(n) if c1[i] == c2[i]]
print(cp_nodes)
def output(path):
    print('->'.join(str(i) for i in path))
def summation(path):
    t = 0
    for j in path:
        t += p[j-1]
    return t
def deep(head):
    global path
    path.append(head+1)
    if leaf[head] and (summation(path) == cmax):
        output(path)
        del path[-1]
    else:
        for x in cp_nodes:
            if relation_mat[head, x]:
                deep(x)
        del path[-1]
    return 0
print(root)
for i in range(n):
    if root[i]:
        path = []
        deep(i)