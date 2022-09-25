import numpy as np
import pandas as pd

def sort(x, order, d1):
    # bubble sort
    td = d1.copy()
    for i in range(x):
        tmin = td[i]
        marker = i
        for j in range(i+1, x):
            if td[j] < tmin:
                tmin = td[j]
                marker = j
        if marker != i:
            o = order[marker]
            for j in range(marker - i):
                td[marker - j] = td[marker - j - 1]
                order[marker - j] = order[marker - j - 1]
            td[i] = tmin
            order[i] = o
    return order, td
def run_EDD(instance):
    data = pd.read_csv(instance,sep = ' ')
    time = np.array(data)
    n = int(time[0, 0])
    p = np.zeros(n)
    d = np.zeros(n)
    for i in range(n):
        p[i] = int(time[i+1, 0])
        d[i] = int(time[i+1, 1])
    store = {}
    o2, d2 = sort(n, np.arange(0,n,1), d)
    y_st = 0
    y_en = 0
    timespan = 0
    loss = 0
    while (y_en < n):
        while (y_en < n-1) and (d2[y_en+1] == d2[y_en]):
            y_en += 1
        p2 = [p[o2[i]] for i in range(y_st, y_en + 1)]
        o3, p3 = sort(y_en-y_st+1, o2[y_st:y_en+1], p2)
        for i in o3:
            store[i] = int(timespan)
            timespan += p[i]
            loss += max(timespan - d[i], 0)
        y_en += 1
        y_st = y_en
    return (int(loss), store)

