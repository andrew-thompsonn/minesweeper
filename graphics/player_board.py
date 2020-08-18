from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import pyqtSignal

from graphics.button import Button

import os
import sys

####################################################################################################

class PlayerBoard(QGridLayout):
    # Custom signal for left click
    buttonLeftClick = pyqtSignal(object)
    # Custom signal to right click
    buttonRightClick = pyqtSignal(object)

####################################################################################################

    def __init__(self, gameState, playerType):
        # Initialize parent class
        super().__init__()

        # Set spacing to zero
        self.setSpacing(0)
        # Button dictionary
        self.buttons = {}
        # Reversed button dictionary
        self.buttonCoords = {}
        # Colors for numbers
        self.numberColors = {1:"blue",
                             2:"green",
                             3:"red",
                             4:"darkblue",
                             5:"navy",
                             6:"purple",
                             7:"orange"}

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
            # Connect left click
            button.leftClick.connect(self.handleLeftClick)
            # Connect right click
            button.rightClick.connect(self.handleRightClick)

####################################################################################################

    def handleRightClick(self):
        """ Handle the right clicks on the board

            Inputs:     None
            Ouputs:     None
        """
        # Get the sender
        button = self.sender()
        # Emit the signal for a right click
        self.buttonRightClick.emit(self.buttonCoords[button])

####################################################################################################

    def handleLeftClick(self):
        """ Handle the left clicks on the board

            Inputs:     None
            Outputs:    None
        """
        # Get the sender
        button = self.sender()
        # Emit the signal for a left clik
        self.buttonLeftClick.emit(self.buttonCoords[button])

####################################################################################################

    def changeBrick(self, info):
        """ Change the graphics of a single brick

            Inputs:     info <list>
            Oututs:     None
        """
        # Get the gamestate
        gameState = info[1]
        # Get the coordinate of the brick to be changed
        coordinate = info[0]
        # Get all the bricks
        bricks = gameState.bricks
        # Get the specific brick
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
                button.setIcon(QIcon(os.path.join(sys.path[0], "graphics/images/bombIcon.png")))
                button.setStyleSheet("background:white;border-width:1px;border-color:black;width:20px;height:20px;")
        # If not visible and flagged
        elif not brick.visible and brick.flag:
            button.setIcon(QIcon(os.path.join(sys.path[0], "graphics/images/flagIcon.png")))
        # If not visible and not flagged
        elif not brick.visible and not brick.flag:
            button.setIcon(QIcon())

####################################################################################################

    def changeMany(self, gameState):
        """ Change the graphics of many bricks on the board

            Inputs:     GameState <GameState>
            Outputs:    None
        """
        # Get all bricks
        bricks = gameState.bricks
        # For every brick
        for coordinate in bricks:
            # Change the graphcis of the brick
            self.changeBrick([coordinate, gameState])

####################################################################################################

    def lose(self, coordinate):
        """ Update the board graphics to represent a loss.

            Inputs:     coordinate <tuple>
            Outputs:    gameState <GameState>
        """
        # Get the button that lost the game
        button = self.buttons[coordinate]
        # Set background to red
        button.setStyleSheet("border: 3px solid; border-color:red;")

####################################################################################################
