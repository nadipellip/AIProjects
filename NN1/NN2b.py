import sys
import math
import random
import time


def setGlobals(input):
    global TRAINING, NUM_INPUTS, ALPHA, INIT_TIME
    INIT_TIME = time.time()
    TRAINING = {}
    ALPHA = 0.05
    num_inputs = 0
    filename = input[0]
    training_file = open(filename, 'r').read().splitlines()
    for t in training_file:
        """temp_inputs = t[:t.find(">=") - 1]
        output = float(t[t.find("=") + 2:])
        inputs = [float(i) for i in temp_inputs.split(" ")]"""
        inputs = []
        bool = False
        output = 0
        for i in range(len(t)):
            if t[i] == " ":
                continue
            else:
                if t[i] == "=" or t[i] == ">":
                    bool = True
                elif not bool:
                    inputs.append(float(t[i]))
                elif bool:
                    output = float(t[i])
        inputs += [1.0]
        if num_inputs == 0:
            num_inputs = len(inputs)
            NUM_INPUTS = num_inputs
        TRAINING[tuple(inputs)] = output


def gen_init_network(structure):
    network = []
    for level in range(len(structure) - 1):
        network.append(
            [{'w': [random.random() for i in range(structure[level])]} for i in range(structure[level + 1])])
    return network


def dot(weights, inputs):
    activation = 0
    for i in range(len(weights)):
        activation += weights[i] * inputs[i]
    return activation


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


def feed_forward(network, inputs):
    for layer in network:
        new_inputs = []
        for neuron in layer:
            activation = dot(neuron['w'], inputs)
            neuron['o'] = sigmoid(activation)
            new_inputs.append(neuron['o'])
        inputs = new_inputs
    return inputs


def sigmoid_derivative(val):
    return sigmoid(val) * (1 - sigmoid(val))


def back_prop(network, expected):
    for i in reversed(range(len(network))):
        layer = network[i]
        errors = list()
        if i != len(network) - 1:
            for j in range(len(layer)):
                error = 0.0
                for neuron in network[i + 1]:
                    error += (neuron['w'][j] * neuron['d'])
                errors.append(error)
        else:
            for j in range(len(layer)):
                neuron = layer[j]
                errors.append(expected[j] - neuron['o'])
        for j in range(len(layer)):
            neuron = layer[j]
            neuron['d'] = errors[j] * sigmoid_derivative(neuron['o'])
    return network


def update_weights(network, inputs):
    for i in range(len(network)):
        if i != 0:
            inputs = [neuron['o'] for neuron in network[i - 1]]
        for neuron in network[i]:
            for j in range(len(inputs)):
                neuron['w'][j] += ALPHA * neuron['d'] * inputs[j]
            neuron['w'][-1] += ALPHA * neuron['d']
    return network


def train_network(network):
    global TRAINING, ALPHA
    error_sum = math.inf
    epoch = 0
    while error_sum > 0.01:
        if epoch > 125000 and error_sum > 0.499:
            epoch = 0
            network = gen_init_network([NUM_INPUTS,2,2,1])
        error_sum = 0
        for input in TRAINING:
            output = feed_forward(network, input)[0]
            expected = [TRAINING[input]]
            error_sum += (output - expected[0]) ** 2 / 2
            network = back_prop(network, expected)
            network = update_weights(network, input)
        print("Epoch: " + str(epoch) + ", " + str(error_sum))
        epoch += 1
    return network


def output_network(network):
    output_str = ""
    for layer in network:
        temp_str = ""
        for neuron in layer:
            temp_str += str(neuron['w']).replace("[", "").replace("]", "").replace(","," ") + " "
        output_str += temp_str[:-1]
        output_str += "\n"
    print(output_str)
if sys.argv[1:]:
    setGlobals(sys.argv[1:])
else:
    setGlobals(["training_sample.txt"])
#print(TRAINING)
print("Layer count: " + str([NUM_INPUTS, 2, 1, 1]).replace("[","").replace("]","").replace(",",""))
network = gen_init_network([NUM_INPUTS, 2, 1, 1])
network = train_network(network)
#print("Weights")
output_network(network)
print("Time: " + str(time.time()-INIT_TIME) +"s")