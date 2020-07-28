from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QIcon

import sys
import os

class Brick(QPushButton):
####################################################################################################
    def __init__(self, coordinates):
        # Initialize parent class
        super().__init__()
        # Set coordinates on initialization
        self.coordinates = coordinates
        # Default visibility is hidden
        self.visibility = "hidden"
        # Default not a bomb
        self.bomb = False
        # Number of bombs brick is touching
        self.touching = 0

        # Initial stylesheet
        self.defaultStyleSheet = "background:lightgrey;border-style:outset;border-width:4px;border-color:grey;width:15px;height:15px;"
        self.setStyleSheet(self.defaultStyleSheet)

        # Signals
        self.pressed.connect(self.brickPress)
        self.released.connect(self.brickRelease)

        # Image file locations
        self.image = {1:"images/number1Icon.png",
                      2:"images/number2Icon.png",
                      3:"images/number3Icon.png"}

####################################################################################################

    def setVisibility(self, visibility):

        # Set visibility
        self.visibility = visibility.lower()
        self.setStyleSheet("background:white; border-width:1px; border-color:black;width:15px;height:15px;")

        # If brick is a bomb
        if self.bomb == True:
            # Set bomb Icon
            self.setIcon(QIcon(os.path.join(sys.path[0], "images/bombIcon.png")))
        # If brick is touching any bombs
        elif self.bomb == False and self.touching > 0:
            self.setIcon(QIcon(os.path.join(sys.path[0], self.image[self.touching])))


####################################################################################################

    def setBomb(self):
        # Activate brick as bomb
        self.bomb = True

####################################################################################################

    def setTouching(self, number):
        # Set number of bombs brick is touching
        self.touching = number

####################################################################################################

    def brickPress(self):
        # If brick is hidden
        if self.visibility == "hidden":
            # Change styleSheet
            styleSheet = "background:darkgrey;border-style:inset;border-width:4px;border-color:grey;width:15px;height:15px;"
            self.setStyleSheet(styleSheet)
        # If brick is revealed
        else:
            # Keep styleSheet constant
            self.setStyleSheet("background:white; border-width:1px; border-color:black;width:15px;height:15px;")

####################################################################################################

    def brickRelease(self):
        # If brick is hidden
        if self.visibility == "hidden":
            # Change sytleSheet
            self.setStyleSheet(self.defaultStyleSheet)
        # If brick is revealed
        else:
            # Keep styleSheet constant
            self.setStyleSheet("background:white; border-width:1px; border-color:black;width:15px;height:15px;")
            self.setVisibility("revealed")


####################################################################################################
