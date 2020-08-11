from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton
from PyQt5.QtGui import QIcon, QFont

import os
import sys


### Plan to make a generic board class and have ComputerBoard/PlayerBoard inherit it ###

class ComputerBoard(QGridLayout):
    def __init__(self, gameState, playerType):
        super().__init__()

        # Set spacing to zero
        self.setSpacing(0)
        # Button dictionary
        self.buttons = {}
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
            button = QPushButton()
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
            # Add to board
            self.addWidget(button, coordinates[0], coordinates[1])

    def changeBrick(self, info):
        gameState = info[1]
        coordinate = info[0]
        bricks = gameState.bricks

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
        elif not brick.visible and brick.flag:
            button.setIcon(QIcon(os.path.join(sys.path[0], "graphics/images/flagIcon.png")))
        elif not brick.visible and not brick.flag:
            button.setIcon(QIcon())

    def changeMany(self, gameState):
        bricks = gameState.bricks
        for coordinate in bricks:
            self.changeBrick([coordinate, gameState])

    def lose(self, coordinate, gameState):
        self.changeBoard(gameState)
        button = self.buttons[coordinate]
        button.setStyleSheet("background:red;")
