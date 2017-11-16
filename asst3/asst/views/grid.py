from flask import Blueprint, render_template, abort, flash
from flask import request
from itertools import *
from asst.controllers import a_star, ucs, a_star_seq
import numpy as np
from copy import deepcopy
import traceback
import math
import random
import json
import time

page = Blueprint('main', __name__, template_folder='templates')
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

@page.route("solve_grid",methods=['POST'])
def solve_grid(arr = None, size = 5):
    try:
        data = request.get_json()
        grid = data['grid']
        start = data['start']
        end = data['end']
        w = [float(data['w1']), float(data['w2'])]
        method = int(data['method'])
    except Exception as e:
        return "Error", 500
    if method == 1:
        solved, path, g_h_f = a_star.solve(grid, start, end)
    elif method == 2:
        solved, path, g_h_f = a_star.solve(grid, start, end, w[0])
    elif method == 3:
        solved, path, g_h_f = a_star_seq.solve(grid, start, end, w)
    elif method == 4:
        solved, path, g_h_f = ucs.solve(grid, start, end)
    else:
        return "Error", 400
    response = {"grid": grid, "start": start, "end": end, "path" : path, "g_h_f": g_h_f}
    return json.dumps(response)

@page.route("get_grid",methods=['POST'])
def get_grid(arr = None, size = 5):
    try:
        data = request.get_json()
    except Exception as e:
        return "Error", 500
    grid, start, end = make_grid_nums()
    solved, path, g_h_f = a_star.solve(grid, start, end)
    response = {"grid": grid, "start": start, "end": end, "path" : path, "g_h_f": g_h_f}
    return json.dumps(response)

@page.route("upload_grid", methods=['GET'])
@page.route("/",methods=['GET', 'POST'])
def showhello(arr = None, size = 5):
    return render_template('/grid.html')


@page.route("upload_grid", methods=['POST'])
def upgrid():
    if 'file' not in request.files:
        flash('No file part', 'danger')
        return showhello()
    file = request.files['file']
    # if user does not select file, browser also
    # submit a empty part without filename
    arr = []
    size = 0
    if file.filename == '':
        flash('No selected file', 'danger')
        return showhello()
    try:
        for line in file.readlines():
            tmp_arr = line.decode().split(" ")
            if len(tmp_arr) == 1:
                size = int(tmp_arr[0])
                continue
            if size == 0:
                raise
            for n, num in enumerate(tmp_arr):
                tmp_arr[n] = int(num)
            if len(tmp_arr) != size:
                flash("Invalid file", 'danger')
                return showhello()
            arr.append(tmp_arr)
        if len(arr) != size:
            flash("Invalid grid file", 'danger')
            return showhello()
        flash("Grid loaded", 'success')
        return showhello(arr, size)
    except:
        flash("Error reading file", 'danger')
        return showhello()

