#################################################
# # Point and Intersection class 
#################################################

from cmu_112_graphics import *
from boardClass import *
import math

class Point(object):
    def __init__(self, app, xCoord, yCoord, pointName = '', 
                 currObject = None, canMove = True, isDrawn = True):
        self.app = app
        if currObject == None:
            self.x = xCoord
            self.y = yCoord
        else:
            self.x, self.y = currObject.closestPoint(app, xCoord, yCoord)

        # if no argument provided, default name used
        if pointName == '':
            while app.defaultNames[app.currIndex] in app.pointNames:
                app.currIndex += 1
            self.label = app.defaultNames[app.currIndex]
            app.currIndex += 1
        else: self.label = pointName
        
        self.label_dx = -0.5
        self.label_dy = 0.5
        self.canMove = canMove
        self.isDrawn = isDrawn
        self.currObject = currObject

    # computes distance between (x1, y1) and (x2, y2)
    @staticmethod
    def distance(x1, y1, x2, y2):
        return ((x1 - x2)**2 + (y1 - y2)**2)**0.5

    # moves the label: if click too far, normalizes label vector to magnitude 3
    def moveLabel(self, newX, newY):
        labelDist = Point.distance(newX, newY, self.x, self.y)

        if labelDist <= 3:
            (self.label_dx, self.label_dy) = (newX-self.x, newY-self.y)
        else:
            dx = newX - self.x
            dy = newY - self.y
            dx /= (labelDist / 3)
            dy /= (labelDist / 3)
            self.label_dx = dx
            self.label_dy = dy

    def movePoint(self, newX, newY):
        if not self.canMove: return
        
        if self.currObject == None:
            self.x, self.y = newX, newY
        else:
            self.x, self.y = self.currObject.closestPoint(self.app, newX, newY)

    # changes whether point is visible is hidden
    def toggleHidden(self):
        self.isDrawn = not self.isDrawn

    # ! View method (draw point and label)

    def drawPoint(self, board, app, canvas):
        if not self.isDrawn: return

        r = 5
        pixelX, pixelY = board.convertPointToPixel(app, self.x, self.y)
        labelPixelX, labelPixelY = board.convertPointToPixel(app, self.x+self.label_dx, 
                                                             self.y+self.label_dy)
        canvas.create_oval(pixelX - r, pixelY - r, pixelX + r, pixelY + r,
                           fill = 'dark blue', outline = 'black',
                           width = 1)
        canvas.create_text(labelPixelX, labelPixelY, text = self.label,
                           fill = 'green', font = 'Arial 15 bold')
    
class Intersection(object):
    def __init__(self, app, index1, index2, index3, index4):
        self.app = app
        self.obj1Type = app.objects[index1]
        self.obj2Type = app.objects[index3]
        self.obj1 = app.objects[index1][index2]
        self.obj2 = app.objects[index3][index4]
        self.allIntersections = []
        self.labels = []

    def computeBestDir(self, obj1, obj2, r, currX, currY):
        thetas = set(i * math.pi / 15 for i in range(30))
        minDist, bestdx, bestdy = None, None, None
        for theta in thetas:
            dx, dy = r*math.cos(theta), r*math.sin(theta)
            candidateX, candidateY = currX + dx, currY + dy
            try:
                candidateDist = obj1.fastDist(self.app, candidateX, candidateY)
            except:
                candidateDist = obj1.distance(self.app, candidateX, candidateY)
            try:
                candidateDist += obj2.fastDist(self.app, candidateX, candidateY)
            except:
                candidateDist += obj2.distance(self.app, candidateX, candidateY)
            if minDist == None or candidateDist < minDist:
                minDist = candidateDist
                bestdx, bestdy = dx, dy
        return (bestdx, bestdy)
            

    def computeIntersectStart(self, obj1, obj2, numIter, startX, startY):
        r1, r2, r3 = 5, 0.5, 0.01
        currX, currY = startX, startY
        for i in range(numIter):
            dx, dy = self.computeBestDir(obj1, obj2, r1, currX, currY)
            currX += dx
            currY += dy
        for i in range(numIter):
            dx, dy = self.computeBestDir(obj1, obj2, r2, currX, currY)
            currX += dx
            currY += dy
        for i in range(numIter):
            dx, dy = self.computeBestDir(obj1, obj2, r3, currX, currY)
            currX += dx
            currY += dy
        return (currX, currY)

    def computeAllIntersections(self, obj1, obj2, numIter):
        allIntersections = []
        for xVal in [0, 100, -100]:
            for yVal in [0, 100, -100]:
                if xVal == 0 and yVal == 0:
                    continue
                newInter = self.computeIntersectStart(obj1, obj2, numIter, xVal, yVal)
                isNewInter = True
                for elem in allIntersections:
                    if Point.distance(newInter[0], newInter[1], elem[0], elem[1]) < 1:
                        isNewInter = False
                if isNewInter:
                    allIntersections.append(newInter)
        return allIntersections

    def updateIntersection(self):
        for label in self.labels:
            self.app.pointNames.remove(label)
        self.allIntersections = self.computeAllIntersections(self.obj1, self.obj2, 40)
        labels = [-1 for i in self.allIntersections]
        startIndex = 0
        for i in range(len(labels)):
            while self.app.defaultNames[startIndex] in self.app.pointNames:
                startIndex += 1
            labels[i] = self.app.defaultNames[startIndex]
            startIndex += 1
        self.labels = labels
        for label in self.labels:
            self.app.pointNames.add(label)

        

    