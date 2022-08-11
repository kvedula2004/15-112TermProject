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
from circleClass import *
import copy


def appStarted(app):
    app.board = Board()
    
    app.isBoardDragging = False
    app.isPolygonDragging = False
    app.originalClick_X, app.originalClick_Y = 0, 0
    app.timerDelay = 20
    app.lastActions = [0] * 10

    app.defaultNames = []
    for row in range(10):
        for i in range(26):
            app.defaultNames.append(chr(ord('A')+i) + "'"*row)
    app.currIndex = 0

    app.points = []
    app.pointNames = set()
    app.points.append(Point(app, 0,5))
    app.pointNames.add(app.points[0].label)
    app.points.append(Point(app, 5,0))
    app.pointNames.add(app.points[1].label)
    app.points.append(Point(app, 10,10))
    app.pointNames.add(app.points[2].label)
    app.points.append(Point(app, 7,15))
    app.pointNames.add(app.points[3].label)
    
    app.intersections = []
    app.allPoints = []
    updateAllPoints(app)

    app.lines = []
    app.defaultObjNames = [ptName.lower() for ptName in app.defaultNames]
    app.currObjIndex = 10
    app.lines.append(Line(app, 0, 1, 'a'))
    app.lines.append(Line(app, 2, 3, 'b'))

    app.polygons = []
    app.polygons.append(Polygon('g', (0,1,2,3)))
    #app.polygons.append(Polygon('h', (0,1,2)))

    app.circles = []
    app.circles.append(Circle('m', 0, 1))
    app.circles.append(Circle('n', 0, 1, index3 = 2))

    app.ellipses = []

    app.objects = [app.lines, app.polygons, app.circles, app.ellipses]
    app.intersections = [Intersection(app,2,1,2,0), Intersection(app, 0,0,0,1)]
    updateAllPoints(app)

    

    app.sidebar = Sidebar(app)
    app.inputParse = InputParse(app, '')

def updateAllPoints(app):
    app.allPoints = [] + app.points
    for intersection in app.intersections:
        intersection.updateIntersection()
        ogLen = len(app.allPoints)
        app.allPoints.extend([1 for i in range(len(intersection.labels))])
        for i in range(len(intersection.labels)):
            app.allPoints[ogLen+i] = Point(app, intersection.allIntersections[i][0],
                                                     intersection.allIntersections[i][1],
                                                     intersection.labels[i],
                                                     canMove = False)
    
    
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

def closestPolygon(app, event):
    newX, newY = app.board.getPointFromPixel(app, event.x, event.y)
    minIndex = None
    minDist = None
    for i in range(len(app.polygons)):
        if minIndex == None:
            minIndex = i
            minDist = app.polygons[i].distance(app, newX, newY)
            continue
        polygon = app.polygons[i]
        if minDist == None or polygon.distance(app, newX, newY) < minDist:
            minDist = polygon.distance(app, newX, newY)
            minIndex = i
    return (minIndex, minDist)

def polygonDragging(app, event):
    if not app.isPolygonDragging:
        app.originalClick_X, app.originalClick_Y = app.board.getPointFromPixel(app, event.x, event.y)
        app.isPolygonDragging = True
    else:
        newPoint = app.board.getPointFromPixel(app, event.x, event.y)
        dx = -newPoint[0] + app.originalClick_X
        dy = -newPoint[1] + app.originalClick_Y
        minIndex = closestPolygon(app, event)[0]
        app.polygons[minIndex].movePolygon(app, -dx, -dy)
        app.isPolygonDragging = False


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
    app.sidebar.__init__(app)
    app.lastActions.pop(0)
    app.lastActions.append(1)
    (minIndex, isLabelMin) = closestObject(app, event)
    polyDist = closestPolygon(app, event)[1]
    if minIndex == -1:
        if polyDist < 2:
            polygonDragging(app, event)
        else:
            boardDragging(app, event)
    elif not isLabelMin:
        pointDragging(app, event, minIndex)
    else:
        labelDragging(app, event, minIndex)
    
def timerFired(app):
    # clears up the queue of past dragging history (1 = drag, 0 = not drag)
    updateAllPoints(app)
    app.lastActions.pop(0)
    app.lastActions.append(0)
    if app.lastActions == [0] * 10:
        app.isBoardDragging = False
        app.isPolygonDragging = False

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
        app.sidebar.__init__(app)
        return


#################################################
# # VIEW
#################################################

# draws all points in app.points
def drawPoints(app, canvas):
    for point in app.allPoints:
        point.movePoint(point.x, point.y)
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

def drawCircles(app, canvas):
    for circle in app.circles:
        circle.drawCircle(app.board, app, canvas)

def redrawAll(app, canvas):
    app.board.drawBoard(app, canvas)
    drawPolygons(app, canvas)
    drawCircles(app, canvas)
    drawLines(app, canvas)
    drawPoints(app, canvas)
    app.sidebar.drawSidebar(canvas)
    

def main():
    runApp(width = 1440, height = 785)

if (__name__ == '__main__'):
    main()