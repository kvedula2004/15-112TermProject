#################################################
# # Ellipse class 
#################################################

from tracemalloc import start
from cmu_112_graphics import *
from boardClass import *
from pointClass import *

class Ellipse(object):
    def __init__(self, app, index1, index2, index3, label, isDrawn = True):
        self.app = app
        self.focusIdx1, self.focusIdx2 = index1, index2
        self.borderIdx = index3
        self.label = label
        self.isDrawn = isDrawn

    def computeEquation(self):
        f1_x, f1_y = self.app.allPoints[self.focusIdx1].x, self.app.allPoints[self.focusIdx1].y
        f2_x, f2_y = self.app.allPoints[self.focusIdx2].x, self.app.allPoints[self.focusIdx2].y
        ptX, ptY = self.app.allPoints[self.borderIdx].x, self.app.allPoints[self.borderIdx].y

        d = Point.distance(f1_x, f1_y, ptX, ptY) + Point.distance(f2_x, f2_y, ptX, ptY)
        A = 4*(f2_x-f1_x)**2 - 4*d**2
        B = 8*(f2_x-f1_x)*(f2_y-f1_y)
        C = 4*(f2_y-f1_y)**2 - 4*d**2
        filler = f1_x**2 + f1_y**2 - f2_x**2 - f2_y**2
        D = 4*(f2_x-f1_x)*filler + 4*(f1_x+f2_x)*d**2
        E = 4*(f2_y-f1_y)*filler + 4*(f1_y+f2_y)*d**2
        F = filler**2 + d**4 - 2*(f1_x**2+f1_y**2+f2_x**2+f2_y**2)*d**2
        if A == 0: A = 0.001
        if C == 0: C = 0.001
        return (A,B,C,D,E,F)

    def xInterval(self):
        (A,B,C,D,E,F) = self.computeEquation()
        quadCoeff = B**2-4*A*C
        linearCoeff = 2*B*E-4*C*D
        constCoeff = E**2-4*C*F
        if quadCoeff == 0: quadCoeff = 0.001
        discriminant = math.sqrt(linearCoeff**2 - 4*quadCoeff*constCoeff)
        x1 = (-linearCoeff-discriminant)/(2*quadCoeff)
        x2 = (-linearCoeff+discriminant)/(2*quadCoeff)
        return (min(x1, x2), max(x1, x2))

    def getYVals(self, x):
        (A,B,C,D,E,F) = self.computeEquation()
        quadCoeff = C
        linearCoeff = B*x+E
        constCoeff = A*x*x+D*x+F
        if quadCoeff == 0: quadCoeff = 0.001
        discriminant = math.sqrt(linearCoeff**2 - 4*quadCoeff*constCoeff)
        y1 = (-linearCoeff-discriminant)/(2*quadCoeff)
        y2 = (-linearCoeff+discriminant)/(2*quadCoeff)
        return (min(y1,y2), max(y1,y2))

    def closestPoint(self, app, x, y):
        bestX, bestY = None, None
        closestDist = None
        startX, endX = self.xInterval()[0]+0.001, self.xInterval()[1]-0.001
        step = 0.1
        while(startX < endX):
            y1, y2 = self.getYVals(startX)
            dist1 = Point.distance(x, y, startX, y1)
            if closestDist == None or dist1 < closestDist:
                bestX, bestY = startX, y1
                closestDist = dist1
            dist2 = Point.distance(x, y, startX, y2)
            if closestDist == None or dist2 < closestDist:
                bestX, bestY = startX, y2
                closestDist = dist2
            startX += step
        return (bestX, bestY)

    def distance(self, app, x, y):
        closestPt = self.closestPoint(app, x, y)
        return Point.distance(x, y, closestPt[0], closestPt[1])

    def fastDist(self, app, x, y):
        f1_x, f1_y = self.app.allPoints[self.focusIdx1].x, self.app.allPoints[self.focusIdx1].y
        f2_x, f2_y = self.app.allPoints[self.focusIdx2].x, self.app.allPoints[self.focusIdx2].y
        ptX, ptY = self.app.allPoints[self.borderIdx].x, self.app.allPoints[self.borderIdx].y

        d = Point.distance(f1_x, f1_y, ptX, ptY) + Point.distance(f2_x, f2_y, ptX, ptY)
        dist = Point.distance(f1_x, f1_y, x, y) + Point.distance(f2_x, f2_y, x, y)
        return abs(d-dist)
    
    def drawEllipse(self, canvas):
        if not self.isDrawn: return
        startX, endX = self.xInterval()[0]+0.001, self.xInterval()[1]-0.001
        step = 0.1
        prevLowPixel = None
        prevHiPixel = None
        while(startX < endX):
            y1, y2 = self.getYVals(startX)
            pixel1 = self.app.board.convertPointToPixel(self.app, startX, y1)
            pixel2 = self.app.board.convertPointToPixel(self.app, startX, y2)
            if prevLowPixel == None:
                prevLowPixel, prevHiPixel = pixel1, pixel2
                canvas.create_line(pixel1[0], pixel1[1], pixel2[0], pixel2[1],
                                   fill = 'black', width = 2)
            else:
                canvas.create_line(prevLowPixel[0], prevLowPixel[1], pixel1[0], pixel1[1],
                                   fill = 'black', width = 2)
                canvas.create_line(prevHiPixel[0], prevHiPixel[1], pixel2[0], pixel2[1],
                                   fill = 'black', width = 2)
            prevLowPixel, prevHiPixel = pixel1, pixel2
            startX += step
        canvas.create_line(pixel1[0], pixel1[1], pixel2[0], pixel2[1],
                                   fill = 'black', width = 2)
