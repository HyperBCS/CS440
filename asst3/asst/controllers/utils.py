import random, math
import numpy as np
import heapq
import time
from copy import deepcopy

ROWS = 120
COLS = 160

def coord_id(coord):
	return coord[0] * COLS + coord[1]