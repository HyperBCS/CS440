import random, math
import numpy as np
import heapq
import time
from copy import deepcopy

ROWS = 120
COLS = 160

def add_highway(num_arr):          
    corner = random.randint(0, 3)
    # top wall
    if corner == 0:
        bounary_start = [0, random.randint(1, COLS-2)] 
        mov_x = 1
        mov_y = 0
    # bottom wall
    elif corner == 1:
        bounary_start = [ROWS - 1, random.randint(1, COLS-2)]  
        mov_x = -1
        mov_y = 0
    # left wall
    elif corner == 2:
        bounary_start = [random.randint(1, ROWS-2), 0]  
        mov_x = 0
        mov_y = -1
    # right wall
    elif corner == 3:
        bounary_start = [random.randint(1, ROWS-2), COLS - 1]  
        mov_x = 0
        mov_y = -1
    x_c = bounary_start[0]
    y_c = bounary_start[1]
    for x in range(0,5):
        if x_c + 20 * mov_x >= ROWS or x_c + 20 * mov_x < 0 or y_c + 20 * mov_y >= COLS or y_c + 20 * mov_y < 0:
            return -1
        for a in range(0,20):
            if num_arr[x_c][y_c] == 'a' or num_arr[x_c][y_c] == 'b':
                return -1
            if num_arr[x_c][y_c] == 1:
                num_arr[x_c][y_c] = 'a'
            elif num_arr[x_c][y_c] == 2:
                num_arr[x_c][y_c] = 'b'
            if a < 19:
                x_c = x_c + mov_x
                y_c  = y_c + mov_y
        if random.random() < 0.4:
            if abs(mov_x) == 1:
                mov_y = 1 if bool(random.getrandbits(1)) else -1
                mov_x = 0
            elif abs(mov_y) == 1:
                mov_x = 1 if bool(random.getrandbits(1)) else -1
                mov_y = 0
        x_c = x_c + mov_x
        y_c  = y_c + mov_y

def make_start_end(num_arr):
    while True:
        start_end = random.sample(range(0, 4), 2)
        corner_coords = []
        # top wall
        corner_coords.append([random.randint(0, 20), random.randint(COLS-21, COLS-1)])
        # bottom wall
        corner_coords.append([random.randint(ROWS-21, ROWS-1), random.randint(COLS-21, COLS-1)])
        # left wall
        corner_coords.append([random.randint(1, ROWS-1), random.randint(0, 20)])
        # right wall
        corner_coords.append([random.randint(1, ROWS-1), random.randint(COLS-21, COLS-1)])
        if num_arr[corner_coords[start_end[0]][0]][corner_coords[start_end[0]][1]] != 0 and num_arr[corner_coords[start_end[1]][0]][corner_coords[start_end[1]][1]] != 0:
            distance =  math.hypot(corner_coords[start_end[1]][1] - corner_coords[start_end[0]][1], corner_coords[start_end[1]][0] - corner_coords[start_end[0]][0])
            if distance >= 100:
                break
    return corner_coords[start_end[0]], corner_coords[start_end[1]]


# create a random grid of size n
def make_grid_nums():
    terrain = [0, 1, 2, 'a', 'b']
    num_arr = np.full((ROWS, COLS), 1).tolist()
    # Doing hard to traverse
    for i in range(0, 8):
        coord = [random.randint(0, ROWS-1), random.randint(0, COLS-1)]
        start_x = max(coord[0] - 15, 0)
        start_y = max(coord[1] - 15, 0)
        end_x = min(coord[0] + 15, ROWS - 1)
        end_y = min(coord[1] + 15, COLS - 1)
        for x in range(start_x,end_x + 1):
            for y in range(start_y, end_y + 1):
                num_arr[x][y] = 2 if (random.random() > 0.5 or num_arr[x][y] == 2) else 1
    # add highways  
    i = 0
    while i < 4:
        tmp_list = deepcopy(num_arr)
        if add_highway(num_arr) == -1:
            num_arr = deepcopy(tmp_list)
            continue
        i = i + 1
    # add blocked things
    i = 0
    while i < 0.2 * ROWS * COLS:
        coord = [random.randint(0, ROWS-1), random.randint(0, COLS-1)]
        if num_arr[coord[0]][coord[1]] != 'a' and num_arr[coord[0]][coord[1]] != 'b':
            num_arr[coord[0]][coord[1]] = 0
            i = i + 1
    start, end = make_start_end(num_arr)
    return num_arr, start, end