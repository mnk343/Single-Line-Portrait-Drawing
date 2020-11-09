import matplotlib.pyplot as plt
import numpy as np
from scipy import interpolate
from heapq import heapify, heappush, heappop
import math
import random
import pickle
stipples_pickle = pickle.load( open("file" , "rb") )
stipples_dict = {}
stipples = []

for stipple in stipples_pickle:
	if stipple not in stipples_dict:
		stipples.append(stipple)
		stipples_dict[stipple]=1

def get_distance(a, b):
    return math.sqrt(((a[0] - b[0]) ** 2) + ((a[1] - b[1]) ** 2))

def get_next_point(current_point, visited):
    # Creating empty heap 
    close_points = [] 
    heapify(close_points)

    count_closest_points = 1

    for i, pt in enumerate(stipples):
        if not visited[i]:
            distance = get_distance(current_point, pt)
            heappush(close_points, (-1 * distance, i))
            if len(close_points) > count_closest_points:
                heappop(close_points)
    
    if len(close_points) == 0:
        return -1
    
    # random.seed(451)
    random_index = random.randint(0, count_closest_points-1)
    next_point = stipples[close_points[random_index][1]]
    visited[close_points[random_index][1]] = True
    return next_point

visited = [False for i in range(len(stipples))]
next_point = stipples[0]
visited[0] = 1
points = []

while next_point != -1:
    points.append([next_point[0] , next_point[1]])
    next_point = get_next_point(next_point, visited)
nodes = np.array(points)

xfinal = []
yfinal = []

for i in range(0 , len(nodes) // 30 ):
	x = nodes[:,0][i*30 :i*30 + 30]
	y = nodes[:,1][i*30 : i*30 + 30]
	tck,u     = interpolate.splprep( [x,y] ,s = 0 )
	xnew,ynew = interpolate.splev( np.linspace( 0, 1, 100 ), tck,der = 0)
	for x in xnew:
		xfinal.append(x)
	for y in ynew:
		yfinal.append(y)

plt.plot(  xfinal ,yfinal )
plt.legend( [ 'spline'] )

plt.axis( [0 , 500 , 0 , 500 ] )
plt.show()
