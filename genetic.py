import random, math
import numpy as np
import time
from copy import deepcopy
from asst.controllers import solver, tester


def doGenetic(grid, size, iters):
    grid2, value, solution = solver.solve_puzzle(grid, size)
    best_val = value
    rand_array1 = [size-1] #bottom row replacement
    rand_array2 = [size-1] #right-most row replacement
    grid3 = deepcopy(grid)
    grid4 = deepcopy(grid)
    move_score1 = 0
    move_score2 = 0     #score for each
    grid_score1 = 0     #bottom-most row score
    grid_score2 = 0     #right-most column score
    for x in range(0, size):
        rand_array1[x] = random.randint(1, size-x)
        rand_array2[x] = random.randint(1, size-x)
    for x in range(0, size):
        if rand_array1[x] <= size-x-1:
            move_score1 += 1
        if rand_array2[x] <= size-x-1:
            move_score2 += 1
        if grid3[size-1][x] <= size-x-1:
            grid_score1 += 1
        if grid3[x][size-1] <= size-x-1:
            grid_score2 += 1
    swapper(grid4, size, rand_array1, rand_array2, move_score1, move_score2, grid_score1, grid_score2)

####COMPARE GRID 3 and GRID 4 Runtimes with the solver
####I was unable to get everything to work using the current build
####Was tested using pre-made grid and solver independently of the front end and other parts


def swapper(grid4, size, rand_array1, rand_array2, move_score1, move_score2, grid_score1, grid_score2):
    if move_score1 > grid_score1:
        for x in range(0, size):
            grid4[size-1][x] = rand_array1[x]
    if move_score2 > grid_score2:
        for x in range(0, size):
            grid4[size-1][x] = rand_array2[x]

