import random
import math
import time
n = 20048

class Vertex:
    def __init__(self, argcoordinates):
        self.coordinates = argcoordinates

vertices3d = []
for _ in range(n):
    x = random.random()
    y = random.random()
    z = random.random()
    vertices3d.append((x, y, z))       


vertices4d = []
for _ in range(n):
    x = random.random()
    y = random.random()
    z = random.random()
    p4 = random.random()
    vertices4d.append((x, y, z, p4))


# start the timer and calculate the weight between each vertex in 3d
start_time = time.time()

for vertex in vertices3d:
    for adj in vertices3d:
        if vertex == adj:
            continue
        weight = math.dist(vertex,adj)
print("--- %s total seconds 3D cost ---" % (time.time() - start_time))

start_time = time.time()

for vertex in vertices4d:
    for adj in vertices4d:
        if vertex == adj:
            continue
        weight = math.dist(vertex,adj)
print("--- %s total seconds 4D cost ---" % (time.time() - start_time))


