import numpy as np


'''
arr = [[1, 3, 4, 1, 2], #need to read this in from a file, this is just a test case
       [2, 3, 2, 3, 1],
       [2, 1, 2, 1, 3],
       [3, 2, 3, 3, 2],
       [4, 1, 2, 1, 0]]
'''


#print (queue.popleft())


def calc_coords (x, y, vector, size):     #calculates the direction of movement from a cell taken from queue
    if x + vector < size:    #checks to see if i,j coords (+/-) the movement value are valid moves
        pos_x = vector              #change vectors
    else:
        pos_x = 0
    if y + vector < size:
        pos_y = vector
    else:
        pos_y = 0
    if x - vector >= 0:
        neg_x = -vector
    else:
        neg_x = 0
    if y - vector >= 0:
        neg_y = -vector
    else:
        neg_y = 0

    directions = [pos_x, pos_y, neg_x, neg_y]
    return directions


def if_seen(x, y, dist_from_start, arr, seen, distance, queue):      #checks if the next cells have been seen, if so they are not revisited
    if seen[x][y] == 0: #if they have not been seen they are marked as seen, given a distance
        seen[x][y] = 1  #and then they are inserted at the back of the queue
        distance[x][y] = dist_from_start + 1
        queue.insert(len(queue), (x, y, arr[x][y], dist_from_start + 1))

def mark_invalid(seen, distance, size):
    for x in range(0,size):
        for y in range(0,size):
            if seen[x][y] == 0:
                distance[x][y] = -1

def solve_puzzle(arr, size):
    seen = np.zeros((size, size), dtype=np.int)                   #initializing the seen array, only 0,1
    distance = np.zeros((size, size), dtype=np.int)               #this is the distance array which should be returned once search is complete    
    queue = []                      #nodes inserted as they are seen
    dist = []                       #distance from the start node
    queue.insert(0, (0, 0, arr[0][0],0)) #insert at front, (x-coord, y-coord, movement distance, distance from start)
    dist.insert(0, arr[0][0])       #distance from the start state, inserting the start state itself, into the first position
    seen[0][0] = 1

    while queue:
        data_tup = queue.pop(0)
        x_coord = data_tup[0]
        y_coord = data_tup[1]
        magnitude = data_tup[2]
        dist_from_start = data_tup[3]
        dire = calc_coords(x_coord, y_coord, magnitude, size)
        #the next four lines are used to validate the moves thats are calculated in
        #calc_coords, these are necessary to make sure we are not re-visiting and cells
        if_seen(x_coord + dire[0], y_coord, dist_from_start, arr, seen, distance, queue)
        if_seen(x_coord, y_coord + dire[1], dist_from_start, arr, seen, distance, queue)
        if_seen(x_coord + dire[2], y_coord, dist_from_start, arr, seen, distance, queue)
        if_seen(x_coord, y_coord + dire[3], dist_from_start, arr, seen, distance, queue)
    mark_invalid(seen,distance,size)
    return distance








