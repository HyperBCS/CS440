from random import choice
from numpy import array, dot, random

unit_step = lambda x: -1 if x < 0 else 1

training_data = [
    (array([1,0.1,0.72]), -1),
    (array([1,0.15,1.01]), 1),
    (array([1,0.25,0.55]), -1),
    (array([1,0.32,0.95]), 1),
    (array([1,0.45,0.12]), -1),
    (array([1,0.6,0.3]), -1),
    (array([1,0.7,0.6]), 1),
    (array([1,0.9,0.4]), 1),
]

w = [0.2, 1, -1]
errors = []
eta = 1
epoch = 5

print("Initial Weights: " + str(w))
for z in range(epoch):
    print("Epoch: " + str(z + 1))
    for i in xrange(len(training_data)):
        x, expected = training_data[i]
        result = dot(w, x)
        error = expected - unit_step(result)
        errors.append(error)
        w += eta * error * x
    print("Updated weights: " + str(w))
    tmp_err = 0
    for l in range(len(training_data)):
        x, expected = training_data[l]
        result = dot(w, x)
        if expected != unit_step(result):
            tmp_err = tmp_err + 1
    print("Missclassified: " + str(tmp_err))