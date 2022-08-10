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
        return num.isdigit() or num.isfloat()

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

    def parseInput(self):
        if self.input.startswith('Point'):
            self.createPoint()
        else:
            self.output = 'Not valid input.'

        if self.output != '':
            self.app.showMessage(self.output)
            self.output = ''
