"""
Sensor node placement problem
Modified: 27 March 2022
"""
from pulp import *
import math
import matplotlib.pyplot as plt
import time
import random
import numpy as np
start_time = time.time()
#initialization
Dmax = 20 #sensing radius of each node (in m)
c = 1 #cost of establishing a node
W = 100 # Area wide (in m)
H = 100 # Area height (in m)
xin = 0 #starting x point
yin = 0 #starting y point
res = 20 #grid resolution (in m)
P = {}

#potential node locations
rows, cols = (int(H/res+1), int(W/res+1)) #x-y array dimension
xarray = [] 
yarray = []
for i in range(cols): 
    col = [] 
    for j in range(rows): 
        col.append(xin) 
    xarray.append(col) 
    xin = xin + res 
for i in range(cols): 
    col = [] 
    for j in range(rows): 
        col.append(yin)
        yin = yin + res
    yarray.append(col) 
    yin = 0 
xarray1 = np.array(xarray) 
x0 = xarray1.flatten()
yarray1 = np.array(yarray)
y0 = yarray1.flatten()
for k in range(0,rows*cols):
    P[k] = (x0[k],y0[k])

#find node separation distances
Np = [i for i in P.keys()]  #set of all nodes
D = {}  #D will be a dictionary whose keys are links and whose
        #values are separation distances, i.e. Dij
C = {}  #C will be a dictionary whose keys are nodes and whose
        #values are establishing costs, i.e. Ci
for i in Np:
    C[i] = c
    for j in Np:
        tmp = math.sqrt(pow(P[i][0] - P[j][0],2) + \
                        pow(P[i][1] - P[j][1],2))
        D[(i,j)] = tmp #node separation distance

#find the indicator Aij
A = {}
for i in Np:
    for j in Np:
        if D[(i,j)] <= Dmax:
            A[(i,j)] = 1
        else:
            A[(i,j)] = 0
            
prob = LpProblem('nodePlacement_problem', LpMinimize)
x = LpVariable.dicts('x', (Np), 0, 1, LpInteger)
#objective function
prob += lpSum(C[i]*x[i] for i in Np) 
#constraints
for i in Np:
    prob += lpSum(A[(i,j)]*x[j] for j in Np) >= 1
prob.writeLP('nodePlacement_problem.lp')
prob.solve()
print ('Status:', LpStatus[prob.status])
print ('Optimal cost:', '%.2f' % value(prob.objective))
# for v in prob.variables():
#     print(v.name, "=", v.varValue)

#display network layout
for i in Np:
    if x[i].varValue == 1:
        plt.plot(P[i][0],P[i][1], 'r*')
    else:
        plt.plot(P[i][0],P[i][1], 'g.')
    plt.text(P[i][0], P[i][1]+2.5, '%d' % i)
    # for j in Np:
    #     if x[i][j].varValue == 1:
    #         x_values = [P[i][0], P[j][0]]
    #         y_values = [P[i][1], P[j][1]]
    #         plt.plot(x_values, y_values, 'g--')
plt.axis([-5, W+5, -5, H+5])
plt.xlabel('x position [m]')
plt.ylabel('y position [m]')
plt.title('Potential node locations: %d locations' % (len(P)))
plt.grid(True)
plt.show()

#runtime
print("\n** Runtime: %.2f sec **" % (time.time() - start_time))