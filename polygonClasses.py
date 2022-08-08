#################################################
# # Polygon and RegularPolygon class 
#################################################

from cmu_112_graphics import *
from boardClass import *
from pointClass import *
from lineClasses import *

class Polygon(object):
    def __init__(self, label, points, isDrawn = True, *args):
        self.label = label
        self.points = points
        self.indices = list(args)
        self.isDrawn = isDrawn

    def drawPolygon(self, board, app, canvas):
        for i in range(len(self.indices)):
            if i < len(self.indices) - 1:
                ls = LineSegment(self.points, self.indices[i], self.indices[i+1],
                                 label = '')
                ls.drawLineSegment(board, app, canvas)
            else:
                ls = LineSegment(self.points, self.indices[i], self.indices[0],
                                 label = '')
                ls.drawLineSegment(board, app, canvas)
        # vtxList = (for i in range())
        # canvas.create_polygon()

        