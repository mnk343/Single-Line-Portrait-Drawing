import pickle, random, math, sys
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from copy import copy
from heapq import heapify, heappush, heappop
from PIL import Image
from PIL import ImageOps

class Point:    
    def __init__(self, x, y):  
        self.x = x  
        self.y = y

def drawPoint(pt):
    glVertex2f(pt.x, pt.y)
    

def getPoint(t, control_points):
    pt = Point(0, 0)
    pt.x = (((1 - t) ** 3) * control_points[0].x) + (3 * ((1 - t) ** 2) * t * control_points[1].x) + (3 * (1 - t) * (t ** 2) * control_points[2].x) + ((t ** 3) * control_points[3].x)
    pt.y = (((1 - t) ** 3) * control_points[0].y) + (3 * ((1 - t) ** 2) * t * control_points[1].y) + (3 * (1 - t) * (t ** 2) * control_points[2].y) + ((t ** 3) * control_points[3].y)
    return pt

def drawLine(point_A, point_B):
    glPointSize(1)
    glBegin(GL_POINTS)

    t = 0.0
    pt = Point(0, 0)
    while t < 1.0:
        pt.x = (1 - t) * point_A.x + t * point_B.x
        pt.y = (1 - t) * point_A.y + t * point_B.y
        drawPoint(pt)
        t += 0.001

    glEnd()

def drawBezierCurve(control_points):
    glPointSize(2)
    glBegin(GL_POINTS)

    t = 0.0
    pt = Point(0, 0)
    while t < 1.0:
        pt = getPoint(t, control_points)
        drawPoint(pt)
        t += 0.01

    glEnd()

def get_second_cp(control_points):
    pt = Point(0, 0)
    pt.x = (2 * control_points[3].x) - control_points[2].x
    pt.y = (2 * control_points[3].y) - control_points[2].y
    return pt

def get_third_cp(control_points):
    pt = Point(0, 0)
    pt.x = control_points[1].x + 4 * (control_points[3].x - control_points[2].x)
    pt.y = control_points[1].y + 4 * (control_points[3].y - control_points[2].y)
    return pt


def drawPictureUsingBezier():
    control_points = [Point(0,0) for i in range(4)]
    
    # draw first curve (join first two points)
    control_points[0] = copy(path[0])
    control_points[3] = copy(path[1])

    control_points[1] = copy(path[0])
    control_points[2] = copy(path[0])

    drawBezierCurve(control_points)

    new_control_points = [Point(0,0) for i in range(4)]
    for i in range(2, len(path[:10])):
        new_control_points[0] = copy(path[i-1])
        new_control_points[3] = copy(path[i])

        new_control_points[1] = get_second_cp(control_points)
        new_control_points[2] = get_third_cp(control_points)

        drawBezierCurve(new_control_points)
        control_points = copy(new_control_points)


def drawPictureUsingLines():
    for i in range(len(path) - 1):
        drawLine(path[i], path[i+1])


def drawPictureUsingMultipleBezier():
    path_index = 0
    while path_index + 4 <= len(path):
        drawBezierCurve(path[path_index : path_index + 4])
        path_index += 3


def get_distance(a, b):
    return math.sqrt(((a.x - b.x) ** 2) + ((a.y - b.y) ** 2))


def get_next_point(current_point, visited):
    # Creating empty heap 
    close_points = [] 
    heapify(close_points)

    count_closest_points = 1

    for i, pt in enumerate(points):
        if not visited[i]:
            distance = get_distance(current_point, pt)
            heappush(close_points, (-1 * distance, i))
            if len(close_points) > count_closest_points:
                heappop(close_points)
    
    # for elem in close_points:
    #     visited[elem[1]] = True
    
    if len(close_points) == 0:
        return -1
    
    random.seed(451)
    random_index = random.randint(0, count_closest_points - 1)
    next_point = copy(points[close_points[random_index][1]])
    visited[close_points[random_index][1]] = True
    return next_point


def getSingleLinePath():
    path = []
    n = len(points)
    visited = [False for i in range(n)]

    random.seed(9001)
    random_index = random.randint(0, n-1)
    start = copy(points[random_index])
    current_point = start
    visited[random_index] = True
    path.append(copy(current_point))

    next_point = get_next_point(current_point, visited)

    while next_point != -1:
        # drawLine(current_point, next_point) 
        current_point = copy(next_point)
        path.append(copy(current_point))
        next_point = get_next_point(current_point, visited)

    return path
    
def init():
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, width, 0.0, height, 0.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()


def render():
    glLoadIdentity()
    init()
    glClearColor(1, 1, 1, 1)
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(0, 0, 0)
    drawPictureUsingBezier() 
    # drawPictureUsingLines()
    # drawPictureUsingMultipleBezier()
    glFlush()



# main function
glutInit()
glutInitDisplayMode(GLUT_RGBA)
width, height = 1000, 1000
glutInitWindowSize(width, height)
glutInitWindowPosition(0, 0)
wind = glutCreateWindow("Single Line Drawing")

stipple_file = sys.argv[1]

pickle_in = open(stipple_file, "rb")
stipples_coords = pickle.load(pickle_in)
points = []
stipples_coords.sort()
for stipples_coord in stipples_coords:
    if stipples_coord[0] == 0 or stipples_coord[1] == 0:
        continue
    points.append(Point( stipples_coord[0] , stipples_coord[1] ))

path = getSingleLinePath()

# glutDisplayFunc(showScreen)
# glutIdleFunc(showScreen)
# glutMainLoop()

render()

# save the image to file
glPixelStorei(GL_PACK_ALIGNMENT, 1)
data = glReadPixels(0, 0, width, height, GL_RGBA, GL_UNSIGNED_BYTE)
image = Image.frombytes("RGBA", (width, height), data)
image.save(stipple_file + '2.png', 'PNG')
