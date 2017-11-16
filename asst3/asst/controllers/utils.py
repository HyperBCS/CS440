import random, math
import numpy as np
import heapq
import time
from copy import deepcopy
from asst.controllers import vertex

ROWS = 120
COLS = 160

def coord_id(coord):
	return coord[0] * COLS + coord[1]

def succ(num_arr, point, closed):
	not_succ = []
	succs = []
	# check left
	not_succ.append(vertex.Vertex([point.x - 1, point.y], 0))
	# check right
	not_succ.append(vertex.Vertex([point.x + 1, point.y], 0))
	# check up
	not_succ.append(vertex.Vertex([point.x, point.y - 1], 0))
	# check down
	not_succ.append(vertex.Vertex([point.x, point.y + 1], 0))
	# check left up
	not_succ.append(vertex.Vertex([point.x - 1, point.y - 1], 0))
	# check right up
	not_succ.append(vertex.Vertex([point.x + 1, point.y - 1], 0))
	# check left down
	not_succ.append(vertex.Vertex([point.x - 1, point.y + 1], 0))
	# check right down
	not_succ.append(vertex.Vertex([point.x + 1, point.y + 1], 0))
	for ss in not_succ:
		if not (check_bounds(num_arr, [ss.x, ss.y]) or (ss in closed)):
			succs.append(ss)
	return succs

def check_bounds(num_arr, point):
	if(point[0] < 0 or point[0] > ROWS - 1 or point[1] < 0 or point[1] > COLS - 1 or num_arr[point[0]][point[1]] == 0):
		return True
	else:
		return False

def cost(num_arr, c1, c2):
	multi = 1
	curr = num_arr[c1[0]][c1[1]]
	next_p = num_arr[c2[0]][c2[1]]
	# means we move diag
	if c2[0] - c1[0] == 1 and c2[1] - c1[1] == 1:
		multi *= math.sqrt(2)
	# if hard terrain to hard terrain
	if (curr == '2' or curr == 'b') and (next_p == '2' or next_p == 'b'):
		multi *= 2
	# if hard terrain to smooth
	if (curr == '2' or curr == 'b') != (next_p == '2' or next_p == 'b'):
		multi *= 1.5
	# if highway
	if (curr == 'a' or curr == 'b') and (next_p == 'a' or next_p == 'b'):
		multi *= 0.25
	return multi

def goal_path(start, end, parent):
	g_path = []
	curr = end
	while curr != start:
		curr = parent[coord_id(curr)]
		if curr != start:
			g_path.append(curr)
	return g_path