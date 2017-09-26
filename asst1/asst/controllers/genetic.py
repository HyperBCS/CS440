import random, math
import numpy as np
import time
from copy import deepcopy
from operator import itemgetter
from asst.controllers import solver


def doGenetic(grid, size, iters, initial_pop, num_child, mutation_rate):
    current_pop = []
    if initial_pop % 2 == 1:
        initial_pop += 1
    for i in range(initial_pop):
        grid_gen, value_gen = generate_rand_grid(size)
        current_pop.append([grid_gen, value_gen])
    current_pop.sort(key=itemgetter(1), reverse=True)
    for j in range(iters):
        children = []
        for k in range(0, len(current_pop)-1, 2):
            for ch in range(num_child):
                curr_parent1 = deepcopy(current_pop[k][0])
                curr_parent2 = deepcopy(current_pop[k+1][0])
                while True:
                    rand_x = random.sample(range(0, (size)), 2)
                    rand_y = random.sample(range(0, (size)), 2)
                    rand_x_start = rand_x[0]
                    rand_x_end = rand_x[1]
                    rand_y_start = rand_y[0]
                    rand_y_end = rand_y[1]

                    if rand_x_start >= rand_x_end:
                        temp = rand_x_start
                        rand_x_start = rand_x_end
                        rand_x_end = temp
                    if rand_y_start >= rand_y_end:
                        temp = rand_y_start
                        rand_y_start = rand_y_end
                        rand_y_end = temp
                    if [rand_x_end,rand_y_end] != [size-1,size-1]:
                        break
                tmp_chromo1 = []
                tmp_chromo2 = []
                for num in range(rand_x_start,rand_x_end):
                    for num2 in range(rand_y_start,rand_y_end):
                        tmp_chromo1.append(curr_parent1[num][num2])
                        tmp_chromo2.append(curr_parent2[num][num2])
                count = 0
                rand_val1 = random.uniform(0, 1)
                rand_val2 = random.uniform(0, 1)
                for num in range(rand_x_start,rand_x_end):
                    for num2 in range(rand_y_start,rand_y_end):
                        if rand_val1 < mutation_rate:
                            tmp_chromo1[count] = random.randint(1, (size)-1)
                        if rand_val2 < mutation_rate:
                            tmp_chromo2[count] = random.randint(1, (size)-1)
                        curr_parent1[num][num2] = tmp_chromo2[count]
                        curr_parent2[num][num2] = tmp_chromo1[count]
                        count += 1
                children.append(curr_parent1)
                children.append(curr_parent2)
        if len(children) % 2 == 1:
            children = children[:len(children) - 2]
        current_pop = []
        for l in children:
            grid2, value, solution = solver.solve_puzzle(l, size)
            current_pop.append([l, value])
        current_pop.sort(key=itemgetter(1), reverse=True)
        # for i in current_pop:
        #     print(i[1])
        # print("--------------------")
        current_pop = current_pop[:initial_pop]

    best_grid = np.array(current_pop[-1][0]).tolist()
    best_grid_s, best_val, best_sol = solver.solve_puzzle(best_grid, size)
    best_grid = [item for sublist in best_grid for item in sublist]
    best_grid_s = np.array(best_grid_s).tolist()
    best_grid_s = [item for sublist in best_grid_s for item in sublist]
    if best_val > 0:
        best_sol = "Puzzle Value: " + str(best_val) + "\n" + best_sol
        # best_sol = "Puzzle Value: " + str(best_val) + "\n" + best_sol + "\nIterations: " + str(i) + "\nCompute Time: " + "{0:.2f}".format(end - start) + "s"
        
    return best_grid, best_grid_s, best_val, best_sol

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
            return num_arr, value

