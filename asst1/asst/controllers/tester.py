from itertools import *
import solver, hill2
import numpy as np
import traceback
import math
import random
import json
import time

def make_grid_nums(n):
    num_arr = []
    for i in range(0,n):
        row = []
        for j in range(0,n):
            row.append(random.randint(1,n-1))
        num_arr.append(row)
    num_arr[n-1][n-1] = 0
    return num_arr

def testBasic():
    new_arr = {}
    size = 9
    iters = 75
    temp_init = 900
    for uio in range(40):
        grid = make_grid_nums(size)
        for n in range(60):
            grid_calc, grid_cost, value, solution, iters2, iter_vals = hill2.doBasic(grid, size, iters)
            for u,num in enumerate(iter_vals):
                if u not in new_arr:
                    new_arr[u] = [num]
                else:
                    new_arr[u].append(num)  

    avg_arr = []
    # print(new_arr)
    for m in new_arr:
        avg_arr.append(np.sum(new_arr[m]) / (1.0 * len(new_arr[m])))
    print(avg_arr)

def testRestart():
    new_arr = {}
    size = 11
    restarts = 75
    iters_per = 150
    for uio in range(3):
        grid = make_grid_nums(size)
        for n in range(25):
            grid_calc, grid_cost, value, solution, iters2, iter_vals = hill2.doRestart(grid, size, restarts, iters_per)
            for u,num in enumerate(iter_vals):
                if u not in new_arr:
                    new_arr[u] = [num]
                else:
                    new_arr[u].append(num)  

    avg_arr = []
    # print(new_arr)
    for m in new_arr:
        avg_arr.append(np.sum(new_arr[m]) / (1.0 * len(new_arr[m])))
    print(avg_arr)
testBasic()
# testRestart()