import random, math
import numpy as np
import time
from copy import deepcopy
from asst.controllers import solver, hill

# Basic hill climbing method
def doBasic(grid, size, iters, prob = 0):
    grid2, value, solution = solver.solve_puzzle(grid, size)
    best_val = value
    best_found = False
    best_grid = deepcopy(grid)
    grid_gen = deepcopy(grid)
    best_grid_s = deepcopy(grid2)
    best_sol = solution
    # Iterate for the number we specify
    for i in range(iters):
        rand_val = random.uniform(0, 1)
        prev_grid = deepcopy(grid_gen)
        grid_gen, grid_s, value_gen, solution_s = generate_grid(grid_gen, size)
        # print("BEST: " + str(best_val) + "\nGEN: " + str(value_gen) + "\nRAND: " + str(rand_val) + "\n------------")
        # If the value we generate is better than the best we make a new global best. Also if the value is the same we do not
        # consider a new max found, but still set the current puzzle as best.
        if value_gen >= best_val:
            if not value_gen == best_val:
                best_found = True
            best_val = value_gen
            best_grid = grid_gen
            best_grid_s = grid_s
            best_sol = solution_s
        # For random walk we determine if we should accept the new puzzle or not to go downhill
        elif best_found and rand_val > prob:
            grid_gen = prev_grid
    best_grid = np.array(best_grid).tolist()
    best_grid = [item for sublist in best_grid for item in sublist]
    best_grid_s = np.array(best_grid_s).tolist()
    best_grid_s = [item for sublist in best_grid_s for item in sublist]
    if best_val > 0:
        best_sol = "Puzzle Value: " + str(best_val) + "\n" + best_sol
        # best_sol = "Puzzle Value: " + str(best_val) + "\n" + best_sol + "\nIterations: " + str(i) + "\nCompute Time: " + "{0:.2f}".format(end - start) + "s"
        
    return best_grid, best_grid_s, best_val, best_sol, i + 1


# Performs the annealing method
def doAnneal(grid, size, iters, temp_init, decay):
    grid2, value, solution = solver.solve_puzzle(grid, size)
    best_val = value
    prev_val = best_val
    best_found = False
    best_grid = deepcopy(grid)
    grid_gen = deepcopy(grid)
    best_grid_s = deepcopy(grid2)
    best_sol = solution
    accept_prob = 1
    for i in range(iters):
        prev_grid = deepcopy(grid_gen)
        grid_gen, grid_s, value_gen, solution_s = generate_grid(grid_gen, size)
        try:
            # Calculate the acceptance probability
            accept_prob = math.exp((value_gen - prev_val) / (1.0 * temp_init))
        except:
            accept_prob = 1
        rand_val = random.uniform(0, 1)    
        # print("Prev Val: " + str(prev_val) + "\nGen Val: " + str(value_gen) + "\nTemp: " + str(temp_init) + "\nAccept prob: " + str(accept_prob)  + "\nRandom Value: " + str(rand_val) + "\n---------------")
        prev_val = value_gen
        if value_gen >= best_val:
            best_found = True
            best_val = value_gen
            best_grid = grid_gen
            best_grid_s = grid_s
            best_sol = solution_s
        elif rand_val > accept_prob:
            grid_gen = prev_grid
        temp_init *= decay
        temp_init = max(.01, temp_init)
    best_grid = np.array(best_grid).tolist()
    best_grid = [item for sublist in best_grid for item in sublist]
    best_grid_s = np.array(best_grid_s).tolist()
    best_grid_s = [item for sublist in best_grid_s for item in sublist]
    if best_val > 0:
        best_sol = "Puzzle Value: " + str(best_val) + "\n" + best_sol
        # best_sol = "Puzzle Value: " + str(best_val) + "\n" + best_sol + "\nIterations: " + str(i) + "\nCompute Time: " + "{0:.2f}".format(end - start) + "s"
        
    return best_grid, best_grid_s, best_val, best_sol, i + 1

def generate_grid(grid, size):
    orig_grid = deepcopy(grid)
    while True: 
        rand_coord = [random.randint(0, size-1), random.randint(0, size-1)]
        rand_mag = random.randint(1, size-1)
        if not (rand_coord == [size-1,size-1]) and rand_mag != grid[rand_coord[0]][rand_coord[1]]:
            grid_gen = grid[:]
            grid_gen[rand_coord[0]][rand_coord[1]] = rand_mag
            grid_s, value_gen, solution_s = solver.solve_puzzle(grid_gen, size)
            if value_gen > 0:
                return grid_gen, grid_s, value_gen, solution_s
            else:
                grid = deepcopy(orig_grid)

def generate_rand_grid(n):
    while True:
        num_arr = []
        for i in range(0,n):
            row = []
            for j in range(0,n):
                row.append(random.randint(1,n-1))
            num_arr.append(row)
        num_arr[n-1][n-1] = 0
        grid2, value, solution = solver.solve_puzzle(num_arr, n)
        if value > 0:
            return num_arr


def doRestart(grid, size, iters, iters_per):
    grid2, value, solution = solver.solve_puzzle(grid, size)
    best_val = value
    new_best = False
    best_grid = deepcopy(grid)
    grid_gen = deepcopy(grid)
    best_grid_s = deepcopy(grid2)
    best_sol = solution
    start = time.time()
    it = 0
    for i in range(iters):
        grid_gen = generate_rand_grid(size)
        grid_g, grid_s, value_gen, solution_s, iters = doBasic(grid_gen, size, iters_per)
        it += iters
        if value_gen >= best_val:
            new_best = True
            best_val = value_gen
            best_grid = grid_gen
            best_grid_s = grid_s
            best_sol = solution_s
    end = time.time()
    best_grid = np.array(best_grid).tolist()
    best_grid = [item for sublist in best_grid for item in sublist]
    best_grid_s = np.array(best_grid_s).tolist()
    if len(best_grid_s) <= size:
        best_grid_s = [item for sublist in best_grid_s for item in sublist]
    if not new_best:
        best_sol = "Puzzle Value: " + str(best_val) + "\n" + best_sol
    return best_grid, best_grid_s, best_val, best_sol, it