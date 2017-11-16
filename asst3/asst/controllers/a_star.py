import random, math
import numpy as np
import heapq
import time
from asst.controllers import utils, vertex, fringe

ROWS = 120
COLS = 160

def heur(point, end):
	std = math.hypot(point[0] - end[0], point[1] - end[1])
	return math.sqrt(2)*0.25*(std) + 2*math.sqrt(2) - 0.25*(std)

def solve(num_arr, start, end, w=1):
	goal = vertex.Vertex(end, 0)
	g = {}
	g[utils.coord_id(start)] = 0
	g_h_f = {}
	g_h_f[utils.coord_id(start)] = [0,heur(start, end), w * heur(start, end)]
	parent = {}
	parent[utils.coord_id(start)] = start
	fr = fringe.Fringe()
	fr.insert(vertex.Vertex(start, g[utils.coord_id(start)] + heur(start, end)))
	closed = set()
	
	while len(fr) != 0:
		s = fr.pop()
		if s == goal:
			path = utils.goal_path(start, end, parent)
			return True, path, g_h_f
		closed.add(s)
		for s_p in utils.succ(num_arr,s, closed):
			if s_p not in fr.to_list():
				sp_cid = utils.coord_id([s_p.x, s_p.y])
				g[sp_cid] = math.inf
				parent[sp_cid] = None
			update_vertex(s, s_p, g, parent, fr, end, num_arr,w, g_h_f)
	return False, [], []


def update_vertex(s, s_p, g, parent, fr, end, num_arr, w, g_h_f):
	s_c = [s.x, s.y]
	sp_c = [s_p.x, s_p.y]
	s_cid = utils.coord_id(s_c)
	sp_cid = utils.coord_id(sp_c)
	next_cost = utils.cost(num_arr, s_c, sp_c)
	if g[s_cid] + next_cost < g[sp_cid]:
		g[sp_cid] = g[s_cid] + next_cost
		parent[sp_cid] = s_c
		if s_p in fr.to_list():
			fr.remove(sp_c)
		g_c = g[sp_cid] 
		h_c = heur(sp_c, end)
		f_c = g_c + w * h_c
		g_h_f[utils.coord_id(sp_c)] = [g_c, h_c, f_c]
		fr.insert(vertex.Vertex(sp_c, f_c))