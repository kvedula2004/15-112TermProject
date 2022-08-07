#################################################
# # Board class 
#################################################

from cmu_112_graphics import *
import statistics

class Board(object):
    def __init__(self):
        self.originX = 0
        self.originY = 0
        self.xRightLimit = 100
        self.yUpLimit = 100
        self.xLeftLimit = -100
        self.yDownLimit = -100
        self.gridLineSpace = 20

    # converts point to app pixel coordinates
    def convertPointToPixel(self, app, pointX, pointY):
        dx = pointX - self.originX
        dy = pointY - self.originY
        newX = app.width / 2 + self.originX + dx * self.gridLineSpace
        newY = app.height / 2 + self.originY - dy * self.gridLineSpace
        return (newX, newY)
    
    # converts app pixel coordinates to coordinate grid point
    def getPointFromPixel(self, app, pixelX, pixelY):
        dx = (pixelX - app.width / 2 - self.originX) / self.gridLineSpace
        dy = - (pixelY - app.height / 2 - self.originY) / self.gridLineSpace
        return (dx + self.originX, dy + self.originY)

    # moves the origin
    def changeOrigin(self, newOriginX, newOriginY):
        self.originX = newOriginX
        self.originY = newOriginY

    # ! View methods: draws x-line, y-line, and all of board
    # makes sure all x-line and y-line on the visible board

    def drawLine_X(self, app, canvas, xCoord):
        topPointX, topPointY = Board.convertPointToPixel(self, app, xCoord, self.yUpLimit)
        bottomPointY = Board.convertPointToPixel(self, app, xCoord, self.yDownLimit)[1]
        newLineX = statistics.median([topPointX, 0, app.width])
        newLineY_top = statistics.median([topPointY, 0, app.height])
        newLineY_bottom = statistics.median([bottomPointY, 0, app.height])

        lineWidth = 1
        if xCoord == 0: lineWidth = 3

        canvas.create_line(newLineX, newLineY_top, newLineX, newLineY_bottom, 
                           width = lineWidth, fill = 'black')

    def drawLine_Y(self, app, canvas, yCoord):
        leftPointX, leftPointY = Board.convertPointToPixel(self, app, self.xLeftLimit, yCoord)
        rightPointX = Board.convertPointToPixel(self, app, self.xRightLimit, yCoord)[0]
        newLineY = statistics.median([leftPointY, 0, app.height])
        newLineX_left = statistics.median([leftPointX, 0, app.width])
        newLineX_right = statistics.median([rightPointX, 0, app.width])

        lineWidth = 1
        if yCoord == 0: lineWidth = 3

        canvas.create_line(newLineX_left, newLineY, newLineX_right, newLineY, 
                           width = lineWidth, fill = 'black')

    def drawBoard(self, app, canvas):
        for xLine in range(self.xLeftLimit, self.xRightLimit+1):
            Board.drawLine_X(self, app, canvas, xLine)
        for yLine in range(self.yDownLimit, self.yUpLimit+1):
            Board.drawLine_Y(self, app, canvas, yLine)
