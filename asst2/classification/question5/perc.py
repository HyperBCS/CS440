from random import choice
from numpy import array, dot, random

unit_step = lambda x: -1 if x < 0 else 1

training_data = [
    (array([1,0.02,0.48]), -1),
    (array([1,0.095,0.72]), 1),
    (array([1,0.13,1.1]), -1),
    (array([1,0.195,0.5]), 1),
    (array([1,0.22,0.3]), 1),
    (array([1,0.33,0.33]), 1),
    (array([1,0.35,0.78]), -1),
    (array([1,0.41,0.49]), 1),
    (array([1,0.52,0.22]), -1),
    (array([1,0.7,0.66]), -1),
    (array([1,0.79,0.27]), -1),
    (array([1,0.92,0.45]), -1),
]

w = [0.8, -1, 1]
errors = []
eta = 1
epoch = 30


for z in range(epoch):
    for i in xrange(len(training_data)):
        x, expected = training_data[i]
        result = dot(w, x)
        # if unit_step(result) != expected:
        #     print("[" + str(z) + "]" + "Expected " + str(expected) + " but got " + str(unit_step(result)))
        error = expected - unit_step(result)
        errors.append(error)
        w += eta * error * x
    print w

e = 0
for x, _ in training_data:
    result = dot(x, w)
    if unit_step(result) != _:
        e = e + 1
    print("{}: {} -> {}".format(x[1:3], result, unit_step(result)))

print(w)
print("Error: ",e)