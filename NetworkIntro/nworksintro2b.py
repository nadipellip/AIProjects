import sys
import random


def setGlobals(input):
    global SIZE, AVGDEGCOUNT, TOTALDEGCOUNT, NETWORK, POPULARITY, NSTATS
    SIZE = input[0]
    AVGDEGCOUNT = input[1]
    TOTALDEGCOUNT = AVGDEGCOUNT * SIZE / 2
    NETWORK = {}
    POPULARITY = []
    NSTATS = {}


def geninitNetwork():
    global POPULARITY
    NETWORK[0] = {1, 3}
    NETWORK[1] = {0}
    NETWORK[2] = {3}
    NETWORK[3] = {0, 2}
    NETWORK[4] = set()
    POPULARITY = [0, 0, 1, 2, 3, 3,4]


def genConnections():
    # Add each node as singletons or attached to node
    # Use two weighted choices to make rest of connections
    edgecount = 3
    for i in range(SIZE):
        if i not in NETWORK:
            weight_length = len(POPULARITY)
            randnode = random.randint(0, weight_length)
            POPULARITY.append(i)
            if randnode == weight_length:
                NETWORK[i] = set()
            else:
                NETWORK[i] = {POPULARITY[randnode]}
                if POPULARITY[randnode] in NETWORK:
                    NETWORK[POPULARITY[randnode]].add(i)
                else:
                    NETWORK[POPULARITY[randnode]] = {i}
                POPULARITY.append(i)
                POPULARITY.append(POPULARITY[randnode])
                edgecount += 1
        if edgecount == TOTALDEGCOUNT:
            return
    # print(NETWORK)
    while edgecount < TOTALDEGCOUNT:
        weight_length = len(POPULARITY)
        randnodeone = random.randint(0, weight_length - 1)
        randnodetwo = random.randint(0, weight_length - 1)
        while POPULARITY[randnodeone] == POPULARITY[randnodetwo] or POPULARITY[randnodetwo] in NETWORK[POPULARITY[randnodeone]]:
            randnodeone = random.randint(0, weight_length - 1)
            randnodetwo = random.randint(0, weight_length - 1)
        NETWORK[POPULARITY[randnodeone]].add(POPULARITY[randnodetwo])
        NETWORK[POPULARITY[randnodetwo]].add(POPULARITY[randnodeone])
        POPULARITY.append(POPULARITY[randnodeone])
        POPULARITY.append(POPULARITY[randnodetwo])
        edgecount += 1
    return


def genStats():
    for i in NETWORK:
        n = len(NETWORK[i])
        if n in NSTATS:
            NSTATS[n] += 1
        else:
            NSTATS[n] = 1


if sys.argv[1:]:
    setGlobals(sys.argv[1:])
else:
    setGlobals([100000, 4])
    geninitNetwork()
    genConnections()
    genStats()
    nlist = [s for s in NSTATS]
    nlist.sort()
    slist = [NSTATS[i] for i in nlist]
    print(slist)
