from queue import Queue
from random import randint
from PIL import Image, ImageOps
import numpy

input_image = Image.open("image.png")
grayscale_image = ImageOps.grayscale( input_image )
# grayscale_image.show()

np_image = numpy.array(grayscale_image)
print(np_image.shape)

# for i in range(len(np_image)):
# 	for j in range(len(np_image[i])) :
# 		print(np_image[i][j])
# 		np_image[i][j] = 255
# new_im = Image.fromarray(np_image)
# new_im.show()
# generating_points = numpy.random.rand(1000, 2)
# print(generating_points)

generating_points = []
while len(generating_points) < 1000:
    x, y = randint(0, len(np_image) - 1), randint(0, len(np_image[0]) - 1)
    if (x,y) not in generating_points:
    	generating_points.append((x, y))

grid = []
for i in range(0 ,(np_image.shape[0])):
	grid_row = []
	for j in range(0 ,np_image.shape[1] ):
		grid_row.append(1000000)
	grid.append(grid_row)

map_coordinate_to_region = {}

def get_possible_points( grid_point, grid, visited_pixels ):
	x_coords = [1,0,-1,0]
	y_coords = [0,1,0,-1]
	possibe_points = []

	for i in range(len(x_coords)):
		new_point = (grid_point[0] + x_coords[i] , grid_point[1] + y_coords[i])
		if new_point not in visited_pixels:
			if new_point[0] >=0 and new_point[1] >= 0:
				if new_point[0] < len(grid) and new_point[1] < len(grid[0]):
					possibe_points.append(new_point)
	# print(grid_point)
	# print(possibe_points)
	return possibe_points


def run_bfs(generating_points):
	q = Queue()
	for point in generating_points:
		q.put( point )
		grid[point[0]][point[1]] = 0
		map_coordinate_to_region[point] = point
	visited_pixels = {}

	while q.empty() == False :
		grid_point = q.get()
		possible_points = get_possible_points(grid_point, grid, visited_pixels)
		for possible_point in possible_points:
			q.put(possible_point)
			visited_pixels[ possible_point ] = 1

			if( grid[ possible_point[0] ][ possible_point[1] ] > grid[ grid_point[0] ][ grid_point[1] ] + 1 ):
				grid[ possible_point[0] ][ possible_point[1] ] = grid[ grid_point[0] ][ grid_point[1] ] + 1 
				map_coordinate_to_region[possible_point] = map_coordinate_to_region[grid_point]

# for index in range(len(generating_points)):
	# point = generating_points[index]
run_bfs(generating_points)

# print(generating_points)
# print(map_coordinate_to_region)
# print(grid[0][0])
print("done")

for i in range(0 ,(np_image.shape[0])):
	for j in range(0 ,np_image.shape[1] ):
		print( str(i) + " " + str(j) + " " + str(map_coordinate_to_region[(i,j)] ) )	
	print()
	print()