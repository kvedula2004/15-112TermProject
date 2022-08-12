#################################################
# # Input parser
#################################################

from cmu_112_graphics import *
from boardClass import *
from pointClass import *
from lineClasses import *
from polygonClasses import *
from circleClass import *
from ellipseClass import *
from sidebar import *

class InputParse(object):
    def __init__(self, app, input):
        self.input = input
        self.app = app
        self.output = ''


    @staticmethod
    def checkIntFloat(num):
        if num.isdigit(): return True
        try:
            float(num)
            return True
        except:
            return False

    def createPoint(self):
        # 'Point(...)' to '...'
        interior = self.input[6:-1]
        try:
            newInterior = tuple(interior.split(','))
            newInterior = [elem.strip() for elem in newInterior]
            if len(newInterior) == 2:
                if self.checkIntFloat(newInterior[0]) and self.checkIntFloat(newInterior[1]):
                    x, y = eval(newInterior[0]), eval(newInterior[1])
                    self.app.points.append(Point(self.app, x, y))
                    self.app.pointNames.add(self.app.points[-1].label)
                else:
                    self.output = 'Not valid point coordinates.'
            elif len(newInterior) == 3:
                if not(self.checkIntFloat(newInterior[0]) and self.checkIntFloat(newInterior[1])):
                    self.output = 'Not valid point coordinates.'
                elif newInterior[2] in self.app.pointNames:
                    self.output = 'Duplicate label.'
                else:
                    x, y = eval(newInterior[0]), eval(newInterior[1])
                    self.app.points.append(Point(self.app, x, y, pointName=newInterior[2]))
                    self.app.pointNames.add(newInterior[2])
            else:
                raise Exception
        except:
            interior = interior.strip()
            objectList = self.app.lines + self.app.polygons + self.app.circles
            objectNames = [anyObject.label for anyObject in objectList]
            for index in range(len(objectNames)):
                objLabel = objectNames[index]
                if interior == objLabel:
                    self.app.allPoints.append(Point(self.app,0,0,pointName='',currObject=objectList[index]))
                    self.app.pointNames.add(self.app.allPoints[-1].label)
                    return
            self.output = 'Not valid object.'

    def createLine(self):
        # 'Line(...)' to '...'
        interior = self.input[5:-1]
        try:
            newInterior = tuple(interior.split(','))
            newInterior = [elem.strip() for elem in newInterior]
            if len(newInterior) != 2:
                raise Exception
            pt1, pt2 = newInterior[0], newInterior[1]
            if pt1 not in self.app.pointNames or pt2 not in self.app.pointNames:
                raise Exception
            
            label = self.app.defaultObjNames[self.app.currObjIndex]
            self.app.currObjIndex += 1
            index1, index2 = 0, 0
            for i in range(len(self.app.allPoints)):
                point = self.app.allPoints[i]
                if point.label == pt1: index1 = i
                if point.label == pt2: index2 = i
            self.app.lines.append(Line(self.app, index1, index2, label))
        except:
            self.output = 'Not valid object.'

    def createPolygon(self):
        # 'Polygon(...)' to '...'
        interior = self.input[8:-1]
        try:
            newInterior = tuple(interior.split(','))
            newInterior = [elem.strip() for elem in newInterior]
            for ptLabel in newInterior:
                if ptLabel not in self.app.pointNames:
                    raise Exception
            
            polyLabel = self.app.defaultObjNames[self.app.currObjIndex]
            self.app.currObjIndex += 1
            labelIndices = [-1 for i in range(len(newInterior))]
            for i in range(len(self.app.allPoints)):
                label = self.app.allPoints[i].label
                for j in range(len(newInterior)):
                    if newInterior[j] == label:
                        labelIndices[j] = i
            self.app.polygons.append(Polygon(polyLabel, tuple(labelIndices), isDrawn = True))
        except:
            self.output = 'Not valid object.'

    def createCircle(self):
        # 'Circle(...)' to '...'
        interior = self.input[7:-1]
        try:
            newInterior = tuple(interior.split(','))
            newInterior = [elem.strip() for elem in newInterior]
            for ptLabel in newInterior:
                if ptLabel not in self.app.pointNames:
                    raise Exception
            if len(newInterior) > 3 or len(newInterior) < 2: raise Exception
            
            circleLabel = self.app.defaultObjNames[self.app.currObjIndex]
            self.app.currObjIndex += 1
            labelIndices = [-1, -1, -1]
            for i in range(len(self.app.allPoints)):
                label = self.app.allPoints[i].label
                for j in range(len(newInterior)):
                    if newInterior[j] == label:
                        labelIndices[j] = i
            if labelIndices[2] == -1:
                self.app.circles.append(Circle(circleLabel, labelIndices[0], labelIndices[1]))
            else:
                self.app.circles.append(Circle(circleLabel, labelIndices[0], labelIndices[1],
                                               index3=labelIndices[2]))
        except:
            self.output = 'Not valid object.'
            
    def createIntersection(self):
        # 'Intersect(...)' to '...'
        interior = self.input[10:-1]
        try:
            newInterior = tuple(interior.split(','))
            newInterior = [elem.strip() for elem in newInterior]
            if len(newInterior) != 2:
                self.output = 'Exactly 2 objects needed for intersection.'
                return
            obj1Type, obj1Index, obj2Type, obj2Index = -1, -1, -1, -1
            for i in range(len(self.app.objects)):
                for j in range(len(self.app.objects[i])):
                    if self.app.objects[i][j].label == newInterior[0]:
                        obj1Type, obj1Index = i, j
                    if self.app.objects[i][j].label == newInterior[1]:
                        obj2Type, obj2Index = i, j
            if obj1Type == -1 or obj1Index == -1 or obj2Type == -1 or obj2Index == -1:
                self.output = 'Not valid objects.'
                return
            if obj1Type == obj2Type and obj1Index == obj2Index:
                self.output = 'Cannot intersect an object with itself.'
                return
            self.app.intersections.append(Intersection(self.app,obj1Type,obj1Index,obj2Type,obj2Index))
        except:
            self.output = 'Not valid intersection.'
    
    def getArea(self):
        # 'Area(...)' to '...'
        interior = self.input[5:-1]
        for poly in self.app.polygons:
            if poly.label == interior:
                self.output = f'Area is {poly.computeArea(self.app):.2f}.'
                return
        self.output = 'Not valid polygon.'

    def createEllipse(self):
        # 'Ellipse(...)' to '...'
        interior = self.input[8:-1]
        try:
            newInterior = tuple(interior.split(','))
            newInterior = [elem.strip() for elem in newInterior]
            for ptLabel in newInterior:
                if ptLabel not in self.app.pointNames:
                    raise Exception
            if len(newInterior) != 3: raise Exception
            ellipseLabel = self.app.defaultObjNames[self.app.currObjIndex]
            self.app.currObjIndex += 1
            labelIndices = [-1, -1, -1]
            for i in range(len(self.app.allPoints)):
                label = self.app.allPoints[i].label
                for j in range(len(newInterior)):
                    if newInterior[j] == label:
                        labelIndices[j] = i
            self.app.ellipses.append(Ellipse(self.app, labelIndices[0], labelIndices[1], labelIndices[2], label))
        except:
            self.output = 'Not valid ellipse.'

    def parseInput(self):
        if self.input == None:
            self.output = ''
        elif self.input.startswith('Point'):
            self.createPoint()
        elif self.input.startswith('Line'):
            self.createLine()
        elif self.input.startswith('Polygon'):
            self.createPolygon()
        elif self.input.startswith('Circle'):
            self.createCircle()
        elif self.input.startswith('Intersect'):
            self.createIntersection()
        elif self.input.startswith('Area'):
            self.getArea()
        elif self.input.startswith('Ellipse'):
            self.createEllipse()
        else:
            self.output = 'Not valid input.'

        if self.output != '':
            self.app.showMessage(self.output)
            self.output = ''
