#################################################
# # Line class 
#################################################

from cmu_112_graphics import *
from boardClass import *
from pointClass import *

# TODO test/finish line class
class Line(object):
    def __init__(self, points, index1, index2, label, isDrawn = True):
        point1, point2 = points[index1], points[index2]
        self.point1 = point1
        self.point2 = point2
        self.label = label
        self.isDrawn = isDrawn
        self.label_dx = -0.5
        self.label_dy = 0.5
        self.labelLoc_x = (point1.x + point2.x) / 2
        self.LabelLoc_y = (point1.y + point2.y) / 2
    
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

    def moveLabel(self, newX, newY):
        point = self.closestPoint(newX, newY)
        (self.labelLoc_x, self.LabelLoc_y) = (point.x, point.y)

        dist = self.distance(newX, newY)
        dx = newX - self.labelLoc_x
        dy = newY - self.LabelLoc_y

        if dist >= 3:
            dx /= (dist / 3)
            dy /= (dist / 3)
        (self.label_dx, self.label_dy) = (dx, dy)

    # ! View method (draw line and label)

    # TODO finish
    def drawLine(self, board, app, canvas):
        if not self.isDrawn: return

        lineWidth = 3
        color = 'blue'
        pixel1 = board.convertPointToPixel(app, self.point1.x, self.point1.y)
        pixel2 = board.convertPointToPixel(app, self.point2.x, self.point2.y)
        topY, bottomY = board.convertPointToPixel(app, board.yUpLimit, board.yDownLimit)
        leftX, rightX = board.convertPointToPixel(app, board.xLeftLimit, board.xRightLimit)

        if pixel1[0] == pixel2[0]:
            canvas.create_line(pixel1[0], topY, pixel1[0], bottomY,
                               fill = color, width = lineWidth)
            return
        if pixel1[1] == pixel2[1]:
            canvas.create_line(leftX, pixel1[1], rightX, pixel2[2],
                               fill = color, width = lineWidth)
            return

        lineM = (pixel1[1] - pixel2[1]) / (pixel1[0] - pixel2[0])
        lineB = pixel1[1] - lineM * pixel1[0]
        leftBound = lineM * leftX + lineB
        rightBound = lineM * rightX + lineB