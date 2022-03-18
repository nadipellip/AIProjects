import sys
import random


def setGlobals(input):
    global INITPOP, AVGDEGCOUNT, NETWORK, POPULARITY, PEOPLE, AVGDEATH, SDDEATH, TOTALEDGECOUNT
    INITPOP = input[0]
    AVGDEGCOUNT = input[1]
    NETWORK = {}
    POPULARITY = []
    PEOPLE = set()
    AVGDEATH = 79
    SDDEATH = 8
    TOTALEDGECOUNT = 0


def genInitPop():
    global POPULARITY, PEOPLE, TOTALEDGECOUNT
    NETWORK[0, -5] = {(-1, -7), (3, -10)}
    NETWORK[1, -7] = {(0, -5)}
    NETWORK[2, -9] = {(3, -10)}
    NETWORK[3, -10] = {(0, -5), (2, -9)}
    NETWORK[4, -6] = set()
    POPULARITY = [(0, -5), (0, -5), (1, -7), (2, -9), (3, -10), (3, -10)]
    PEOPLE = {(0, -5), (1, -7), (2, -9), (3, -10), (4, -6)}
    TOTALEDGECOUNT = 3
    for i in range(5, INITPOP):
        if i not in PEOPLE:
            randage = random.randint(0, 81)
            createperson(i, -1 * randage)


def simulate():
    year = 0
    print("Year 0")
    print("Population: " + str(len(NETWORK)))
    poptime = [len(NETWORK)]
    while len(NETWORK) < 100000:
        year += 1
        print("Year " + str(year))
        newbirths = birth(year)
        print("Births: " + str(newbirths))
        newdeaths = death(year)
        print("Death: " + str(newdeaths))
        print("Population: " + str(len(NETWORK)))
        poptime.append(len(NETWORK))
    return poptime


def createperson(person, year):
    global TOTALEDGECOUNT
    NETWORK[person, year] = set()
    PEOPLE.add(person)
    if TOTALEDGECOUNT * 2 / len(NETWORK) >= AVGDEGCOUNT:
        randa = random.randint(0, 3)
        for i in range(randa):
            weight_length = len(POPULARITY)
            randnode = random.randint(0, weight_length - 1)
            while POPULARITY[randnode] in NETWORK[person, year] or POPULARITY[randnode] == (person, year):
                randnode = random.randint(0, weight_length - 1)
            NETWORK[person, year].add(POPULARITY[randnode])
            NETWORK[POPULARITY[randnode][0], POPULARITY[randnode][1]].add((person, year))
            POPULARITY.append((POPULARITY[randnode][0], POPULARITY[randnode][1]))
            POPULARITY.append((person, year))
            TOTALEDGECOUNT += 1
    elif TOTALEDGECOUNT * 2 / len(NETWORK) < AVGDEGCOUNT:
        if len(NETWORK) < 13:
            randa = 4
        if len(NETWORK) > 12:
            randa = random.randint(4, 7)
        for i in range(randa):
            weight_length = len(POPULARITY)
            randnode = random.randint(0, weight_length - 1)
            while POPULARITY[randnode] in NETWORK[person, year] or POPULARITY[randnode] == (person, year):
                randnode = random.randint(0, weight_length - 1)
            # print(NETWORK)
            NETWORK[person, year].add(POPULARITY[randnode])
            NETWORK[POPULARITY[randnode][0], POPULARITY[randnode][1]].add((person, year))
            POPULARITY.append((POPULARITY[randnode][0], POPULARITY[randnode][1]))
            POPULARITY.append((person, year))
            TOTALEDGECOUNT += 1


def birth(year):
    newperson = len(PEOPLE)
    births = 0
    for i in NETWORK:
        if random.random() * 1000 <= 18.5:
            births += 1
    for b in range(births):
        createperson(newperson, year)
        newperson += 1
    return births


def death(year):
    remove = set()
    for i in NETWORK:
        age = year - i[1]
        if int(random.gauss(AVGDEATH, SDDEATH) <= age):
            remove.add(i)
    kill(remove)
    return len(remove)


def kill(remnode):
    global TOTALEDGECOUNT, POPULARITY
    POPULARITY = [p for p in POPULARITY if p not in remnode]
    # print("Hello")
    for node in remnode:
        connections = NETWORK[node]
        del NETWORK[node]
        for c in connections:
            NETWORK[c].remove(node)
            TOTALEDGECOUNT += -1


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
        if node in NETWORK:
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
        if node in NETWORK:
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

def genStats():
    slist = [0]
    for i in NETWORK:
        n = len(NETWORK[i])
        while len(slist) <= n:
            slist.append(0)
        slist[n] += 1
    return slist

if sys.argv[1:]:
    setGlobals(sys.argv[1:])
else:
    setGlobals([80000, 6])
    genInitPop()
    # print(NETWORK)
    print(simulate())
    print(genStats())
    print(findDiameter())
