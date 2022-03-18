import sys
import math
import random


def setGlobals(input):
    global TRAINING, NUM_INPUTS, NETWORK, WEIGHTS, ALPHA
    ALPHA = 0.05
    NETWORK = {}
    WEIGHTS = {}
    NUM_INPUTS = 0
    TRAINING = {}
    num_inputs = 0
    filename = input[0]
    training_file = open(filename, 'r').read().splitlines()
    for t in training_file:
        temp_inputs = t[:t.find(">=") - 1]
        output = float(t[t.find("=") + 2:])
        inputs = [float(i) for i in temp_inputs.split(" ")]
        if num_inputs == 0:
            num_inputs = len(inputs)
            NUM_INPUTS = num_inputs
        inputs += [1.0]
        TRAINING[(i for i in inputs)] = output


def gen_init_network():
    global TRAINING, NUM_INPUTS, NETWORK, WEIGHTS, ALPHA
    for level in range(4):
        if level == 0:
            if NUM_INPUTS == 3:
                NETWORK[(0, 0)] = {(1, 0), (1, 1)}
                NETWORK[(0, 1)] = {(1, 0), (1, 1)}
                NETWORK[(0, 2)] = {(1, 0), (1, 1)}
                NETWORK[(0, 3)] = {(1, 0), (1, 1)}
            if NUM_INPUTS == 2:
                NETWORK[(0, 0)] = {(1, 0), (1, 1)}
                NETWORK[(0, 1)] = {(1, 0), (1, 1)}
                NETWORK[(0, 2)] = {(1, 0), (1, 1)}
            if NUM_INPUTS == 1:
                NETWORK[(0, 0)] = {(1, 0), (1, 1)}
                NETWORK[(0, 1)] = {(1, 0), (1, 1)}
        if level == 1:
            NETWORK[(1, 0)] = {(2, 0)}
            NETWORK[(1, 1)] = {(2, 0)}
        if level == 2:
            NETWORK[(2, 0)] = {(3, 0)}
        if level == 3:
            NETWORK[3, 0] = set()


def gen_init_weights():
    global TRAINING, NUM_INPUTS, NETWORK, WEIGHTS, ALPHA
    for node in NETWORK:
        connections = NETWORK[node]
        for c in connections:
            WEIGHTS[(node, c)] = random.random()


def sigmoid(val):
    if val < 0:
        try:
            return_val = 1.0 / (1 + math.exp(-val))
        except OverflowError:
            return_val = 0
        return return_val
    else:
        if val < 100:
            return_val = 1.0 / (1 + math.exp(-val))
        else:
            return_val = 1
        return return_val


def sigmoid_derivative(val):
    return sigmoid(val) * (1 - sigmoid(val))


def evaluate(input):
    global TRAINING, NUM_INPUTS, NETWORK, WEIGHTS, ALPHA
    NODES = {}
    count = 0
    for i in input:
        NODES[0, count] = i
        count += 1
    for level in range(1, 4):
        count = 0
        while (level, count) in NETWORK:
            count_two = 0
            NODES[(level, count)] = 0
            while (level - 1, count_two) in NETWORK:
                NODES[(level, count)] += NODES[(level - 1, count_two)] * WEIGHTS[
                    ((level - 1, count_two), (level, count))]
                count_two += 1
            if level < 3:
                NODES[(level, count)] = sigmoid(NODES[(level, count)])
            if level == 3:
                return NODES[level, 0]
            count += 1


def training():
    error = math.inf
    while error > 0.5:
        partial_sum = 0
        
def outputWeights():
    print(WEIGHTS)
if sys.argv[1:]:
    setGlobals(sys.argv[1:])
else:
    setGlobals(["training_sample.txt"])
gen_init_network()
gen_init_weights()
print(WEIGHTS)
