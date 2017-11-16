import random, math
import numpy as np
import heapq
import time
from copy import deepcopy
from asst.controllers import utils, vertex

class Fringe(object):

	def __init__(self):
		self.fringe = []

	def insert(self, s):
		heapq.heappush(self.fringe, s)

	def remove(self, s):
		cid = utils.coord_id(s)
		for obj in self.fringe[:]:
			if cid == obj.cid:
				self.fringe.remove(obj)

	def get_vert(self, s):
		cid = utils.coord_id(s)
		for obj in self.fringe[:]:
			if cid == obj.cid:
				return obj

	def upd_vert(self, s, g_h):
		cid = utils.coord_id(s)
		for obj in self.fringe[:]:
			if cid == obj.cid:
				obj.g_h = g_h
				heapq.heapify(self.fringe)
				return True
		return False

	def pop(self):
		try:
			return heapq.heappop(self.fringe)
		except:
			return None

	def __len__(self):
		return len(self.fringe)

	def to_list(self):
		return self.fringe