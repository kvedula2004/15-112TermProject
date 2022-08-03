#################################################
# # Main app
#################################################

from cmu_112_graphics import *
from boardClass import *
from pointClass import *


def appStarted(app):
    app.board = Board()

    app.originalOrigin_X, app.originalOrigin_Y = 0, 0
    app.isDragging = False
    app.originalClick_X, app.originalClick_Y = 0, 0
    app.timerDelay = 50
    

# TODO fix snapping
def mouseDragged(app, event):
    print(f'MousePoint{app.board.getPointFromPixel(app, event.x, event.y)}')
    if not app.isDragging:
        app.originalClick_X, app.originalClick_Y = app.board.getPointFromPixel(app, event.x, event.y)
        app.originalOrigin_X = app.board.originX
        app.originalOrigin_Y = app.board.originY
        app.isDragging = True
    else:
        newPoint = app.board.getPointFromPixel(app, event.x, event.y)
        dx = -newPoint[0] + app.originalClick_X
        dy = -newPoint[1] + app.originalClick_Y
        app.board.changeOrigin(app.originalOrigin_X + dx, app.originalOrigin_Y + dy)
        app.isDragging = False

def timerFired(app):
    if not app.mouseDragged: 
        app.isDragging = False
        app.board.changeOrigin(app.originalOrigin_X, app.originalOrigin_Y)


def redrawAll(app, canvas):
    app.board.drawBoard(app, canvas)

def main():
    runApp(width = 2000, height = 800)

if (__name__ == '__main__'):
    main()