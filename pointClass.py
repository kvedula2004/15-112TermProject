#################################################
# # Point class 
#################################################

from cmu_112_graphics import *

# TODO test point class
class Point(object):
    def __init__(self, xCoord, yCoord, canMove, pointName):
        self.x = xCoord
        self.y = yCoord
        self.label = pointName
        self.labelX = xCoord - 10
        self.labelY = yCoord - 10
        self.canMove = canMove
        self.isDrawn = True

    @staticmethod
    def distance(x1, y1, x2, y2):
        return ((x1 - x2)**2 + (y1 - y2)**2)**0.5

    def movePoint(self, newX, newY):
        self.x = newX
        self.y = newY

    def moveLabel(self, newX, newY):
        labelDist = Point.distance(newX, newY, self.x, self.y)

        if labelDist <= 25:
            (self.labelX, self.labelY) = (newX, newY)
        else:
            dx = newX - self.x
            dy = newY - self.y
            dx /= (labelDist / 25)
            dy /= (labelDist / 25)
            self.labelX += dx
            self.labelY += dy

    def toggleHidden(self):
        self.isDrawn = not self.isDrawn

    # ! View method (draw point and label)

    def drawPoint(self, canvas):
        r = 3
        canvas.create_oval(self.x - r, self.y - r, self.x + r, self.y + r,
                           fill = 'light blue', outline = 'black',
                           width = 1)
        canvas.create_text(self.labelX, self.labelY, text = self.label,
                           fill = 'black', font = 'Arial 10 bold')
    

    