import random



def doBasic(grid, size, iters):
    grid_calc = [random.randint(1, size-1) for x in range(size*size)]
    grid_cost = [random.randint(1, size-1) for x in range(size*size)]
    return grid_calc, grid_cost