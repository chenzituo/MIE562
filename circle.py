import numpy as np
import pandas as pd

n = 9
p = np.array([15, 50, 60,
              50, 50, 15,
              30, 15, 20])
relation_dic = np.array(pd.read_csv('./patch.csv'))
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
restore = relation_mat.copy()
m = 3
resource = {}
resource[0] = [1, 5, 7]
resource[1] = [2, 4, 8]
resource[2] = [3, 6, 9]
def scare(n):
    x = 1
    for j in range(n):
        x = x*(j+1)
    return x
length = [len(resource[i]) for i in range(m)]
ls = np.array([scare(c) for c in length]).prod()

def cpm():
    global p, degree, path, cmax, relation_mat
    # print(p)
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
    # print(c1)
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
    # print(c2)
    cp_nodes = [i for i in range(n) if c1[i] == c2[i]]
    # print(cp_nodes)
    def output(path):
        global cmax, imin, pmin, rmin
        if (summation(path) == cmax):
            # print('->'.join(str(i+1) for i in path))
            # print(cmax)
            if cmax < imin:
                imin = cmax
                pmin = path.copy()
                rmin = relation_mat.copy()
    def summation(path):
        t = 0
        for j in path:
            t += p[j]
        return t
    def deep(head):
        global path
        path.append(head)
        if leaf[head]:
            output(path)
            del path[-1]
        else:
            for x in cp_nodes:
                if relation_mat[head, x]:
                    deep(x)
            del path[-1]
        return 0
    for i in range(n):
        if root[i]:
            path = []
            deep(i)
def generate(x):
    global relation_mat
    listt = [[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]
    xx = x
    order = []
    for j in range(m):
        order.append(xx % 6)
        xx = xx // 6
        od = listt[order[-1]]
        for i in range(length[j]-1):
            relation_mat[resource[j][od[i]-1]-1, 
                         resource[j][od[i+1]-1]-1] = 1
def loopid():
    global relation_mat, path_set, count_loop, path
    path_set = {}
    count_loop = 0
    def compare(path1, path2):
        l1 = len(path1)
        l2 = len(path2)
        if l1 == l2:
            bl = 0
            for w in range(l1):
                if path1 == path2:
                    bl = 1
                    break
                t = path1[0]
                for i in range(l1-1):
                    path1[i] = path1[i+1]
                path1[l1-1] = t
            if bl:
                return 1 
        return 0 
    def endd(path, idt):
        global count_loop, path_set
        path.append(idt)
        mark = 0
        while True:
            if path[mark] == idt:
                break
            mark += 1
        p = path[mark+1:]
        bl = 0
        for i in range(1, count_loop+1):
            if compare(p, path_set[i]):
                bl = 1
                break
        if not bl:
            count_loop += 1
            path_set[count_loop] = p
            # print(path_set)
            # print('->'.join(str(x) for i, x in enumerate(path) if i >= mark))
    def deep(head):
        global path, ident
        if (head+1) in path:
            endd(path, head+1)
            del path[-1]
        else:
            path.append(head+1)
            for x in range(n):
                if relation_mat[head, x]:
                    deep(x)
            del path[-1]
        return 0
    for i in range(n):
        path = []
        deep(i)
    return count_loop
rmin = np.zeros([n, n])
pmin = []
imin = 1e9
for x in range(ls):
    relation_mat = restore.copy()
    generate(x)
    bl = loopid()
    if not bl:
        cpm()
# print(pmin)
print('Complete Result')
print('->'.join(str(i+1) for i in pmin))
print(imin)
print(rmin)      
