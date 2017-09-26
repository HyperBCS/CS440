from flask import Blueprint, render_template, abort, flash
from flask import request
from itertools import *
from asst.controllers import solver, hill, genetic
import traceback
import math
import random
import json
import time

page = Blueprint('main', __name__, template_folder='templates')

def make_grid_nums(n):
    num_arr = []
    for i in range(0,n):
        row = []
        for j in range(0,n):
            row.append(random.randint(1,n-1))
        num_arr.append(row)
    num_arr[n-1][n-1] = 0
    return num_arr

@page.route("upload_grid", methods=['GET'])
@page.route("/",methods=['GET', 'POST'])
def showhello(arr = None, size = 5):
    try:
        size = int(request.form['size'])
    except Exception as e:
        pass
    if arr == None:
            grid = make_grid_nums(size)
    else:
        grid = arr
    grid2, value, solution = solver.solve_puzzle(grid, size)
    '''Super basic function. Always shows "Hi"'''
    return render_template('/grid.html', nums=grid, size=size, grid2=grid2, sol=solution, value = value)


# Connect to basic hill climb in controller
def doBasic(size, grid, iters):
    start = time.time()
    grid_calc, grid_cost, value, solution, iters = hill.doBasic(grid, size, iters)
    end = time.time()
    if value > 0:
     solution += "\nCompute Time: " + "{0:.2f}".format(end - start) + "s" + "\nIterations: " + str(iters)
    return grid_calc, grid_cost, solution

# Connect to restart in controller
def doRestart(size, grid, iters, iters_per):
    iters_per = int(iters_per)
    start = time.time()
    grid_calc, grid_cost, value, solution, iters = hill.doRestart(grid, size, iters, iters_per)
    end = time.time()
    if value > 0:
     solution += "\nCompute Time: " + "{0:.2f}".format(end - start) + "s" + "\nIterations: " + str(iters)
    return grid_calc, grid_cost, solution

# Connect to the random walk controller
def doWalk(size, grid, iters, prob):
    prob = float(prob)
    start = time.time()
    grid_calc, grid_cost, value, solution, iters = hill.doBasic(grid, size, iters, prob)
    end = time.time()
    if value > 0:
     solution += "\nCompute Time: " + "{0:.2f}".format(end - start) + "s" + "\nIterations: " + str(iters)
    return grid_calc, grid_cost, solution

# Connect to the simulated anneal controller
def doAnneal(size, grid, iters, init_t, decay):
    init_t = int(init_t)
    decay = float(decay)
    start = time.time()
    grid_calc, grid_cost, value, solution, iters = hill.doAnneal(grid, size, iters, init_t, decay)
    end = time.time()
    if value > 0:
     solution += "\nCompute Time: " + "{0:.2f}".format(end - start) + "s" + "\nIterations: " + str(iters)
    return grid_calc, grid_cost, solution

# Connect to the genetic population method controller
def doGenetic(size, grid, iters, child, mut_rate, init_pop):
    child = int(child)
    iters = int(iters)
    init_pop = int(init_pop)
    mut_rate = float(mut_rate)
    start = time.time()
    grid_calc, grid_cost, value, solution = genetic.doGenetic(grid, size, iters, init_pop, child, mut_rate)
    end = time.time()
    if value > 0:
     solution += "\nCompute Time: " + "{0:.2f}".format(end - start) + "s" 
    return grid_calc, grid_cost, solution

def arr_to_grid(grid):
    n = math.sqrt(len(grid))
    arr = []
    if not n.is_integer():
        raise
    size = int(n)
    count = 0
    for n in range(0,size):
        tmp_arr = []
        for m in range(0,size):
            tmp_arr.append(grid[count])
            count += 1
        arr.append(tmp_arr)
    return arr

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

@page.route("get_grids",methods=['POST'])
def getgrids():
    size = 0
    grid_o = None
    grid_c_o = None
    req_type = None
    try:
        data = request.get_json()
        req_type = data['type']
        size = data['size']
        iters = int(data['iters'])
        var2 = data['var2']
        var3 = data['var3']
        var4 = data['var4']
        grid_o = data['grid']
        grid_c_o = data['grid_c']
    except Exception as e:
       print(e) 
       return "Error", 500
    try:
        grid_o = arr_to_grid(grid_o)
        grid_c_o = arr_to_grid(grid_c_o)
        if req_type == "basic":
            grid, grid2, msg = doBasic(size, grid_o, iters)
        elif req_type == 'restart':
            grid, grid2, msg = doRestart(size, grid_o, iters, var2)
        elif req_type == 'walk':
            grid, grid2, msg = doWalk(size, grid_o, iters, var2)
        elif req_type == 'anneal':
            grid, grid2, msg = doAnneal(size, grid_o, iters, var2, var3)
        elif req_type == 'genetic':
            grid, grid2, msg = doGenetic(size, grid_o, iters, var2, var3, var4)
        else:
            return "Bad request", 400
    except Exception as e:
        print(e)
        print(traceback.print_exc())
        return "Internal Server Error", 500

    '''Super basic function. Always shows "Hi"'''
    response = {"grid": grid, "grid2": grid2, "msg": msg}
    return json.dumps(response)