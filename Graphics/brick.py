from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QIcon, QFont

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
        # Default unflagged
        self.flagged = False
        # Number of bombs brick is touching
        self.touching = 0
        # Set fixed dimensions
        self.setFixedWidth(35)
        self.setFixedHeight(35)

        # Initial stylesheet
        self.defaultStyleSheet = "background:lightgrey;border-style:outset;border-width:4px;border-color:grey;width:20px;height:20px;"
        self.setStyleSheet(self.defaultStyleSheet)

        # Signals
        self.pressed.connect(self.brickPress)
        self.released.connect(self.brickRelease)

        # Image file locations
        self.buttonStyles = {1:"color:blue;",
                             2:"color:green",
                             3:"color:red",
                             4:"color:darkblue",
                             5:"color:darkred",
                             6:"color:purple"}

####################################################################################################

    def setVisibility(self, visibility):

        # Set visibility
        self.visibility = visibility.lower()
        self.setStyleSheet("background:white; border-width:1px; border-color:black;width:20px;height:20px;")

        # If brick is a bomb
        if self.bomb == True:
            # Set bomb Icon
            self.setIcon(QIcon(os.path.join(sys.path[0], "images/bombIcon.png")))
        # If brick is touching any bombs
        elif self.bomb == False and self.touching > 0:
            self.setText(str(self.touching))
            self.setFont(QFont('Ariel', 15))
            self.setStyleSheet(self.buttonStyles[self.touching])


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
            styleSheet = "background:darkgrey;border-style:inset;border-width:4px;border-color:grey;width:20px;height:20px;"
            self.setStyleSheet(styleSheet)
        # If brick is revealed
        else:
            # Keep styleSheet constant
            self.setStyleSheet("background:white; border-width:1px; border-color:black;width:20px;height:20px;")

####################################################################################################

    def brickRelease(self):
        # If brick is hidden
        if self.visibility == "hidden":
            # Change sytleSheet
            self.setVisibility("revealed")
        # If brick is revealed
        else:
            # Keep styleSheet constant
            self.setStyleSheet("background:white; border-width:1px; border-color:black;width:20px;height:20px;")


####################################################################################################
