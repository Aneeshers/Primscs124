from typing import List, Dict # For annotations
import random
import math
import sys
import time
import threading
from collections.abc import MutableMapping


class heapdict(MutableMapping):
    __marker = object()

    def __init__(self, *args, **kw):
        self.heap = []
        self.d = {}
        self.update(*args, **kw)

    def clear(self):
        del self.heap[:]
        self.d.clear()

    def __setitem__(self, key, value):
        if key in self.d:
            self.pop(key)
        wrapper = [value, key, len(self)]
        self.d[key] = wrapper
        self.heap.append(wrapper)
        self._decrease_key(len(self.heap)-1)

    def _min_heapify(self, i):
        n = len(self.heap)
        h = self.heap
        while True:
            # calculate the offset of the left child
            l = (i << 1) + 1
            # calculate the offset of the right child
            r = (i + 1) << 1
            if l < n and h[l][0] < h[i][0]:
                low = l
            else:
                low = i
            if r < n and h[r][0] < h[low][0]:
                low = r

            if low == i:
                break

            self._swap(i, low)
            i = low

    def _decrease_key(self, i):
        while i:
            # calculate the offset of the parent
            parent = (i - 1) >> 1
            if self.heap[parent][0] < self.heap[i][0]:
                break
            self._swap(i, parent)
            i = parent

    def _swap(self, i, j):
        h = self.heap
        h[i], h[j] = h[j], h[i]
        h[i][2] = i
        h[j][2] = j

    def __delitem__(self, key):
        wrapper = self.d[key]
        while wrapper[2]:
            # calculate the offset of the parent
            parentpos = (wrapper[2] - 1) >> 1
            parent = self.heap[parentpos]
            self._swap(wrapper[2], parent[2])
        self.popitem()

    def __getitem__(self, key):
        return self.d[key][0]

    def __iter__(self):
        return iter(self.d)

    def popitem(self):
        """D.popitem() -> (k, v), remove and return the (key, value) pair with lowest\nvalue; but raise KeyError if D is empty."""
        wrapper = self.heap[0]
        if len(self.heap) == 1:
            self.heap.pop()
        else:
            self.heap[0] = self.heap.pop()
            self.heap[0][2] = 0
            self._min_heapify(0)
        del self.d[wrapper[1]]
        return wrapper[1], wrapper[0]

    def __len__(self):
        return len(self.d)

    def peekitem(self):
        """D.peekitem() -> (k, v), return the (key, value) pair with lowest value;\n but raise KeyError if D is empty."""
        return (self.heap[0][1], self.heap[0][0])



#Timer for testing
start_time = time.time()

class Node:
    def __init__(self, arg_id):
        self._id = arg_id

class Graph:
    def __init__(self, source : int, adj_list : Dict[int, List[int]]) :
        self.source = source
        self.vertices = adj_list


    def PrimsMST (self) -> int :
        
        source = Node(self.source)

        priority_queue = heapdict()
        priority_queue[source] = 0
        added = {}
        
        for vertex in self.vertices:
            added[vertex] = False
        MST_cost = 0

        while priority_queue :
            # Choose and "pop" the adjacent node with the least edge cost
            (node, cost) = priority_queue.popitem()

            if added[node._id] == False :
                MST_cost += cost
                added[node._id] = True

                for vertex in self.vertices :
                    # for every vertex in the set of vertices EXCEPT for node._id (itself)
                    if vertex == node._id:
                        continue
                    # Only look at vertices that are not in our MST
                    if added[vertex] == False :

                        # Calculate cost and add to PQ
                        cost = math.dist(node._id, vertex)
                        priority_queue[Node(vertex)] = cost
        return MST_cost




def get_cost(n, dim) -> int:
    vertices = []

    if (dim == 1):
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
    cost = g1.PrimsMST()
    return cost

def main(): #need to implement number of trials still

    n, numtrials, dim = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    
    total_min_cost_count = 0
    for trial in range(numtrials):
        
        print("trial :" + str(trial))
        cost_from_one_trial = get_cost(n, dim)
        print("cost from one trial", cost_from_one_trial)
        total_min_cost_count +=  cost_from_one_trial
        print("total cost ", total_min_cost_count)
        #start thread for every getcost()
        
    average_cost = total_min_cost_count/numtrials
    print("average cost is ", average_cost)

if __name__ == "__main__" :
    main()
    print("--- %s seconds ---" % (time.time() - start_time))


