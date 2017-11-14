import random, math
import numpy as np
import heapq
import time
from copy import deepcopy

ROWS = 120
COLS = 160

def coord_id(coord):
	return coord[0] * COLS + coord[1]


def solve(num_arr, start, end):
	g = {}
	g[coord_id(start)] = 0
	parent = {}
	parent[coord_id(start)] = start
	fringe = []
	return "hello"


def update_vertex(s, s_p):
	return "hello"