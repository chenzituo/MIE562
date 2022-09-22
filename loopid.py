import numpy as np
import pandas as pd

n = 7
relation_dic = np.array(pd.read_csv('./disp.csv'))
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
def output(path, idt):
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
        print('->'.join(str(x) for i, x in enumerate(path) if i >= mark))
def deep(head):
    global path, ident
    if (head+1) in path:
        output(path, head+1)
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

print(path_set)