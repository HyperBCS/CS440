from flask import Blueprint, render_template, abort
from flask import request
from itertools import *
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

@page.route("/",methods=['GET', 'POST'])
def showhello():
    size = 5
    try:
        size = int(request.form['size'])
    except Exception as e:
        pass
    grid = make_grid_nums(size)
    grid2 = range(0,size*size)
    '''Super basic function. Always shows "Hi"'''
    return render_template('/grid.html', nums=grid, size=size, grid2=grid2)


# Connect to basic hill climb in controller
def doBasic(size, grid):
    grid_calc = [random.randint(1, size-1) for x in range(size*size)]
    grid_cost = [random.randint(1, size-1) for x in range(size*size)]
    return grid_calc, grid_cost, "Basic solution"

# Connect to restart in controller
def doRestart(size, grid):
    grid_calc = [random.randint(1, size-1) for x in range(size*size)]
    grid_cost = [random.randint(1, size-1) for x in range(size*size)]
    return grid_calc, grid_cost, "Restart solution"

# Connect to the random walk controller
def doWalk(size, grid):
    grid_calc = [random.randint(1, size-1) for x in range(size*size)]
    grid_cost = [random.randint(1, size-1) for x in range(size*size)]
    return grid_calc, grid_cost, "Walk solution"

# Connect to the simulated anneal controller
def doAnneal(size, grid):
    grid_calc = [random.randint(1, size-1) for x in range(size*size)]
    grid_cost = [random.randint(1, size-1) for x in range(size*size)]
    return grid_calc, grid_cost, "Anneal solution"

# Connect to the genetic population method controller
def doGenetic(size, grid):
    grid_calc = [random.randint(1, size-1) for x in range(size*size)]
    grid_cost = [random.randint(1, size-1) for x in range(size*size)]
    return grid_calc, grid_cost, "Genetic solution"

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
        grid_o = data['grid']
        grid_c_o = data['grid_c']
    except Exception as e:
       print(e) 
       return "Error", 500
    try:
        if req_type == "basic":
            grid, grid2, msg = doBasic(size, grid_o)
        elif req_type == 'restart':
            grid, grid2, msg = doRestart(size, grid_o)
        elif req_type == 'walk':
            grid, grid2, msg = doWalk(size, grid_o)
        elif req_type == 'anneal':
            grid, grid2, msg = doAnneal(size, grid_o)
        elif req_type == 'genetic':
            grid, grid2, msg = doGenetic(size, grid_o)
        else:
            return "Bad request", 400
    except Exception as e:
        print(e)
        return "Internal Server Error", 500

    '''Super basic function. Always shows "Hi"'''
    response = {"grid": grid, "grid2": grid2, "msg": msg}
    return json.dumps(response)