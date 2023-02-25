# Programming Assignment #1 CS124 Aneesh Muppidi and Eric Li
# usage: python3 randmst.py 0 numpoints numtrials dimension

import random
import math
import sys
import time
from collections.abc import MutableMapping


class vertexHeap(MutableMapping):
    # Define abtract methods 
    def __init__(self, *args, **kw):

        self.vDict = {}
        self.vHeap = []
        self.update(*args, **kw)

    def __setitem__(self, key, value):
        if key in self.vDict:
            self.pop(key)
            
        v = [value, key, len(self)]
        self.vHeap.append(v)
        self.vDict[key] = v

        self.update_key(len(self.vHeap)-1)

    def __delitem__(self, key):
        v = self.vDict[key]
        while v[2]:
            parentInd = (v[2] - 1) >> 1
            parent = self.vHeap[parentInd]
            self.vSwap(v[2], parent[2])
        self.pop()

    def __getitem__(self, key):
        return self.vDict[key][0]

    def __iter__(self):
        return iter(self.vDict)

    def __len__(self):
        return len(self.vDict)

    def pop(self):
        v = self.vHeap[0]

        # If there is only one vertex, then pop
        if len(self.vHeap) == 1:
            self.vHeap.pop()
        else:

        # But if there are more, we need to re-"heapify"
            self.vHeap[0] = self.vHeap.pop()
            self.vHeap[0][2] = 0
            self.heapify(0)

        del self.vDict[v[1]]
        return v[1], v[0]

    def clear(self):
        del self.vHeap[:]
        self.vDict.clear()

    def heapify(self, i):

        while len(self.vHeap) > 0:
            # Find offsets of children vertices (use bit shift operator)
            l = (i << 1) + 1
            r = (i + 1) << 1
            if l < len(self.vHeap) and self.vHeap[l][0] < self.vHeap[i][0]:
                min = l
            else:
                min = i
            if r < len(self.vHeap) and self.vHeap[r][0] < self.vHeap[min][0]:
                min = r
                
            # Found position     
            if min == i:
                break

            self.vSwap(i, min)
            i = min

    def update_key(self, i):
        while i > 1:
            # Parent offset (again - we use bit shift operator)
            parent = (i - 1) >> 1
            if self.vHeap[parent][0] < self.vHeap[i][0]:
                break
            self.vSwap(i, parent)
            i = parent

    def vSwap(self, i, j):
        h = self.vHeap
        h[i], h[j] = h[j], h[i]
        h[i][2] = i
        h[j][2] = j


#Timer for testing
start_time = time.time()
class Vertex:
    def __init__(self, argcoordinates):
        self.coordinates = argcoordinates

class Graph:
    def __init__(self, source, vertices) :
        self.source = source
        self.vertices = vertices

    def prims(self, k, d):
        
        source = Vertex(self.source)
        priority_queue = vertexHeap()
        priority_queue[source] = 0

        MST = set()
        MST_cost = 0

        while priority_queue :
            # "pop" the vertex with the least edge cost in our PQ
            (vMin, cost) = priority_queue.pop()

            # Dim 0 is slightly different than the other higher dims
            if d == 0:
                coordinates = vMin.coordinates[0]
                if coordinates not in MST :
                    MST_cost += cost
                    MST.add(coordinates)
        
                    for vertex in self.vertices :
                        # for every vertex in the set of vertices EXCEPT for vMin.coordinates (itself)
                        if vertex == vMin.coordinates:
                            continue
                        cost = random.random()
                        if cost <= k:

                            # If below pruning cost, and NOT in MST, add to our PQ
                            if (vertex[0] not in MST):
                                priority_queue[Vertex(vertex)] = cost

            # Higher dim
            else:
                if vMin.coordinates not in MST :
                    MST_cost += cost
                    MST.add(vMin.coordinates)

                    for vertex in self.vertices :
                        # for every vertex in the set of vertices EXCEPT for vMin.coordinates (itself)
                        if vertex == vMin.coordinates:
                            continue

                        if d == 2:
                            (x,y,) = vertex
                            (vX,vY) = vMin.coordinates
                            
                            # Generate a k-bounded box around our vMin vertex
                            # Then prefilter weights before even calculating cost -- that is, skip vertices that are outside of our k-cost
                            if (x > (vX + k)) or (x < (vX - k)) or (y > (vY + k)) or (y < (vY - k)):
                                continue


                        if d == 3:
                            (x,y,z) = vertex
                            (vX,vY,vZ) = vMin.coordinates
                            
                            # Generate a k-bounded cube around our vMin vertex
                            # Then prefilter weights before even calculating cost -- that is, skip vertices that are outside of our k-cost
                            if (x > (vX + k)) or (x < (vX - k)) or (y > (vY + k)) or (y < (vY - k)) or (z > (vZ + k)) or (z < (vZ - k)):
                                continue
                        
                        if d == 4:
                            (x,y,z, p4) = vertex
                            (vX,vY,vZ,vP4) = vMin.coordinates
                            
                            # Generate a k-bounded hypercube around our vMin vertex
                            # Then prefilter weights before even calculating cost -- that is, skip vertices that are outside of our k-cost
                            if (x > (vX + k)) or (x < (vX - k)) or (y > (vY + k)) or (y < (vY - k)) or (z > (vZ + k)) or (z < (vZ - k)) or (p4 > (vP4 + k)) or (p4 < (vP4 - k)):
                                continue
                        
                        # Calculate cost and add to PQ (only if it's not in our MST and if our cost is below pruning value)
                        if (vertex not in MST):
                            cost = math.dist(vMin.coordinates, vertex)
                            if cost <= k:
                                priority_queue[Vertex(vertex)] = cost
        return MST_cost



def get_cost(n, dim, k) -> int:
    vertices = []

    if (dim == 0):
        for vertex in range(n):
            vertex = x = [random.random()]
            vertices.append(vertex)
        source = vertices[0]
            
    elif (dim == 2):
        vertices = []
        
        # generate random vertices
        for _ in range(n):
            x = random.random()
            y = random.random()
            vertices.append((x, y))        
        source = vertices[0]
        
    elif (dim == 3): #17.6
        vertices = []
        
        # generate random vertices
        for _ in range(n):
            x = random.random()
            y = random.random()
            z = random.random()
            vertices.append((x, y, z))        
        source = vertices[0]
        
    elif (dim == 4):
        vertices = []

        # generate random vertices
        for _ in range(n):
            x = random.random()
            y = random.random()
            z = random.random()
            p4 = random.random()
            vertices.append((x,y,z,p4))
        source = vertices[0]
    

    g1 = Graph(source, vertices)
    cost = g1.prims(k, dim)
    return cost

def main():

    flag, n, numtrials, dim = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])

    if n == 0:
        print(str(0) + " " + " " + str(n) + " " + str(numtrials) + " " + str(dim))
        exit() 

    k_values = {}


    # Dim 0 k - values
    k_values[(128,0)] = 0.08
    k_values[(256,0)] = 0.04
    k_values[(512,0)] = 0.02
    k_values[(1024,0)] = 0.008
    k_values[(2048,0)] = 0.007
    k_values[(4096,0)] = 0.004
    k_values[(8192,0)] = 0.002
    k_values[(16384,0)] = 0.001
    k_values[(32768,0)] = 0.0008
    k_values[(65536,0)] = 0.0005
    k_values[(131072,0)] = 0.0003
    k_values[(262144,0)] = 0.00008



    # Dim 2 k - values
    k_values[(128,2)] = 0.2
    k_values[(256,2)] = 0.14
    k_values[(512,2)] = 0.12
    k_values[(1024,2)] = 0.1
    k_values[(2048,2)] = 0.08
    k_values[(4096,2)] = 0.06
    k_values[(8192,2)] = 0.04
    k_values[(16384,2)] = 0.0205
    k_values[(32768,2)] = 0.015
    k_values[(65536,2)] = 0.009
    k_values[(131072,2)] = 0.008
    k_values[(262144,2)] = 0.006



    # Dim 3 k-values
    k_values[(128,3)] = 0.36
    k_values[(256,3)] = 0.28
    k_values[(512,3)] = 0.22
    k_values[(1024,3)] = 0.18
    k_values[(2048,3)] = 0.15
    k_values[(4096,3)] = 0.11
    k_values[(8192,3)] = 0.08
    k_values[(16384,3)] = 0.06
    k_values[(32768,3)] = 0.05
    k_values[(65536,3)] = 0.045
    k_values[(131072,3)] = 0.035
    k_values[(262144,3)] = 0.02


    # Dim 4 k-values
    k_values[(128,4)] = 0.46
    k_values[(256,4)] = 0.4
    k_values[(512,4)] = 0.3
    k_values[(1024,4)] = 0.3
    k_values[(2048,4)] = 0.2
    k_values[(4096,4)] = 0.2
    k_values[(8192,4)] = 0.19
    k_values[(16384,4)] = 0.14
    k_values[(32768,4)] = 0.13
    k_values[(65536,4)] = 0.13
    k_values[(131072,4)] = 0.099
    k_values[(262144,4)] = 0.08

    n_values = [128,256,512,1024,2048,4096,8192, 16384,32768, 65536, 131072, 262144]
    if n in n_values:
        k = k_values[(n, dim)]
    else:
        k = 1

    total_min_cost_count = 0
    for trial in range(numtrials):
        
        print("trial :" + str(trial))
        cost_from_one_trial = get_cost(n, dim, k)
        print("cost from one trial", cost_from_one_trial)
        total_min_cost_count +=  cost_from_one_trial
        print("total cost ", total_min_cost_count)
        
    average_cost = total_min_cost_count/numtrials
    print("average cost: ", average_cost)
    print(str(average_cost) + " " + " " + str(n) + " " + str(numtrials) + " " + str(dim))
    print("--- %s total seconds ---" % (time.time() - start_time))
    print("--- %s average seconds per trial ---" % ((time.time() - start_time)/numtrials))

if __name__ == "__main__" :
    main()

    


