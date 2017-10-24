from random import choice
from copy import deepcopy
from numpy import array, dot, random

unit_step = lambda x: -1 if x < 0 else 1

training_data = [
    (array([1,0.1]), -1),
    (array([1,0.15]), 1),
    (array([1,0.25]), -1),
    (array([1,0.32]), 1),
    (array([1,0.45]), -1),
    (array([1,0.6]), -1),
    (array([1,0.7]), 1),
    (array([1,0.9]), 1),
]

w = [0.2, 1]
errors = []
eta = 1
epoch = 5

best_err = len(training_data)
best = []


for z in range(epoch):
    for i in xrange(len(training_data)):
        x, expected = training_data[i]
        result = dot(w, x)
        error = expected - unit_step(result)
        errors.append(error)
        w += eta * error * x
        tmp_err = 0
        for l in range(len(training_data)):
            x, expected = training_data[l]
            result = dot(w, x)
            if expected != unit_step(result):
                tmp_err = tmp_err + 1
        if tmp_err < best_err:
            print(w)
            print("New best: " + str(tmp_err))
            best = deepcopy(w)
            best_err = tmp_err

# for x, _ in training_data:
#     result = dot(x, w)
#     print("{}: {} -> {}".format(x[1:3], result, unit_step(result)))
print("Best error: " + str(best_err))
print("Weight: " + str(best))