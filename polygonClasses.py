#################################################
# # Polygon and RegularPolygon class 
#################################################

from cmu_112_graphics import *
from boardClass import *
from pointClass import *
from lineClasses import *
import math

class Polygon(object):
    def __init__(self, label, indices, isDrawn = True):
        self.label = label
        self.indices = list(indices)
        self.isDrawn = isDrawn

    # draws all line segments and fills in poylgon
    def drawPolygon(self, board, app, canvas):
        if not self.isDrawn: return
        for i in range(len(self.indices)):
            if i < len(self.indices) - 1:
                ls = LineSegment(app, self.indices[i], self.indices[i+1],'')
                ls.drawLineSegment(board, app, canvas)
            else:
                ls = LineSegment(app, self.indices[i], self.indices[0],'')
                ls.drawLineSegment(board, app, canvas)
        ptVtxList = tuple(app.allPoints[self.indices[i]] for i in range(len(self.indices)))
        pixelVtxList = tuple(board.convertPointToPixel(app, pt.x, pt.y)
                             for pt in ptVtxList)
        canvas.create_polygon(pixelVtxList, width = 0, fill = 'pink')

    # computes distance between point and polygon
    def distance(self, app, x, y):
        minDist = None
        for i in range(len(self.indices)):
            if i < len(self.indices) - 1:
                ls = LineSegment(app, self.indices[i], self.indices[i+1],
                                 label = '')
            else:
                ls = LineSegment(app, self.indices[i], self.indices[0],
                                 label = '')
            if minDist == None or ls.distance(app, x,y) < minDist:
                minDist = ls.distance(app, x,y)
        return minDist

    def closestPoint(self, app, x, y):
        minPoint = None
        minDist = None
        for i in range(len(self.indices)):
            if i < len(self.indices) - 1:
                ls = LineSegment(app, self.indices[i], self.indices[i+1],
                                 label = '')
            else:
                ls = LineSegment(app, self.indices[i], self.indices[0],
                                 label = '')
            if minDist == None or ls.distance(app, x, y) < minDist:
                minDist = ls.distance(app, x, y)
                minPoint = ls.closestPoint(app, x, y)
        return minPoint

    def movePolygon(self, app, dx, dy):
        for index in self.indices:
            app.allPoints[index].x += dx
            app.allPoints[index].y += dy

    def computeArea(self, app):
        xList = [app.allPoints[index].x for index in self.indices]
        xList.append(app.allPoints[self.indices[0]].x)
        yList = [app.allPoints[index].y for index in self.indices]
        yList.append(app.allPoints[self.indices[0]].y)

        LHS, RHS = 0, 0
        for i in range(len(xList)-1):
            LHS += yList[i] * xList[i+1]
            RHS += xList[i] * yList[i+1]
        return 0.5 * abs(LHS - RHS)

# TODO finish
class RegularPolygon(object):
    def __init__(self, app, index1, index2, numSides, label, isDrawn = True):
        self.app = app
        self.index1, self.index2 = index1, index2
        self.numSides = numSides
        self.label = label
        self.isDrawn = isDrawn

    def getVertices(self):
        polyVertices = [(self.app.allPoints[self.index1].x, self.app.allPoints[self.index1].y)]
        polyVertices += [[(self.app.allPoints[self.index2].x, self.app.allPoints[self.index2].y)]]
        theta = math.pi - 2*math.pi/(self.numSides)
        while len(polyVertices) < self.numSides:
            polyVertices.append(self.rotate(polyVertices[-1], polyVertices[-2], theta))
        return polyVertices

    #def rotate(self, center, radius, theta):

