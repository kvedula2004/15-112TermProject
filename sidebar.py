#################################################
# #  Button
#################################################

from cmu_112_graphics import *
from boardClass import *
from pointClass import *
from lineClasses import *
from polygonClasses import *

class Button(object):
    def __init__(self, app, buttonType, buttonObject):
        self.app = app
        self.bType = buttonType
        self.isClicked = False
        self.buttonObject = buttonObject
        self.buttonHeight =  app.height / 40
    
    def drawButton(self, canvas, startY):
        if self.bType == 'point':
            self.drawPointButton(canvas, startY)
        elif self.bType == 'line':
            self.drawLineButton(canvas, startY)
        elif self.bType == 'polygon':
            self.drawPolygonButton(canvas, startY)
        elif self.bType == 'circle':
            self.drawCircleButton(canvas, startY)
        elif self.bType == 'ellipse':
            self.drawEllipseButton(canvas, startY)

    def drawPointButton(self, canvas, startY):
        if self.isClicked:
            canvas.create_rectangle(0, startY - 10, self.app.width/10, startY + 10,
                                    fill = 'grey')
        point = self.buttonObject
        isDrawn = point.isDrawn
        color = 'white'
        if isDrawn: color = 'black'

        canvas.create_oval(10, startY - 5, 20, startY + 5, fill=color, width=1)
        canvas.create_text(20, startY, text=f' {point.label} : ({point.x:.2f}, {point.y:.2f})',
                            anchor = 'w', fill = 'black', font = 'Arial 15 bold')

    def drawLineButton(self, canvas, startY):
        if self.isClicked:
            canvas.create_rectangle(0, startY - 10, self.app.width/10, startY + 10,
                                    fill = 'grey')
        line = self.buttonObject
        isDrawn = line.isDrawn
        color = 'white'
        if isDrawn: color = 'black'

        canvas.create_oval(10, startY - 5, 20, startY + 5, fill=color, width=1)
        canvas.create_text(20, startY, 
                            text=f' {line.label} : Line({line.points[line.index1].label}, {line.points[line.index2].label})',
                            anchor = 'w', fill = 'black', font = 'Arial 15 bold')

    def drawPolygonButton(self, canvas, startY):
        if self.isClicked:
            canvas.create_rectangle(0, startY - 10, self.app.width/10, startY + 10,
                                    fill = 'grey')
        polygon = self.buttonObject
        isDrawn = polygon.isDrawn
        color = 'white'
        if isDrawn: color = 'black'

        polyStr = ''
        for index in polygon.indices:
            polyStr += self.app.points[index].label
        canvas.create_oval(10, startY - 5, 20, startY + 5, fill=color, width=1)
        canvas.create_text(20, startY, 
                            text=f' {polygon.label} : {polyStr}',
                            anchor = 'w', fill = 'black', font = 'Arial 15 bold')


#################################################
# #  Sidebar
#################################################

class Sidebar(object):
    def __init__(self, app):
        self.app = app
        self.clicked = False
        self.clickedObjectType, self.clickedObjectIndex = None, -1
        self.width = app.width / 9

        # picture modified from triangle tool logo from
        # https://www.geogebra.org/classic
        logo = app.loadImage('ggb112-logo.png')
        imageWidth = logo.size[0]
        self.scaledLogo = self.app.scaleImage(logo, self.width/imageWidth)
        self.logoHeight = self.scaledLogo.size[1]

        self.boxHeight = app.height/40

        self.pointButtons, self.showPoints = [Button(app, 'point', point) for point in app.points], True
        self.lineButtons, self.showLines = [Button(app, 'line', line) for line in app.lines], True
        self.polygonButtons, self.showPolygons = [Button(app, 'polygon', polygon) for polygon in app.polygons], True
        self.circleButtons, self.showCircles = [Button(app, 'circle', circle) for circle in app.circles], True
        self.ellipseButtons, self.showEllipses = [Button(app, 'ellipse', ellipse) for ellipse in app.ellipses], True

    def drawSidebar(self, canvas):
        canvas.create_rectangle(0,0, self.width, self.app.height, fill='white',
                                outline = 'black', width = 3)
        self.createLogo(canvas)
        self.drawPoints(canvas)
        self.drawLines(canvas)
        self.drawPolygons(canvas)
        self.drawCircles(canvas)
        self.drawEllipses(canvas)

    def createLogo(self, canvas):
        canvas.create_image(self.width/2, self.logoHeight/2, image=ImageTk.PhotoImage(self.scaledLogo))
        canvas.create_rectangle(0,0,self.width,self.logoHeight,outline = 'black', 
                                width = 3, fill = '')
    
    def drawPoints(self, canvas):
        startY = self.logoHeight + self.boxHeight/2
        headerText = 'Points v'
        if self.showPoints: headerText = 'Points ^'
        canvas.create_text(self.width/2, startY, anchor = 'c',
                           text = headerText, font = 'Arial 20 bold', fill = 'pink')

        if not self.showPoints: return
        for pointButton in self.pointButtons:
            startY += self.boxHeight
            pointButton.drawButton(canvas,startY)


    def drawLines(self, canvas):
        startY = self.logoHeight + self.boxHeight/2
        if self.showPoints:
            startY += self.boxHeight * len(self.pointButtons)
        startY += self.boxHeight

        headerText = 'Lines v'
        if self.showLines: headerText = 'Lines ^'
        canvas.create_text(self.width/2, startY, anchor = 'c',
                           text = headerText, font = 'Arial 20 bold', fill = 'pink')

        if not self.showLines: return
        for lineButton in self.lineButtons:
            startY += self.boxHeight
            lineButton.drawButton(canvas,startY)


    def drawPolygons(self, canvas):
        startY = self.logoHeight + self.boxHeight/2
        if self.showPoints:
            startY += self.boxHeight * len(self.pointButtons)
        if self.showLines:
            startY += self.boxHeight * len(self.lineButtons)
        startY += 2*self.boxHeight

        headerText = 'Polygons v'
        if self.showPolygons: headerText = 'Polygons ^'
        canvas.create_text(self.width/2, startY, anchor = 'c',
                           text = headerText, font = 'Arial 20 bold', fill = 'pink')

        if not self.showPolygons: return
        for polygonButton in self.polygonButtons:
            startY += self.boxHeight
            polygonButton.drawButton(canvas, startY)
        
    def drawCircles(self, canvas):
        pass

    def drawEllipses(self, canvas):
        pass

    def translateToButton(self, s):
        if s == 'point': return self.pointButtons
        if s == 'line': return self.lineButtons
        if s == 'polygon': return self.polygonButtons
        if s == 'circle': return self.circleButtons
        if s == 'ellipse': return self.ellipseButtons

    def clickButton(self, buttonType, index):
        if self.clicked == True:
            self.translateToButton(self.clickedObjectType)[self.clickedObjectIndex].isClicked = False
            if self.clickedObjectType == buttonType and self.clickedObjectIndex == index:
                self.clicked = False
                return
        self.translateToButton(buttonType)[index].isClicked = True
        self.clickedObjectType = buttonType
        self.clickedObjectIndex = index
        self.clicked = True

    def doButtonAction(self, x, y):
        if x > self.width or y < self.logoHeight: return

        y -= self.logoHeight
        oldY = y % self.boxHeight
        y = int(y // self.boxHeight)

        if y == 0: 
            self.showPoints = not self.showPoints
            return
        if self.showPoints:
            if y <= len(self.pointButtons):
                if Point.distance(x, oldY, 15, self.boxHeight/2) <= 5:
                    self.app.points[y-1].isDrawn = not self.app.points[y-1].isDrawn
                    return
                self.clickButton('point', y-1)
                return
            else:
                y -= (len(self.pointButtons)+1)
        else: y -= 1

        if y == 0: 
            self.showLines = not self.showLines
            return
        if self.showLines:
            if y <= len(self.lineButtons):
                if Point.distance(x, oldY, 15, self.boxHeight/2) <= 5:
                    self.app.lines[y-1].isDrawn = not self.app.lines[y-1].isDrawn
                    return
                self.clickButton('line', y-1)
                return
            else:
                y -= (len(self.lineButtons)+1)
        else: y -= 1

        if y == 0: 
            self.showPolygons = not self.showPolygons
            return
        if self.showPolygons:
            if y <= len(self.polygonButtons):
                if Point.distance(x, oldY, 15, self.boxHeight/2) <= 5:
                    self.app.polygons[y-1].isDrawn = not self.app.polygons[y-1].isDrawn
                    return
                self.clickButton('polygon', y-1)
                return
            else:
                y -= (len(self.polygonButtons)+1)
        else: y -= 1


                
    
