from flask import Blueprint, render_template, abort, flash
from flask import request
from itertools import *
from asst.controllers import a_star, ucs, a_star_seq, grid_gen, utils
import numpy as np
from os import listdir
from os.path import isfile, join, dirname, realpath
from copy import deepcopy
import traceback
import sys, traceback
import math
import random
import json
import time

page = Blueprint('main', __name__, template_folder='templates')
ROWS = 120
COLS = 160

@page.route("solve_grid",methods=['POST'])
def solve_grid():
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


@page.route("load_file",methods=['POST'])
def load_file():
    try:
        data = request.get_json()
        filename = data['filename']
        method = data['method']
        method = int(data['method'])
        w = [float(data['w1']), float(data['w2'])]
        grid, start, end, regions = utils.load_file(filename)
    except Exception as e:
        traceback.print_exc(file=sys.stdout)
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
    response = {"grid": grid, "start": start, "end": end, "path" : path, "g_h_f": g_h_f, "regions": regions}
    return json.dumps(response)


@page.route("get_grid",methods=['POST'])
def get_grid():
    try:
        grid, start, end, regions = grid_gen.make_grid_nums()
    except Exception as e:
        return "Error", 500
    solved, path, g_h_f = a_star.solve(grid, start, end)
    response = {"grid": grid, "start": start, "end": end, "path" : path, "g_h_f": g_h_f, "regions": regions}
    return json.dumps(response)

@page.route("upload_grid", methods=['GET'])
@page.route("/",methods=['GET', 'POST'])
def showhello(filename = None):
    mypath = dirname(realpath(__file__)) + "/../grids"
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    if onlyfiles is not None:
        onlyfiles.sort()
    return render_template('/grid.html', files = onlyfiles, filename = filename)


@page.route("upload_grid", methods=['POST'])
def upgrid():
    if 'file' not in request.files:
        flash('No file part', 'danger')
        return showhello()
    file = request.files['file']
    # if user does not select file, browser also
    # submit a empty part without filename
    if file.filename == '':
        flash('No selected file', 'danger')
        return showhello()
    try:
        grid, start, end, regions = utils.parse_file(file)
        if len(grid[0]) * len(grid) != ROWS * COLS:
            flash("Invalid grid file", 'danger')
            return showhello()
        file.seek(0)
        utils.save_file(file, file.filename)
        flash("Grid uploaded successfully", 'success')
        # return get_grid([grid, start, end])
        return showhello(file.filename)
    except:
        traceback.print_exc(file=sys.stdout)
        flash("Error reading file", 'danger')
        return showhello()

