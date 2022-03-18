from math import pi, acos, sin, cos
import sys
import heapq
from tkinter import *
from random import randint
import time


class PriorityQueue():
    def __init__(self):
        self.queue = []

    def next(self):
        if self.current >= len(self.queue):
            self.current
            raise StopIteration

        out = self.queue[self.current]
        self.current += 1

        return out

    def __iter__(self):
        return self

    __next__ = next

    def isEmpty(self):
        return len(self.queue) == 0

    ''' complete the following functions '''

    def remove(self, index):
        # remove self.queue[index]
        self.queue.pop(index)
        heapq.heapify(self.queue)
        return self.queue[index]

    def pop(self):
        # swap first and last. Remove last. Heap down from first.
        # return the removed value
        temp = self.queue[0]
        heapq.heappop(self.queue)
        return temp

    def push(self, value):
        # append at last. Heap up.
        heapq.heappush(self.queue, value)
        pass

    def peek(self):
        # return min value (index 0)
        return self.queue[0]


def calcd(y1, x1, y2, x2):
    #
    # y1 = lat1, x1 = long1
    # y2 = lat2, x2 = long2
    # all assumed to be in decimal degrees

    # if (and only if) the input is strings
    # use the following conversions

    y1 = float(y1)
    x1 = float(x1)
    y2 = float(y2)
    x2 = float(x2)
    #
    R = 3958.76  # miles = 6371 km
    #
    y1 *= pi / 180.0
    x1 *= pi / 180.0
    y2 *= pi / 180.0
    x2 *= pi / 180.0
    #
    # approximate great circle distance with law of cosines
    #
    temp = sin(y1) * sin(y2) + cos(y1) * cos(y2) * cos(x2 - x1)
    if temp < 1:
        return acos(sin(y1) * sin(y2) + cos(y1) * cos(y2) * cos(x2 - x1)) * R
    return acos(1) * R


def makeGraph(edgefile):
    edges = open(edgefile, 'r').read().splitlines()
    myGraph = {}
    for e in edges:
        n1, n2 = e[:7], e[8:]
        if n1 not in myGraph:
            myGraph[n1] = set()
        if n2 not in myGraph:
            myGraph[n2] = set()
        myGraph[n1].add(n2)
        myGraph[n2].add(n1)
    return myGraph


def getNodes(nodefile):
    nodes = open(nodefile, 'r').read().splitlines()
    nvalues = {}
    for n in nodes:
        n1, n2, n3 = n[:7], n[8:17], n[18:]
        nvalues[n1] = (n2, n3)
    return nvalues


def getCities(cityfile):
    cities = open(cityfile, 'r').read().splitlines()
    cvalues = {}
    for c in cities:
        c1, c2 = c[:7], c[8:]
        cvalues[c2] = c1
    return cvalues


def solve(input_line, cfile="CityNodes.txt", nfile="rrNodes.txt", efile="rrEdges.txt"):
    myGraph = makeGraph(efile)
    nodes = getNodes(nfile)
    cities = getCities(cfile)
    start = time.time()
    scity = ""
    ecity = ""
    for i in input_line:
        if scity == "" or scity not in cities:
            if scity == "":
                scity += i
            else:
                scity += " " + i
        else:
            if ecity == "":
                ecity += i
            else:
                ecity += " " + i
    snode = cities[scity]
    enode = cities[ecity]
    if scity == ecity:
        return 0.0
    ROOT = Tk()  # creates new tkinter
    ROOT.title("A*")
    canvas = Canvas(ROOT, background='black')  # sets background
    drawCircle(canvas, nodes[snode][0], nodes[snode][1], "pink", 5)
    drawCircle(canvas, nodes[enode][0], nodes[enode][1], "green", 5)
    draw_all_edges(ROOT, canvas, myGraph, nodes)
    f = calcd(float(nodes[snode][0]), float(nodes[snode][1]), float(nodes[enode][0]), float(nodes[enode][1]))
    openSet = PriorityQueue()
    openSet.push((f, snode, '', 0.0))
    closedSet = {}
    circles = {}
    while openSet:
        f, stop, parent, dt = openSet.pop()
        if parent != '':
            drawLine(canvas, nodes[parent][0], nodes[parent][1], nodes[stop][0], nodes[stop][1], 'blue')
        if stop not in closedSet:
            closedSet[stop] = (parent, dt)
            for nbr in myGraph[stop]:
                h = calcd(float(nodes[nbr][0]), float(nodes[nbr][1]), float(nodes[enode][0]), float(nodes[enode][1]))
                g = calcd(float(nodes[nbr][0]), float(nodes[nbr][1]), float(nodes[stop][0]), float(nodes[stop][1])) + \
                    closedSet[stop][1]
                newF = h + g
                openSet.push((newF, nbr, stop, g))
                if nbr not in closedSet:
                    drawLine(canvas, nodes[stop][0], nodes[stop][1], nodes[nbr][0], nodes[nbr][1], 'red')
                if nbr == enode:
                    closedSet[enode] = (parent, newF)
                    print(backtrack(closedSet, enode, cities, canvas, nodes))
                    print(str(newF) + "mi")
                    while True:
                        ROOT.mainloop()
            if randint(0, int(newF ** (1/2))) == randint(0, int(newF**(1/2))):
                ROOT.update()
    ROOT.mainloop()


def backtrack(dict, goal, cities, canvas, nodes):
    c = {cities[key]: key for key in cities}
    path = []
    key = goal
    while key != "":
        if key in c:
            path = [c[key] + ", " + str(dict[key][1]) + "mi"] + path
        else:
            path = [key + ", " + str(dict[key][1]) + "mi"] + path
        newkey = dict[key][0]
        if newkey != "":
            drawLine(canvas, nodes[key][0], nodes[key][1], nodes[newkey][0], nodes[newkey][1], 'yellow')
        key = newkey
    print("Stations:"  + str(len(path)))
    return str(path)


def draw_all_edges(ROOT, canvas, edges, nodes):
    ROOT.geometry("1200x800")  # sets geometry
    canvas.pack(fill=BOTH, expand=1)  # sets fill expand
    for e in edges:  # graph[4] keys are edge set
        for n in edges[e]:
            drawLine(canvas, nodes[e][0], nodes[e][1], nodes[n][0], nodes[n][1], 'white')  # graph[5] is map dict
    ROOT.update()


def drawLine(canvas, y1, x1, y2, x2, col, **kwargs):
    x1, y1, x2, y2 = float(x1), float(y1), float(x2), float(y2)
    return canvas.create_line((x1) * 10 + 1500, (50 - y1) * 10 + 400, (x2) * 10 + 1500, (50 - y2) * 10 + 400, fill=col, **kwargs)


def drawCircle(canvas, y1, x1, col, r=2):
    x1, y1 = float(x1), float(y1)
    return canvas.create_oval(((x1) * 10 + 1500) - r, ((50 - y1) * 10 + 400) - r, ((x1) * 10 + 1500) + r,
                              ((50 - y1) * 10 + 400) + r, fill=col)


l = sys.argv
solve(l[1:])
#solve(["Miami", "Merida"])
