#################################################
# # Point class 
#################################################

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

    

    