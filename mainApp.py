#################################################
# # Main app
#################################################

from cmu_112_graphics import *
from boardClass import *
from pointClass import *


def appStarted(app):
    app.board = Board()

# TODO fix
def mouseDragged(app, event):
    originalOriginX = app.board.originX
    originalOriginY = app.board.originY
    newPoint = Board.getPointFromPixel(app.board, app, event.x, event.y)
    dx = (newPoint[0] - app.board.originX) / 10
    dy = (newPoint[1] - app.board.originY) / 10
    app.board.changeOrigin(originalOriginX + dx, originalOriginY + dy)


def redrawAll(app, canvas):
    app.board.drawBoard(app, canvas)

def main():
    runApp(width = 2000, height = 800)

if (__name__ == '__main__'):
    main()