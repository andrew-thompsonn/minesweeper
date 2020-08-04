from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import pyqtSignal

from button import Button

import os
import sys

class PlayerBoard(QGridLayout):
    buttonLeftClick = pyqtSignal(object)
    buttonRightClick = pyqtSignal(object)
    def __init__(self, gameState, playerType):
        super().__init__()

        # Set spacing to zero
        self.setSpacing(0)
        # Button dictionary
        self.buttons = {}
        self.buttonCoords = {}
        # Colors for numbers
        self.numberColors = {1:"blue",
                             2:"green",
                             3:"red",
                             4:"darkblue",
                             5:"navy",
                             6:"purple"}

        # For all bricks in the current gamestate
        for coordinates in gameState.bricks:
            # Create button to represent brick
            button = Button()
            # Set fixed Width
            button.setFixedWidth(35)
            # Set fixed height
            button.setFixedHeight(35)
            # Style sheet for buttons
            styleSheet = "background:lightgrey;border-style:outset;border-width:4px;border-color:grey;width:20px;height:20px;"
            # Set button style sheet
            button.setStyleSheet(styleSheet)
            # Add to dictionary for signal management
            self.buttons[coordinates] = button
            self.buttonCoords[button] = coordinates
            # Add to board
            self.addWidget(button, coordinates[0], coordinates[1])
            # Connect to pressed and released
            button.pressed.connect(self.buttonPress)
            button.released.connect(self.buttonRelease)

            button.leftClick.connect(self.handleLeftClick)
            button.rightClick.connect(self.handleRightClick)


    def handleRightClick(self):
        button = self.sender()
        self.buttonRightClick.emit(self.buttonCoords[button])

    def handleLeftClick(self):
        button = self.sender()
        self.buttonLeftClick.emit(self.buttonCoords[button])

    def changeBoard(self, gameState):
        bricks = gameState.bricks
        # For all bricks
        for coordinate in bricks:
            # Define current bricks
            brick = bricks[coordinate]
            # Define current button
            button = self.buttons[coordinate]

            # If the brick is visible
            if brick.visible:
                # If the brick is not a mine and not touching mines
                if brick.mine == False and brick.touching == 0:
                    button.setStyleSheet("background:white;border-width:1px;border-color:black;width:20px;height:20px;")
                # If brick is not a mine and touching mines
                elif brick.mine == False and brick.touching > 0:
                    button.setStyleSheet("background:white;border-width:1px;border-color:black;width:20px;height:20px;color:{}".format(self.numberColors[brick.touching]))
                    button.setText(str(brick.touching))
                    button.setFont(QFont('Ariel', 14))

                # If brick is a mine
                elif brick.mine:
                    button.setIcon(QIcon(os.path.join(sys.path[0], "images/bombIcon.png")))
                    button.setStyleSheet("background:white;border-width:1px;border-color:black;width:20px;height:20px;")
            elif not brick.visible and brick.flag:
                button.setIcon(QIcon(os.path.join(sys.path[0], "images/flagIcon.png")))
            elif not brick.visible and not brick.flag:
                button.setIcon(QIcon())

    def buttonPress(self):
        x = 1

    def buttonRelease(self):
        x = 2
