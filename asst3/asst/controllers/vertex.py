import random, math
import numpy as np
import heapq
import time
from copy import deepcopy
from asst.controllers import utils

ROWS = 120
COLS = 160

class Vertex(object):

	def __init__(self, point, g_h):
		self.x = point[0]
		self.y = point[1]
		self.g_h = g_h
		self.cid = utils.coord_id(point)
		# # calc g(s)
		# self.g = math.hypot(point[0] - start[0], point[1] - start[1])
		# # calc h(s)
		# self.h = math.hypot(point[0] - end[0], point[1] - end[1])

	def __eq__(self, point1):
		id1 = point1.x* COLS + point1.y
		return True if id1 == self.cid else False

	def __ne__(self, point1):
		return not self.__eq__(point1)

	def __lt__(self, point1):
		return True if self.g_h < point1.g_h else False

	def __le__(self, point1):
		return True if self.g_h <= point1.g_h else False

	def __gt__(self, point1):
		return True if self.g_h > point1.g_h else False

	def __ge__(self, point1):
		return True if self.g_h >= point1.g_h else False

	def __hash__(self):
		return self.cid



