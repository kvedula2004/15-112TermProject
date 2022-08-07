#################################################
# # Main app
#################################################

from cmu_112_graphics import *
from boardClass import *
from pointClass import *


def appStarted(app):
    app.board = Board()
    
    app.isBoardDragging = False
    app.originalClick_X, app.originalClick_Y = 0, 0
    app.timerDelay = 20
    app.lastActions = [0] * 10

    app.defaultNames = []
    for row in range(10):
        for i in range(26):
            app.defaultNames.append(chr(ord('A')+i) + "'"*row)
    app.currIndex = 0

    app.points = []
    app.points.append(Point(app, 0,1))
    app.points.append(Point(app, 1,0))
    app.points.append(Point(app, 10,10))
    
# computes the closest object among points, point labels, line labels
def closestObject(app, event):
    minDist = None
    minIndex = -1
    isLabelMin = False
    for index in range(len(app.points)):
        point = app.points[index]
        labelX = point.x + point.label_dx
        labelY = point.y + point.label_dy
        (newEventX, newEventY) = app.board.getPointFromPixel(app, event.x, event.y)
        labelDist = Point.distance(labelX, labelY, newEventX, newEventY)
        pointDist = Point.distance(point.x, point.y, newEventX, newEventY)
        if min(labelDist, pointDist) > 2: continue
        if minDist == None or pointDist < minDist:
            (minDist, minIndex) = (pointDist, index)
            isLabelMin = False
        if minDist == None or labelDist < minDist:
            (minDist, minIndex) = (labelDist, index)
            isLabelMin = True
    return (minIndex, isLabelMin)

# drags the board by alternatingly changing origin and moving click
def boardDragging(app, event):
    if not app.isBoardDragging:
        app.originalClick_X, app.originalClick_Y = app.board.getPointFromPixel(app, event.x, event.y)
        app.isBoardDragging = True
    else:
        newPoint = app.board.getPointFromPixel(app, event.x, event.y)
        dx = -newPoint[0] + app.originalClick_X
        dy = -newPoint[1] + app.originalClick_Y
        app.board.changeOrigin(app.board.originX + dx, app.board.originY + dy)
        app.isBoardDragging = False

# moves point to mouse coordinates
def pointDragging(app, event, index):
    newEventX, newEventY = app.board.getPointFromPixel(app, event.x, event.y)
    app.points[index].x = newEventX
    app.points[index].y = newEventY

# moves label to mouse coordinates
def labelDragging(app, event, index):
    newEventX, newEventY = app.board.getPointFromPixel(app, event.x, event.y)
    app.points[index].moveLabel(newEventX, newEventY)

def mouseDragged(app, event):
    app.lastActions.pop(0)
    app.lastActions.append(1)
    (minIndex, isLabelMin) = closestObject(app, event)
    if minIndex == -1:
        boardDragging(app, event)
    elif not isLabelMin:
        pointDragging(app, event, minIndex)
    else:
        labelDragging(app, event, minIndex)
    
def timerFired(app):
    app.lastActions.pop(0)
    app.lastActions.append(0)
    if app.lastActions == [0] * 10:
        app.isBoardDragging = False

def keyPressed(app, event):
    if event.key == 'Up':
        app.board.gridLineSpace = max(app.board.gridLineSpace-2, 10)
    elif event.key == 'Down':
        app.board.gridLineSpace = min(app.board.gridLineSpace+2, 30)

#################################################
# # VIEW
#################################################

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