import sys
import random


def setGlobals(input):
    global SIZE, AVGDEGCOUNT, NETWORK, NSTATS
    SIZE = input[0]
    AVGDEGCOUNT = input[1]
    NETWORK = {}
    NSTATS = {}


def genNodes():
    for i in range(SIZE):
        NETWORK[i] = set()


def genConnections():
    edgecount = 0
    while edgecount < (AVGDEGCOUNT * SIZE / 2):
        randnodeone = random.randint(0, SIZE - 1)
        randnodetwo = random.randint(0, SIZE - 1)
        while randnodetwo in NETWORK[randnodeone] or randnodeone == randnodetwo:
            randnodeone = random.randint(0, SIZE - 1)
            randnodetwo = random.randint(0, SIZE - 1)
        NETWORK[randnodeone].add(randnodetwo)
        NETWORK[randnodetwo].add(randnodeone)
        edgecount += 1


def genStats():
    sumt = 0
    for i in NETWORK:
        n = len(NETWORK[i])
        sumt += n
        if n in NSTATS:
            NSTATS[n] += 1
        else:
            NSTATS[n] = 1
    print(sumt)


def findDiameter():
    max = "None"
    for i in NETWORK:
        if max == "None":
            max = i
        elif len(NETWORK[i]) > len(NETWORK[max]):
            max = i
    queue_count = 0
    queue = [max]
    dictSeen = {max: 0}
    while queue_count < len(queue):
        queue[0] = queue[queue_count]
        node = queue[0]
        n = NETWORK[node]
        for p in n:
            if p not in dictSeen:
                queue += [p]
                dictSeen.update({p: dictSeen[node] + 1})
        queue_count += 1
    max1 = "None"
    for i in dictSeen:
        if max1 == "None":
            max1 = i
        elif dictSeen[i] > dictSeen[max1]:
            max1 = i
    queue_count = 0
    queue = [max1]
    dictSeen = {max1: 0}
    while queue_count < len(queue):
        queue[0] = queue[queue_count]
        node = queue[0]
        n = NETWORK[node]
        for p in n:
            if p not in dictSeen:
                queue += [p]
                dictSeen.update({p: dictSeen[node] + 1})
        queue_count += 1
    max = "None"
    for i in dictSeen:
        if max == "None":
            max = i
        elif dictSeen[i] > dictSeen[max]:
            max = i
    return dictSeen[max]


if sys.argv[1:]:
    setGlobals(sys[1:])
else:
    setGlobals([100000, 5])
genNodes()
genConnections()
genStats()
nlist = [s for s in NSTATS]
nlist.sort()
slist = [NSTATS[i] for i in nlist]
print(slist)
print("Diameter: " + str(findDiameter()))
#Average Degree 4, Diameter 18
#Average Degree 5, Diameter 14