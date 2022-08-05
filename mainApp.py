#################################################
# # Main app
#################################################

from cmu_112_graphics import *
from boardClass import *
from pointClass import *


def appStarted(app):
    app.board = Board()
    
    app.isDragging = False
    app.originalClick_X, app.originalClick_Y = 0, 0
    app.timerDelay = 20
    app.lastActions = [0] * 10

    app.points = []
    app.points.append(Point(0,1))
    app.points.append(Point(1,0))
    app.points.append(Point(10,10))
    

# def closeToPoint(app):
#     distances = []
#     for point in app.points:

def mouseDragged(app, event):
    app.lastActions.pop(0)
    app.lastActions.append(1)
    if not app.isDragging:
        app.originalClick_X, app.originalClick_Y = app.board.getPointFromPixel(app, event.x, event.y)
        app.isDragging = True
    else:
        newPoint = app.board.getPointFromPixel(app, event.x, event.y)
        dx = -newPoint[0] + app.originalClick_X
        dy = -newPoint[1] + app.originalClick_Y
        app.board.changeOrigin(app.board.originX + dx, app.board.originY + dy)
        app.isDragging = False

def timerFired(app):
    app.lastActions.pop(0)
    app.lastActions.append(0)
    if app.lastActions == [0] * 10:
        app.isDragging = False

def drawPoints(app, canvas):
    for point in app.points:
        point.drawPoint(app.board, app, canvas)


def redrawAll(app, canvas):
    app.board.drawBoard(app, canvas)
    drawPoints(app, canvas)

def main():
    runApp(width = 2000, height = 800)

if (__name__ == '__main__'):
    main()