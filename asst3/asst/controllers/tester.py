from itertools import *
import solver, hill2, genetic2
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
    size = 11
    iters = 500
    initial_pop = 30
    num_child = 4
    mutation_rate = 0.1
    for n in range(10):
        grid = make_grid_nums(size)
        grid_calc, grid_cost, value, solution, iter_vals = genetic2.doGenetic(grid, size, iters, initial_pop, num_child, mutation_rate)
        for u,num in enumerate(iter_vals):
            if u not in new_arr:
                new_arr[u] = [num]
            else:
                new_arr[u].append(num)  

    avg_arr = []
    # print(new_arr)
    for m in new_arr:
        avg_arr.append(np.sum(new_arr[m]) / (1.0 * len(new_arr[m])))
    return avg_arr

def testRestart():
    new_arr = {}
    size = 11
    restarts = 10
    iters_per = 200
    for n in range(50):
        grid = make_grid_nums(size)
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
    return avg_arr
g = testBasic()
# g = testRestart()
for n in g:
    print(str(n))