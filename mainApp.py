#################################################
# # Main app
#################################################

from cmu_112_graphics import *
from boardClass import *
from pointClass import *
from lineClasses import *
from polygonClasses import *
from sidebar import *
from inputParse import *


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
    app.points.append(Point(app, 7,15))

    app.lines = []
    app.lines.append(Line(app.points, 0, 1, 'a'))

    app.polygons = []
    app.polygons.append(Polygon('g', app.points, True, 0,1,2,3))
    app.polygons.append(Polygon('h', app.points, True, 0,1,2))

    app.circles = []

    app.ellipses = []

    app.sidebar = Sidebar(app)
    app.inputParse = InputParse(app, '')
    
    
# computes the closest object among points, point labels
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
        pointDist = Point.distance(point.x, point.y, newEventX, newEventY) / 2
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
    app.points[index].movePoint(newEventX, newEventY)

# moves (point) label to mouse coordinates
def labelDragging(app, event, index):
    newEventX, newEventY = app.board.getPointFromPixel(app, event.x, event.y)
    app.points[index].moveLabel(newEventX, newEventY)

def mouseDragged(app, event):
    # does the necessary draggings of board,label,point
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
    # clears up the queue of past dragging history (1 = drag, 0 = not drag)
    app.lastActions.pop(0)
    app.lastActions.append(0)
    if app.lastActions == [0] * 10:
        app.isBoardDragging = False

def keyPressed(app, event):
    # zooms in and out
    if event.key == 'Up':
        app.board.gridLineSpace = max(app.board.gridLineSpace-2, 10)
    elif event.key == 'Down':
        app.board.gridLineSpace = min(app.board.gridLineSpace+2, 20)

def mousePressed(app, event):
    app.sidebar.doButtonAction(event.x, event.y)
    if event.x <= app.sidebar.scaledLogo.size[0] and event.y <= app.sidebar.scaledLogo.size[1]:
        input = app.getUserInput('Enter a valid command')
        app.inputParse.input = input
        app.inputParse.parseInput()


#################################################
# # VIEW
#################################################

# draws all points in app.points
def drawPoints(app, canvas):
    for point in app.points:
        point.drawPoint(app.board, app, canvas)
 
 # draws all lines in app.lines
def drawLines(app, canvas):
    for line in app.lines:
        if not isinstance(line, LineSegment):
            line.drawLine(app.board, app, canvas)
        else:
            line.drawLineSegment(app.board, app, canvas)

# draws all polygons in app.polygons
def drawPolygons(app, canvas):
    for polygon in app.polygons:
        polygon.drawPolygon(app.board, app, canvas)

def redrawAll(app, canvas):
    app.board.drawBoard(app, canvas)
    drawPolygons(app, canvas)
    drawLines(app, canvas)
    drawPoints(app, canvas)
    app.sidebar.drawSidebar(canvas)
    

def main():
    runApp(width = 2000, height = 800)

if (__name__ == '__main__'):
    main()