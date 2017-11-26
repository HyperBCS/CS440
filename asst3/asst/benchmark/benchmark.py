import random, math
import numpy as np
import heapq
import time
from copy import deepcopy
from controllers import utils, a_star, a_star_seq
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
	for k in range(5):
		filename = 'grid' + str(j + 1) + '_' + str(k + 1) + ".txt"
		grid, start, end, regions = utils.load_file(filename)
		solved, path, g_h_f = a_star.solve(grid, start, end)
		print(g_h_f[utils.coord_id(end)][0])