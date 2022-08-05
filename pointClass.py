#################################################
# # Point class 
#################################################

from cmu_112_graphics import *
from boardClass import *

# TODO fix default naming system
class Point(object):
    defaultNames = []
    for row in range(10):
        for i in range(26):
            defaultNames.append(chr(ord('A')+i) + "'"*row)
    currIndex = 0

    def __init__(self, xCoord, yCoord, pointName = defaultNames[currIndex], 
                 currObject = None, canMove = True):
        self.x = xCoord
        self.y = yCoord
        self.label = pointName
        if self.label == Point.defaultNames[Point.currIndex]: 
            Point.currIndex += 1
            Point.currIndex %= 26*26
        self.label_dx = -0.5
        self.label_dy = 0.5
        self.canMove = canMove
        self.isDrawn = True
        self.onObject = currObject

    @staticmethod
    def distance(x1, y1, x2, y2):
        return ((x1 - x2)**2 + (y1 - y2)**2)**0.5

    def movePoint(self, newX, newY):
        self.x = newX
        self.y = newY

    def moveLabel(self, newX, newY):
        labelDist = Point.distance(newX, newY, self.x, self.y)

        if labelDist <= 25:
            (self.label_dx, self.label_dy) = (newX-self.x, newY-self.y)
        else:
            dx = newX - self.x
            dy = newY - self.y
            dx /= (labelDist / 25)
            dy /= (labelDist / 25)
            self.label_dx = dx
            self.label_dy = dy

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
                           fill = 'black', font = 'Arial 10 bold')
    

    