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

    def parseInput(self):
        self.app.showMessage(f'You entered: {self.input}')