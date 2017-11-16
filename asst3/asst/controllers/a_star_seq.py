import random, math
import numpy as np
import heapq
import time
from asst.controllers import utils, vertex, fringe

ROWS = 120
COLS = 160
n = 5

def heur1(point, end):
	std = math.hypot(point[0] - end[0], point[1] - end[1])
	return math.sqrt(2)*0.25*(std) + 2*math.sqrt(2) - 0.25*(std)

def heur2(point, end):
	std = math.hypot(point[0] - end[0], point[1] - end[1])
	return math.sqrt(2)*0.25*(std) + 2*math.sqrt(2) - 0.25*(std)

def heur3(point, end):
	std = math.hypot(point[0] - end[0], point[1] - end[1])
	return math.sqrt(2)*0.25*(std) + 2*math.sqrt(2) - 0.25*(std)

def heur4(point, end):
	std = math.hypot(point[0] - end[0], point[1] - end[1])
	return math.sqrt(2)*0.25*(std) + 2*math.sqrt(2) - 0.25*(std)

def heur5(point, end):
	std = math.hypot(point[0] - end[0], point[1] - end[1])
	return math.sqrt(2)*0.25*(std) + 2*math.sqrt(2) - 0.25*(std)

# returns g + w*h for the specified hueristic index
def key(s, i, g, end, w, g_h_f):
	g_i = g[i][utils.coord_id(s)]
	# hueristic 1
	if i == 0:
		h_c = heur1(s, end)
		f_c = g_i + w[0] * h_c
		g_h_f[i][utils.coord_id(s)] = [g_i, h_c, f_c]
		return f_c
	# hueristic 2
	if i == 1:
		h_c = heur2(s, end)
		f_c = g_i + w[0] * h_c
		g_h_f[i][utils.coord_id(s)] = [g_i, h_c, f_c]
		return f_c
	# hueristic 3
	if i == 2:
		h_c = heur3(s, end)
		f_c = g_i + w[0] * h_c
		g_h_f[i][utils.coord_id(s)] = [g_i, h_c, f_c]
		return f_c
	# hueristic 4
	if i == 3:
		h_c = heur4(s, end)
		f_c = g_i + w[0] * h_c
		g_h_f[i][utils.coord_id(s)] = [g_i, h_c, f_c]
		return f_c
	# hueristic 5
	if i == 4:
		h_c = heur5(s, end)
		f_c = g_i + w[0] * h_c
		g_h_f[i][utils.coord_id(s)] = [g_i, h_c, f_c]
		return f_c

def expand_state(s, i, fr, g, parent, num_arr, closed, end, w, g_h_f):
	s_c = [s.x, s.y]
	s_cid = utils.coord_id(s_c)
	fr[i].remove(s_c)
	for s_p in utils.succ(num_arr,s, closed[i]):
		sp_c = [s_p.x, s_p.y]
		sp_cid = utils.coord_id(sp_c)
		tmp_cost = utils.cost(num_arr, s_c, sp_c)
		# may be wrong
		if s_p not in fr[i].to_list():
			g[i][sp_cid] = math.inf
			parent[i][sp_cid] = None
		if g[i][sp_cid] > g[i][s_cid] + tmp_cost:
			g[i][sp_cid] = g[i][s_cid] + tmp_cost
			parent[i][sp_cid] = s_c
			if s_p not in closed[i]:
				fr[i].insert(vertex.Vertex(sp_c, key(sp_c, i, g, end, w, g_h_f)))

def solve(num_arr, start, end, w=[1, 1.25]):
	# open_i
	fr = []
	# closed_i
	closed = []
	#g_i
	g = []
	#bp_i
	parent = []
	# stuff to display
	g_h_f = []
	goal = vertex.Vertex(end, 0)
	for i in range(n):
		g.append({})
		g[i][utils.coord_id(start)] = 0
		g[i][utils.coord_id(end)] = math.inf
		parent.append({})
		g_h_f.append({})
		parent[i][utils.coord_id(start)] = start
		parent[i][utils.coord_id(end)] = None
		fr.append(fringe.Fringe(False))
		fr[i].insert(vertex.Vertex(start, key(start, i, g, end, w, g_h_f)))
		closed.append(set())

	while fr[0].minkey().g_h < math.inf:
		for i in range(n):
			if fr[i].minkey().g_h <= w[1] * fr[i].minkey().g_h:
				if g[i][utils.coord_id(end)] <= fr[i].minkey().g_h:
					if g[i][utils.coord_id(end)] < math.inf:
						return True, utils.goal_path(start, end, parent[i]), g_h_f[i]
				else:
					s = fr[i].top()
					expand_state(s, i, fr, g, parent, num_arr, closed, end, w,g_h_f)
					closed[i].add(s)
			else:
				if g[0][utils.coord_id(end)] <= fr[0].minkey().g_h:
					if g[0][utils.coord_id(end)] < math.inf:
						return True, utils.goal_path(start, end, parent[i]), g_h_f[0]
				else:
					s = fr[i].top()
					expand_state(s, 0, fr, g, parent, num_arr, closed, end, w,g_h_f)
					closed[0].add(s)
	return False, [], []