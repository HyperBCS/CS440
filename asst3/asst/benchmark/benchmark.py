import random, math
import numpy as np
import heapq
import time
from copy import deepcopy
from controllers import utils, a_star, a_star_seq, ucs
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

tot_runtime_a = 0
tot_runtime_b = 0
tot_runtime_c = 0
avg_path_perf_a = 0
avg_path_perf_b = 0
avg_path_perf_c = 0
avg_nodes_a = 0
avg_nodes_b = 0
avg_nodes_c = 0
avg_mem_a = 0
avg_mem_b = 0
avg_mem_c = 0

count = 1
for j in range(1):
	for k in range(1):
		print(str(count) + "/50")
		filename = 'grid' + str(j + 1) + '_' + str(k + 1) + ".txt"
		grid, start, end, regions = utils.load_file(filename)
		opt_path = a_star.min_d(start,end)
		start1 = time.time()
		solved1, path1, g_h_f1, expanded1 = a_star.solve(grid, start, end, 1.5)
		end1 = time.time()
		start2 = time.time()
		solved2, path2, g_h_f2, expanded2 = a_star.solve(grid, start, end, 2)
		end2= time.time()
		start3 = time.time()
		solved3, path3, g_h_f3, expanded3 = a_star.solve(grid, start, end, 3)
		end3 = time.time()
		tot_runtime_a += end1 - start1
		tot_runtime_b += end2 - start2
		tot_runtime_c += end3 - start3
		avg_path_perf_a += g_h_f1[utils.coord_id(end)][0] / opt_path
		avg_path_perf_b += g_h_f2[utils.coord_id(end)][0] / opt_path
		avg_path_perf_c += g_h_f3[utils.coord_id(end)][0] / opt_path
		avg_nodes_a += expanded1
		avg_nodes_b += expanded2
		avg_nodes_c += expanded3
		print("STATS FOR weighted A* 0.25*eucledian w=1.5")
		print("File: " + filename)
		print("Runtime: " + str(tot_runtime_a))
		print("G-Value: " + str(g_h_f1[utils.coord_id(end)][0]))
		print("Nodes expanded: " + str(avg_nodes_a))
		print("--------------------------------")
		print("STATS FOR weighted A* 0.25*eucledian w=2")
		print("File: " + filename)
		print("Runtime: " + str(tot_runtime_b))
		print("G-Value: " + str(g_h_f2[utils.coord_id(end)][0]))
		print("Nodes expanded: " + str(avg_nodes_b))
		print("--------------------------------")
		print("STATS FOR weighted A* 0.25*eucledian w=3")
		print("File: " + filename)
		print("Runtime: " + str(tot_runtime_c))
		print("G-Value: " + str(g_h_f3[utils.coord_id(end)][0]))
		print("Nodes expanded: " + str(avg_nodes_c))
		print("--------------------------------")
		count += 1
# print("STATS FOR A* heuristic from PDF")
# print("A* weighted w=1.5 Statistics")
# print("Average runtime: " + str(tot_runtime_a / 50))
# print("Average optimality: " + str(avg_path_perf_a / 50))
# print("Average nodes expanded: " + str(avg_nodes_a / 50))
# print("--------------------------------")
# print("A* weighted w=3 Statistics")
# print("Average runtime: " + str(tot_runtime_b / 50))
# print("Average optimality: " + str(avg_path_perf_b / 50))
# print("Average nodes expanded: " + str(avg_nodes_b / 50))
# print("--------------------------------")
# print("A* weighted w=4 Statistics")
# print("Average runtime: " + str(tot_runtime_c / 50))
# print("Average optimality: " + str(avg_path_perf_c / 50))
# print("Average nodes expanded: " + str(avg_nodes_c / 50))