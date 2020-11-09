import pickle
from queue import Queue
from random import randint
from PIL import Image, ImageOps, ImageDraw
import numpy

input_image = Image.open("image.png")
grayscale_image = ImageOps.grayscale( input_image )
grayscale_image.save("hello.png")
numpy_image = numpy.array(grayscale_image)
numpy_image = numpy_image.T
np_image = []

for i in range(0 ,(numpy_image.shape[0])):
	np_temp = []
	for j in range(0 ,numpy_image.shape[1] ):
		np_temp.append(numpy_image[i][j])
	np_image.append(np_temp)

generating_points = []
while len(generating_points) < 1000:
    x, y = randint(0, len(np_image) - 1), randint(0, len(np_image[0]) - 1)
    if (x,y) not in generating_points:
    	generating_points.append((x, y))

def run_single_iteration(generating_points):
	grid = []
	for i in range(0 ,(len(np_image))):
		grid_row = []
		for j in range(0 ,len(np_image[0]) ):
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

	run_bfs(generating_points)
	denominator = {}
	numerator_x = {}
	numerator_y = {}

	for i in range(0 ,len(np_image)):
		for j in range(0 ,len(np_image[0]) ):
			possible_point = (i,j)
			if np_image[i][j] == 220:
				np_image[i][j] = 254
			if map_coordinate_to_region[possible_point] not in denominator:
				denominator[ map_coordinate_to_region[possible_point] ] = (1 - np_image[i][j]/255)
			else:
				denominator[ map_coordinate_to_region[possible_point] ] += (1 - np_image[i][j]/255)
			if map_coordinate_to_region[possible_point] not in numerator_x:
				numerator_x[ map_coordinate_to_region[possible_point] ] = (i * (1 - np_image[i][j]/255))
			else:
				numerator_x[ map_coordinate_to_region[possible_point] ] += (i * (1 - np_image[i][j]/255))
			if map_coordinate_to_region[possible_point] not in numerator_y:
				numerator_y[ map_coordinate_to_region[possible_point] ] = (j * (1 - np_image[i][j]/255) )
			else:
				numerator_y[ map_coordinate_to_region[possible_point] ] += (j * (1 - np_image[i][j]/255))
	for index in range(len(generating_points)):
		if denominator[generating_points[index]] == 0:
			generating_points[index] = (0,0)
			continue
		generating_points[index] = ((int)(numerator_x[generating_points[index]]/denominator[generating_points[index]]) , (int)(numerator_y[generating_points[index]]/denominator[generating_points[index]]))
		if(generating_points[index][0] >= len(np_image)):
		  generating_points[index] = (len(np_image) -1, generating_points[index][1])
		if(generating_points[index][1] >= len(np_image[0])):
		  generating_points[index] = ( generating_points[index][0] ,len(np_image[0]) -1 )

	generating_points_dict = {}
	temp = []
	for pt in generating_points:
		if pt not in generating_points_dict and pt[0] != len(np_image) and pt[1] != len(np_image[0]): 
			generating_points_dict[pt] = 1
			temp.append(pt)
		generating_points = temp
	return generating_points


for i in range(0,100):
	generating_points = run_single_iteration(generating_points)
	print(i)
	if i%50==0:	
		im = Image.new('RGB', (len(np_image), len(np_image[0])), (255, 255, 255))
		draw = ImageDraw.Draw(im)
		for j in generating_points:
			im.putpixel((j[0],j[1]),(0,0,0))
		im.save("output_" + str(i) + ".png" )
		
		if i==0:
			pickle.dump(generating_points, open('file_initial', 'wb'))

im = Image.new('RGB', (len(np_image), len(np_image[0])), (255, 255, 255))
draw = ImageDraw.Draw(im)
for j in generating_points:
	im.putpixel((j[0],j[1]),(0,0,0))
im.save("output.png")
pickle.dump(generating_points, open('file_final', 'wb'))
