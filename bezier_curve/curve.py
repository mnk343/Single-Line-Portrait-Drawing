from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from copy import copy

w, h = 1000, 1000
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

def drawCurve(control_points):
    glPointSize(1)
    glBegin(GL_POINTS)

    t = 0.0
    while t < 1.0:
        pt = Point(200, 200)
        pt = getPoint(t, control_points)
        drawPoint(pt)
        t += 0.001

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

def drawPicture(points):
    control_points = [Point(0,0) for i in range(4)]

    # draw first curve (join first two points)
    control_points[0] = copy(points[0])
    control_points[3] = copy(points[1])

    control_points[1] = copy(points[0])
    control_points[2] = copy(points[0])

    drawCurve(control_points)

    new_control_points = [Point(0,0) for i in range(4)]
    for i in range(2, len(points)):
        new_control_points[0] = copy(points[i-1])
        new_control_points[3] = copy(points[i])

        new_control_points[1] = get_second_cp(control_points)
        new_control_points[2] = get_third_cp(control_points)

        drawCurve(new_control_points)
        control_points = copy(new_control_points)


def iterate():
    glViewport(0, 0, 1000, 1000)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 1000, 0.0, 1000, 0.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()

def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()
    glColor3f(1.0, 0.0, 3.0)

    points = []
    # for i in range(2):
    points.append(Point(400 + 100,400 + 200))
    points.append(Point(400 + 150,400 + 300))
    points.append(Point(400 + 200,400 + 250))
    points.append(Point(400 + 300,400 + 300))
    points.append(Point(400 ,400 ))

    drawPicture(points)   

    glFlush()

glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(1000, 1000)
glutInitWindowPosition(0, 0)
wind = glutCreateWindow("OpenGL Coding Practice")
glutDisplayFunc(showScreen)
glutIdleFunc(showScreen)
glutMainLoop()