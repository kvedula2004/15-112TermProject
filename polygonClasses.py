#################################################
# # Polygon and RegularPolygon class 
#################################################

from cmu_112_graphics import *
from boardClass import *
from pointClass import *
from lineClasses import *

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
                ls = LineSegment(app.points, self.indices[i], self.indices[i+1],'')
                ls.drawLineSegment(board, app, canvas)
            else:
                ls = LineSegment(app.points, self.indices[i], self.indices[0],'')
                ls.drawLineSegment(board, app, canvas)
        ptVtxList = tuple(app.points[self.indices[i]] for i in range(len(self.indices)))
        pixelVtxList = tuple(board.convertPointToPixel(app, pt.x, pt.y)
                             for pt in ptVtxList)
        canvas.create_polygon(pixelVtxList, width = 0, fill = 'pink')

    # computes distance between point and polygon
    def distance(self, x, y):
        minDist = None
        for i in range(len(self.indices)):
            if i < len(self.indices) - 1:
                ls = LineSegment(self.points, self.indices[i], self.indices[i+1],
                                 label = '')
            else:
                ls = LineSegment(self.points, self.indices[i], self.indices[0],
                                 label = '')
            if minDist == None or ls.distance(x,y) < minDist:
                minDist = ls.distance(x,y)
        return minDist

    def closestPoint(self, x, y):
        minPoint = None
        minDist = None
        for i in range(len(self.indices)):
            if i < len(self.indices) - 1:
                ls = LineSegment(self.points, self.indices[i], self.indices[i+1],
                                 label = '')
            else:
                ls = LineSegment(self.points, self.indices[i], self.indices[0],
                                 label = '')
            if minDist == None or ls.distance(x, y) < minDist:
                minDist = ls.distance(x, y)
                minPoint = ls.closestPoint(x, y)
        return minPoint