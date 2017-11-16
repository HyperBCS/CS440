import random, math
import numpy as np
import heapq
import time
from asst.controllers import utils, vertex, fringe

ROWS = 120
COLS = 160

def solve(num_arr, start, end):
	goal = vertex.Vertex(end, 0)
	# g is now cost
	g = {}
	g[utils.coord_id(start)] = 0
	parent = {}
	parent[utils.coord_id(start)] = start
	fr = fringe.Fringe()
	fr.insert(vertex.Vertex(start, 0))
	closed = set()
	
	while len(fr) != 0:
		s = fr.pop()
		s_c = [s.x, s.y]
		if s == goal:
			path = utils.goal_path(start, end, parent)
			return True, path, g
		closed.add(s)
		for s_p in utils.succ(num_arr,s, closed):
			sp_c = [s_p.x, s_p.y]
			sp_cid = utils.coord_id(sp_c)
			ch_cost = s.g_h + utils.cost(num_arr,s_c, sp_c)
			if s_p not in fr.to_list() and s_p not in closed:
				g[sp_cid] = ch_cost
				parent[sp_cid] = s_c
				fr.insert(vertex.Vertex(sp_c, ch_cost))
			elif s_p in fr.to_list() and ch_cost < s.g_h:
				fr.update(s_p, ch_cost)
				g[sp_cid] = ch_cost
				parent[sp_cid] = s_c
	return False, [], []