import random, math
import numpy as np
import heapq
import time
from copy import deepcopy
import vertex, utils
from werkzeug.datastructures import FileStorage
import sys, traceback
from os import listdir
from os.path import isfile, join, dirname, realpath

def load_file(filename):
	path = dirname(realpath(__file__)) + "/../grids/" + filename
	try:
		file = open(path,"r") 
		return parse_file(file)
	except:
		traceback.print_exc(file=sys.stdout)
		return None

tot_runtime = 0
avg_path_perf = 0

for j in range(10):
	count = 1
	for grid in make_grid_nums():
		filename = 'grid' + str(j + 1) + '_' + str(count) + ".txt"
		grid, start, end, regions = utils.load_file(filename)
		myFile.write(str(grid[1][0]) + "," + str(grid[1][1]) + '\n')
		myFile.write(str(grid[2][0]) + "," + str(grid[2][1]) + '\n')
		for reg in grid[3]:
			myFile.write(str(reg[0]) + "," + str(reg[1]) + '\n')
		for x in grid[0]:
			for y in x:
				myFile.write(y)
			myFile.write('\n')
		myFile.close()
		count += 1