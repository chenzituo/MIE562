# All rights reserved.
# Author: Zituo Chen

import gurobipy as gp
from gurobipy import GRB
import time as tim

time = 360

def readin(instance):
    with open(instance,'r') as f:
        data = f.readlines()
    crop = len(data)-1
    rv = {}
    rv['name'] = []
    rv['price'] = []
    rv['yield'] = []
    rv['variable'] = []
    rv['mature_L'] = []
    rv['mature_U'] = []
    rv['season_L1'] = []
    rv['season_U1'] = []
    rv['season_L2'] = []
    rv['season_U2'] = []
    for i in range(crop):
        temp = data[i+1].split(',')
        rv['name'].append(temp[0])
        rv['price'].append(float(temp[1]))
        rv['yield'].append(float(temp[2]))
        rv['variable'].append(int(temp[3]))
        rv['mature_L'].append(int(temp[4]))
        rv['mature_U'].append(int(temp[5]))
        rv['season_L1'].append(int(temp[6]))
        rv['season_U1'].append(int(temp[7]))
        rv['season_L2'].append(int(temp[8]))
        rv['season_U2'].append(int(temp[9]))
    return rv
def generate(data):
    rv = data.copy()
    crop = len(data['name'])
    rv['opt'] = [(rv['mature_L'][i]+rv['mature_U'][i])//2 for i in range(crop)]
    rv['marginal'] = [rv['variable'][i]/rv['opt'][i] for i in range(crop)]
    rv['decay'] = [0.4054651*rv['opt'][i]/(rv['mature_U'][i]-rv['opt'][i]) for i in range(crop)]
    rv['yield_m'] = {}
    for i in range(crop):
        rv['yield_m'][i] = []
        opt = rv['yield'][i]
        d = rv['decay'][i]
        t = rv['opt'][i]
        t0 = rv['mature_L'][i]
        for j in range(rv['mature_U'][i]-rv['mature_L'][i]):
            rv['yield_m'][i].append(opt * (2 - 2.718282 ** (d * abs(j+t0 - t)/t)))
    rv['profit'] = {}
    for i in range(crop):
        rv['profit'][i] = []
        t0 = rv['mature_L'][i]
        for j in range(rv['mature_U'][i]-rv['mature_L'][i]):
            temp = rv['yield_m'][i][j] * rv['price'][i] - rv['marginal'][i]*(t0+j)
            rv['profit'][i].append(temp)
    rv['season'] = {}
    for i in range(crop):
        rv['season'][i] = [1 for j in range(time)]
        for j in range(rv['season_L1'][i],rv['season_U1'][i]):
            rv['season'][i][j] = 0
        for j in range(rv['season_L2'][i],rv['season_U2'][i]):
            rv['season'][i][j] = 0
    return rv
def run_ti(instance, field, acres, labor):
    # readin
    data = readin(instance)
    # preprocess
    rv = generate(data)
    # print(rv['yield'][0])
    # print(rv['profit'][0])
    # print(rv['season'])
    # crop here is available number of crops species
    # crop = len(rv['name'])
    crop = 2
    global time
    # Time-indexed
    model = gp.Model('Time-indexed')
    
    model.Params.outputFlag = 0

    x = model.addVars(range(field), range(crop), range(2 * time), vtype = GRB.BINARY, name = 'x')
    z = model.addVars(range(field), range(crop), range(time), vtype = GRB.BINARY, name = 'z')
    # p = model.addVars(range(field), range(crop), vtype = GRB.INTEGER, name = 'p')
    # p_ij = \sum_t\in L-U_j z_ijt * t
    model.update()

    model.setObjective(gp.quicksum(\
        gp.quicksum(x[i,j,t]*z[i,j,tt]*rv['profit'][j][tt-rv['mature_L'][j]]\
             for j in range(crop)\
             for tt in range(rv['mature_L'][j],rv['mature_U'][j])\
             for t in range(time, 2*time))*acres[i]\
             for i in range(field)), GRB.MAXIMIZE)
    # Cross year
    model.addConstrs((x[i,j,t] == x[i,j,t+time] for t in range(time) for i in range(field) for j in range(crop)),'c0')
    # Growth time control
    model.addConstrs((gp.quicksum(z[i,j,t] for t in range(rv['mature_L'][j],rv['mature_U'][j])) == 1\
         for i in range(field) for j in range(crop)),'c1')
    # model.addConstrs((p[i,j]>=rv['mature_L'][j] for i in range(field) for j in range(crop)), 'c11')
    # model.addConstrs((p[i,j]<=rv['mature_U'][j] for i in range(field) for j in range(crop)), 'c12')
    # No overlap
    model.addConstrs((gp.quicksum(x[i,j,tt]*z[i,j,ttt] for j in range(crop)\
        for ttt in range(rv['mature_L'][j],rv['mature_U'][j])\
         for tt in range(t-ttt+1, t+1))<=1\
              for i in range(field) for t in range(time, time *2)),'c2')
    # Workforce constraint
    model.addConstrs((gp.quicksum(x[i,j,t]+\
        gp.quicksum(x[i,j,t-tt+1]*z[i,j,tt] for tt in range(rv['mature_L'][j],rv['mature_U'][j])) \
         for i in range(field) for j in range(crop))<= labor\
        for t in range(time, 2*time)),'c3')
    # Sowing season control
    model.addConstrs((gp.quicksum(rv['season'][j][t]*x[i,j,t+time] for t in range(time)) == 0 for i in range(field) for j in range(crop)),'c4')
    

    model.update()
    model.optimize()

    for v in model.getVars():
        if v.X == 1 and 'x' in v.Varname:
            xx = v.Varname.split(',')
            if int(xx[-1][:-1])<360:
            # if True:
                print(v.Varname, v.X)
        elif v.X == 1 and 'z' in v.Varname:
            print(v.Varname, v.X)
    print('%.3f' % model.ObjVal)

r1 = tim.time()
run_ti('data.csv', field = 6, acres =[i+1 for i in range(6)], labor = 1)
r2 = tim.time()
print(r2-r1)