#################################################
# # Point class 
#################################################

from cmu_112_graphics import *
from boardClass import *

class Point(object):
    def __init__(self, app, xCoord, yCoord, pointName = '', 
                 currObject = None, canMove = True):
        self.x = xCoord
        self.y = yCoord

        # if no argument provided, default name used
        if pointName == '':
            self.label = app.defaultNames[app.currIndex]
            app.currIndex += 1
        else: self.label = pointName
        
        self.label_dx = -0.5
        self.label_dy = 0.5
        self.canMove = canMove
        self.isDrawn = True
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
            newPt = self.currObject.closestPoint(newX, newY)
            self.x, self.y = newPt.x, newPt.y

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
    

    