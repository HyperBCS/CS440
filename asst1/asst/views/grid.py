from flask import Blueprint, render_template, abort
import random

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

@page.route('/')
def showhello():
    grid = make_grid_nums(5)
    '''Super basic function. Always shows "Hi"'''
    return render_template('/grid.html', nums=grid)