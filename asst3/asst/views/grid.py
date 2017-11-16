from flask import Blueprint, render_template, abort, flash
from flask import request
from itertools import *
from asst.controllers import a_star, ucs, a_star_seq, grid_gen
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
    grid, start, end = grid_gen.make_grid_nums()
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

