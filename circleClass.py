#################################################
# # Circle class 
#################################################

from cmu_112_graphics import *
from boardClass import *
from pointClass import *
from lineClasses import *

class Circle(object):
    def __init__(self, label, index1, index2, index3=None, isDrawn=True):
        self.label = label
        self.index1, self.index2, self.index3 = index1, index2, index3
        self.isDrawn = isDrawn

    def computeCenter(self, points):
        if self.index3 == None:
            return (points[self.index1].x, points[self.index1].y)
        point1, point2, point3 = points[self.index1], points[self.index2], points[self.index3]
        x1, y1 = point1.x, point1.y
        x2, y2 = point2.x, point2.y
        x3, y3 = point3.x, point3.y
        
        try:
            line12_m = (x1-x2)/(y2-y1)
        except:
            line12_m = (x1-x2)/(y2-y1+0.001)
        try:
            line13_m = (x1-x3)/(y3-y1)
        except:
            line13_m = (x1-x3)/(y3-y1+0.001)
        
        line12_b = (y1+y2)*0.5 - line12_m * (x1+x2)*0.5
        line13_b = (y1+y3)*0.5 - line13_m * (x1+x3)*0.5
        try:
            centerX = (line13_b-line12_b)/(line12_m-line13_m)
        except:
            centerX = (line13_b-line12_b)/(line12_m-line13_m+0.001)
        centerY = centerX * line12_m + line12_b
        return (centerX, centerY)

    def computeR(self, points):
        if self.index3 == None:
            x1, y1 = points[self.index1].x, points[self.index1].y
            x2, y2 = points[self.index2].x, points[self.index2].y
            return Point.distance(x1, y1, x2, y2)
        
        centerX, centerY = self.computeCenter(points)
        x1, y1 = points[self.index1].x, points[self.index1].y
        return Point.distance(x1, y1, centerX, centerY)

    def distance(self, app, x, y):
        centerX, centerY = self.computeCenter(app.allPoints)
        r = self.computeR(app.allPoints)
        dist = Point.distance(centerX, centerY, x, y)
        return abs(dist - r)

    def closestPoint(self, app, x, y):
        centerX, centerY = self.computeCenter(app.allPoints)
        r = self.computeR(app.allPoints)
        dx, dy = x - centerX, y - centerY
        dist = Point.distance(dx, dy, 0, 0)
        dx /= (dist/(r+0.0001))
        dy /= (dist/(r+0.0001))
        return (centerX + dx, centerY + dy)

    def drawCircle(self, board, app, canvas):
        if not self.isDrawn: return

        centerX, centerY = self.computeCenter(app.allPoints)
        r = self.computeR(app.allPoints)
        pixelR = r * board.gridLineSpace
        pixelX, pixelY = board.convertPointToPixel(app, centerX, centerY)
        canvas.create_oval(pixelX-pixelR,pixelY-pixelR, pixelX+pixelR, pixelY+pixelR,
                           fill = '', width = 1.5, outline = 'gray')