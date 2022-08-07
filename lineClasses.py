#################################################
# # Line class 
#################################################

from cmu_112_graphics import *
from boardClass import *
from pointClass import *

# TODO test/finish line class
class Line(object):
    def __init__(self, point1, point2, label, isDrawn = True):
        self.point1 = point1
        self.point2 = point2
        self.label = label
        self.isDrawn = isDrawn
        self.label_dx = -0.5
        self.label_dy = 0.5
    
    def distance(self, x, y):
        if self.point1.x == self.point2.x:
            return abs(x - self.point.x)
        if self.point1.y == self.point2.y:
            return abs(y - self.point1.y)
        
        x1, y1 = self.point1.x, self.point1.y
        x2, y2 = self.point2.x, self.point2.y
        shoelaceLHS = x*y1 + x1*y2 + x2*y
        shoelaceRHS = y*x1 + y1*x2 + y2*x
        area = 0.5*abs(shoelaceLHS - shoelaceRHS)
        base = Point.distance(x1, y1, x2, y2)
        return 2 * area / base

    def closestPoint(self, x, y):
        if self.point1.x == self.point2.x:
            return Point(self.point1.x, y)
        if self.point1.y == self.point2.y:
            return Point(x, self.point1.y)

        lineM = (self.point2.y-self.point1.y)/(self.point2.x-self.point1.x)
        lineB = self.point1.y - lineM * self.point1.x
        perpLineM = -1 / lineM
        perpLineB = y - perpLineM * x

        newX = (perpLineB - lineB) / (lineM - lineB)
        newY = lineM * newX + lineB
        return Point(newX, newY)

