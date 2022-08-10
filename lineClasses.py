#################################################
# # Line and LineSegment class 
#################################################

from cmu_112_graphics import *
from boardClass import *
from pointClass import *

class Line(object):
    def __init__(self, points, index1, index2, label, isDrawn = True):
        self.points = points
        self.index1, self.index2 = index1, index2
        point1 = points[index1]
        point2 = points[index2]
        self.label = label
        self.isDrawn = isDrawn
        self.label_dx = -0.5
        self.label_dy = 0.5
        self.labelLoc_x = (point1.x + point2.x) / 2
        self.labelLoc_y = (point1.y + point2.y) / 2
    
    # computes distance between point and line
    def distance(self, app, x, y):
        point1, point2 = self.points[self.index1], self.points[self.index2]
        if point1.x == point2.x:
            return abs(x - point1.x)
        if point1.y == point2.y:
            return abs(y - point1.y)
        
        x1, y1 = point1.x, point1.y
        x2, y2 = point2.x, point2.y
        shoelaceLHS = x*y1 + x1*y2 + x2*y
        shoelaceRHS = y*x1 + y1*x2 + y2*x
        area = 0.5*abs(shoelaceLHS - shoelaceRHS)
        base = Point.distance(x1, y1, x2, y2)
        return 2 * area / base

    # computes the coordinates of closest point on line wrt to a given point
    def closestPoint(self, app, x, y):
        point1, point2 = self.points[self.index1], self.points[self.index2]
        if point1.x == point2.x:
            return (point1.x, y)
        if point1.y == point2.y:
            return (x, point1.y)

        lineM = (point2.y-point1.y)/(point2.x-point1.x)
        lineB = point1.y - lineM * point1.x
        perpLineM = -1 / lineM
        perpLineB = y - perpLineM * x

        newX = (perpLineB - lineB) / (lineM - perpLineM)
        newY = lineM * newX + lineB
        return (newX, newY)

    # ! View method (draw line)

    def drawLine(self, board, app, canvas):
        point1, point2 = self.points[self.index1], self.points[self.index2]
        if not self.isDrawn: return

        lineWidth = 2.5
        color = 'blue'
        pixel1 = board.convertPointToPixel(app, point1.x, point1.y)
        pixel2 = board.convertPointToPixel(app, point2.x, point2.y)
        rightX, bottomY = board.convertPointToPixel(app, board.xRightLimit, board.yDownLimit)
        leftX, topY = board.convertPointToPixel(app, board.xLeftLimit, board.yUpLimit)

        if pixel1[0] == pixel2[0]:
            canvas.create_line(pixel1[0], topY, pixel1[0], bottomY,
                               fill = color, width = lineWidth)
            return
        if pixel1[1] == pixel2[1]:
            canvas.create_line(leftX, pixel1[1], rightX, pixel2[1],
                               fill = color, width = lineWidth)
            return

        lineM = (point2.y - point1.y)/(point2.x - point1.x)
        lineB = point2.y - lineM * point2.x
        leftBoundY = lineM * board.xLeftLimit + lineB
        rightBoundY = lineM * board.xRightLimit + lineB
        upBoundX = (board.yUpLimit - lineB) / lineM
        downBoundX = (board.yDownLimit - lineB) / lineM

        upBoundPixelX, leftBoundPixelY = board.convertPointToPixel(app, upBoundX, leftBoundY)
        downBoundPixelX, rightBoundPixelY = board.convertPointToPixel(app, downBoundX, rightBoundY)

        leftBound, rightBound = (leftX, leftBoundPixelY), (rightX, rightBoundPixelY)
        upBound, downBound = (upBoundPixelX, topY), (downBoundPixelX, bottomY)

        # casework on where line intersects board boundaries
        if(topY <= leftBound[1] <= bottomY):
            if(topY <= rightBound[1] <= bottomY):
                canvas.create_line(leftBound, rightBound, fill = color, width = lineWidth)
            elif(rightBound[1] < topY):
                canvas.create_line(leftBound, upBound, fill = color, width = lineWidth)
            else:
                canvas.create_line(leftBound, downBound, fill = color, width = lineWidth)
        elif(leftBound[1] < topY):
            if(rightBound[1] < topY):
                return
            elif(rightBound[1] > bottomY):
                canvas.create_line(downBound, upBound, fill = color, width = lineWidth)
            else:
                canvas.create_line(upBound, rightBound, fill = color, width = lineWidth)
        else:
            if(rightBound[1] > bottomY): 
                return
            elif(rightBound[1] < topY):
                canvas.create_line(upBound, downBound, fill = color, width = lineWidth)
            else:
                canvas.create_line(downBound, rightBound, fill = color, width = lineWidth)


class LineSegment(Line):
    def __init__(self, points, index1, index2, label, isDrawn = True):
        super().__init__(points, index1, index2, label, isDrawn)

    # computes distance between linesegment and point
    def distance(self, app, x, y):
        point1, point2 = self.points[self.index1], self.points[self.index2]
        dist1 = super().distance(app, x, y)
        dist2 = Point.distance(point1.x, point1.y, x, y)
        dist3 = Point.distance(point2.x, point2.y, x, y)
        return min(dist1, dist2, dist3)

    # computes the coordinates of the closest point
    def closestPoint(self, app, x, y):
        pt1 = super().closestPoint(app, x, y)
        point1, point2 = self.points[self.index1], self.points[self.index2]
        
        distA = Point.distance(pt1[0],pt1[1], point1.x, point1.y)
        distB = Point.distance(pt1[0],pt1[1], point2.x, point2.y)
        distC = Point.distance(point2.x,point2.y, point1.x, point1.y)
        if abs(distA + distB - distC) < 10**-4:
            return pt1
        
        dist1 = Point.distance(x, y, point1.x, point1.y)
        dist2 = Point.distance(x, y, point2.x, point2.y)

        if dist1 <= dist2: return (point1.x, point1.y)
        else: return (point2.x, point2.y)

    # draws the line segment
    def drawLineSegment(self, board, app, canvas):
        point1, point2 = self.points[self.index1], self.points[self.index2]

        pixel1 = board.convertPointToPixel(app, point1.x, point1.y)
        pixel2 = board.convertPointToPixel(app, point2.x, point2.y)

        canvas.create_line(pixel1, pixel2, fill = 'blue', width = 2.5)
        