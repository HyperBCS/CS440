import random, math
import numpy as np
import heapq
import time
from copy import deepcopy
from asst.controllers import utils, vertex

class Fringe(object):

	def __init__(self, prior = True):
		self.prior = prior
		self.fringe = []

	def insert(self, s ):
		if self.prior:
			heapq.heappush(self.fringe, s)
		else:
			self.fringe.append(s)

	def remove(self, s):
		cid = utils.coord_id(s)
		for obj in self.fringe[:]:
			if cid == obj.cid:
				self.fringe.remove(obj)

	def minkey(self):
		if len(self.fringe) > 0:
			if self.prior:
				return self.fringe[0]
			else:
				return heapq.nsmallest(1,self.fringe)[0]
		else:
			return None

	def top(self):
		if len(self.fringe) > 0:
			return self.fringe[0]
		else:
			return None

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