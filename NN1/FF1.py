import sys
import math


def setGlobals(input):
    global WEIGHTS, TRANSFER, INPUTS, NETWORK, NODES, LEVELS
    temp_input = []
    NETWORK = {}
    NODES = {}
    LEVELS = {}
    WEIGHTS = {}
    for i in range(len(input)):
        if i == 0:
            f = input[i]
        elif i == 1:
            TRANSFER = input[i]
        else:
            temp_input.append(float(input[i]))
    INPUTS = temp_input
    getWeights(f)


def getWeights(filename):
    global WEIGHTS, TRANSFER, INPUTS, NETWORK, NODES, LEVELS
    temp = open(filename, 'r').read().splitlines()
    w = []
    for t in temp:
        w.append(t.split(" "))
    count = 1
    level = 0
    for i in INPUTS:
        NETWORK[count] = []
        if level not in LEVELS:
            LEVELS[level] = [count]
        else:
            LEVELS[level].append(count)
        count += 1
    level += 1
    for j in range(len(w) - 1):
        connections = w[j]
        num_nodes = len(connections) // len(LEVELS[level - 1])
        for n in range(num_nodes):
            NETWORK[count] = []
            if level not in LEVELS:
                LEVELS[level] = [count]
            else:
                LEVELS[level].append(count)
            for i in LEVELS[level - 1]:
                temp_weight = connections.pop(0)
                WEIGHTS[i, count] = float(temp_weight)
                NETWORK[i].append(count)
            count += 1
        level += 1
    output_weights = w[-1]
    output_per_node = len(output_weights) // len(LEVELS[level - 1])
    for i in LEVELS[level - 1]:
        for j in range(output_per_node):
            NETWORK[i].append(count)
            NETWORK[count] = []
            if level not in LEVELS:
                LEVELS[level] = [count]
            else:
                LEVELS[level].append(count)
            WEIGHTS[i, count] = float(output_weights.pop(0))
            count += 1


def transfer(val):
    if TRANSFER == "T1":
        return val
    if TRANSFER == "T2":
        if val > 0:
            return val
        return 0
    if TRANSFER == "T3":
        return 1 / (1 + math.exp(-val))
    if TRANSFER == "T4":
        return -1 + 2 / (1 + math.exp(-val))


def evaluate():
    for i in range(len(INPUTS)):
        NODES[LEVELS[0][i]] = INPUTS[i]
    level = 0
    while level < len(LEVELS) - 2:
        temp_nodes = LEVELS[level]
        for n in temp_nodes:
            for c in NETWORK[n]:
                if c not in NODES:
                    NODES[c] = 0
                NODES[c] += NODES[n] * WEIGHTS[n, c]
        level += 1
        for n in LEVELS[level]:
            NODES[n] = transfer(NODES[n])
    temp_nodes = LEVELS[level]
    for n in temp_nodes:
        for c in NETWORK[n]:
            if c not in NODES:
                NODES[c] = 0
            NODES[c] += NODES[n] * WEIGHTS[n, c]
    level += 1
    temp_str = ""
    for val in LEVELS[level]:
        temp_str += str(NODES[val]) + " "
    print(temp_str[:-1])

if sys.argv[1:]:
    setGlobals(sys.argv[1:])
else:
    setGlobals(["weights.txt", "T3", "5", "2", "3", "1", "4"])
    #setGlobals(["weights.txt","T2","1","1","1"])
evaluate()

