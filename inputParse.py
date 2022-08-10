#################################################
# # Input parser
#################################################

from cmu_112_graphics import *
from boardClass import *
from pointClass import *
from lineClasses import *
from polygonClasses import *
from sidebar import *

# TODO fix
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
                    self.app.points.append(Point(self.app, x, y, newInterior[2]))
                    self.app.pointNames.add(self.app.points[-1].label)
            else:
                raise Exception
        except:
            interior = interior.strip()
            objectList = self.app.lines + self.app.polygons
            objectNames = [anyObject.label for anyObject in objectList]
            for index in range(len(objectNames)):
                objLabel = objectNames[index]
                if interior == objLabel:
                    self.app.points.append(Point(self.app,0,0,'',objectList[index]))
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
            for i in range(len(self.app.points)):
                point = self.app.points[i]
                if point.label == pt1: index1 = i
                if point.label == pt2: index2 = i
            self.app.lines.append(Line(self.app.points, index1, index2, label))
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
            for i in range(len(self.app.points)):
                label = self.app.points[i].label
                for j in range(len(newInterior)):
                    if newInterior[j] == label:
                        labelIndices[j] = i
            self.app.polygons.append(Polygon(polyLabel, tuple(labelIndices), isDrawn = True))
        except:
            self.output = 'Not valid object.'

    def parseInput(self):
        if self.input.startswith('Point'):
            self.createPoint()
        elif self.input.startswith('Line'):
            self.createLine()
        elif self.input.startswith('Polygon'):
            self.createPolygon()
        else:
            self.output = 'Not valid input.'

        if self.output != '':
            self.app.showMessage(self.output)
            self.output = ''
