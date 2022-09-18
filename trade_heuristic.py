import numpy as np
import pandas as pd

n = 14
pmax = np.array([5, 6, 9, 12, 7,
        12, 10, 6, 10, 9,
        7, 8, 7, 5])
pmin = np.array([3, 5, 7, 9, 5,
        9, 8, 3, 7, 6,
        4, 5, 5, 2])
ca = np.array([20, 25, 20, 15, 30,
      40, 35, 25, 30, 20,
      25, 35, 20, 10])
mgc = np.array([7, 2, 4, 3, 4,
       3, 4, 4, 4, 5,
       2, 2, 4, 8])
c0 = 6
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
            # print(i+1, '->', int(relation_dic[head, i]))

p = pmax.copy()
p_margin = pmax-pmin
def construct(path):
    global gcp
    l = len(path)
    for i in range(l-1):
        gcp[path[i], path[i+1]] = 1
def cpm():
    global p, degree, path, cmax
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
        global cmax
        if (summation(path) == cmax):
            print('->'.join(str(i+1) for i in path))
            construct(path)
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
# Evaluation
def evaluation(span):
    print(span)
    v = c0 * span + sum(ca)
    v = v + sum((pmax-p)*mgc)
    return v

# Heuristic
while True:
    gcp = np.zeros([n, n])
    cpm()
    restore = gcp.copy()
    # print('Heur')
    # print(gcp)

    def remove(i):
        global gcp
        gcp[:,i] = np.zeros(n)
        gcp[i,:] = np.zeros(n)
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
    # generate minimal
    minset = {}
    count = 0
    defi = np.ones((n+1)**3)
    for i in range(n):
        if root[i] == 1:
            count += 1
            minset[count] = i
            defi[i+1] = 0
        elif leaf[i] == 1:
            count += 1
            minset[count] = i
            defi[i+1] = 0
    def test1():
        global gcp, count
        for i in range(n):
            if defi[i+1]:
                remove(i)
                if not achieve(0):
                    count += 1
                    minset[count] = i
                    defi[i+1] = 0
                gcp = restore.copy()
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
                            minset[count] = [i, j]
                            defi[(i+1)*(n+1)+(j+1)] = 0
                        gcp = restore.copy()
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
                                    minset[count] = [i, j, k]
                                    defi[(i+1)*n**2+(j+1)*n+(k+1)] = 0
                                gcp = restore.copy()
    test3()
    # print(minset)
    # Prune
    minc = 1e9
    item = -1
    for s in minset:
        sets = minset[s]
        if isinstance(sets, int):
            sets = [sets]
        bl = 1
        for j in sets:
            if p_margin[j] == 0:
                bl = 0 
                break
        if bl:
            cost = 0
            for j in sets:
                cost += mgc[j]
            if cost<minc:
                minc = cost
                item = sets
    if minc<=c0:
        for j in item:
            p_margin[j] -= 1
            p[j] -= 1
        print(p)
        print(evaluation(cmax-1), c0-minc)
        print('Next round!')
    else:
        print('End!')
        break
