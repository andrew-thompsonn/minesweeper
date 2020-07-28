from brick import Brick
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGridLayout
from PyQt5.QtGui import QIcon
from random import randrange

import os
import sys


class Board(QGridLayout):
    """ Class for minesweeper board. Contains N x N bricks."""
####################################################################################################
    def __init__(self, sizeX, sizeY, mines):
        """ Initialize the board. Create sizeX by size Y grid filled with bricks. Randomly select
            bricks to be mines.

            Inputs:     sizeX <int>
                        sizeY <int>
                        mines <int>

            Outputs:    None
        """
        super().__init__()
        self.boardState = 0
        self.columns = sizeX
        self.rows = sizeY

        #-------------------------------------------------------------------------------------------
        # Fill board with bricks
        #-------------------------------------------------------------------------------------------
        # Make the bricks touch
        self.setSpacing(0)
        # Initialize bricks dictionary
        self.bricks = {}
        # Initialize a counter
        count = 0
        # For all x coordinates
        for columnIndex in range(self.columns):
            # For all y coordinates
            for rowIndex in range(self.rows):
                # Create brick at (x, y)
                brick = Brick((rowIndex, columnIndex))
                # Add to QGridLayout
                self.addWidget(brick, rowIndex, columnIndex)
                # Add to dictionary. Key = coordinates, Value = brick
                self.bricks[(rowIndex, columnIndex)] = brick
                # Connect clicked signal
                brick.clicked.connect(self.clickedHandler)

        #-------------------------------------------------------------------------------------------
        # Randomly place mines
        #-------------------------------------------------------------------------------------------
        # Count for mines generated
        mineCount = 0
        # List of bomb coordinates
        mineCoords = []
        # While number of mines is less than input
        while mineCount < mines:
            # Generate a random x index
            columnIndex = randrange(self.columns)
            # Generate a random y index
            rowIndex = randrange(self.rows)
            # If brick at x,y is not a bomb
            if self.bricks[(rowIndex, columnIndex)].bomb == False:
                # Set as bomb
                self.bricks[(rowIndex, columnIndex)].setBomb()
                # Create mine coordinates
                coords = (rowIndex, columnIndex)
                print(coords)
                # Append to coordinates list
                mineCoords.append(coords)
                # Increment mine count
                mineCount += 1

        #-------------------------------------------------------------------------------------------
        # Set number of mines touching
        #-------------------------------------------------------------------------------------------
        for coord in self.bricks:
            touchCount = self.getTouchingCount(coord[0], coord[1])
            self.bricks[coord].setTouching(touchCount)


####################################################################################################

    def clickedHandler(self, event):
        # Determine sender
        brick = self.sender()
        # If brick is a bomb
        if brick.bomb == True:
            # Lose game
            self.lose()

####################################################################################################

    def lose(self):
        # Board State = lost
        self.boardState = 1
        # Expose all bricks
        self.__expose()

####################################################################################################

    def __expose(self):
        for coord in self.bricks:
            self.bricks[coord].setVisibility("revealed")

####################################################################################################

    def getTouchingCount(self, rowCoord, columnCoord):
        coords = (rowCoord, columnCoord)
        if self.bricks[coords].bomb == True:
            return 0

        count = 0
        checkList = [(rowCoord-1,columnCoord-1),(rowCoord-1,columnCoord),(rowCoord-1,columnCoord+1),
                     (rowCoord,columnCoord-1),  (rowCoord,columnCoord+1),
                     (rowCoord+1,columnCoord-1),(rowCoord+1,columnCoord),(rowCoord+1,columnCoord+1)]

        for coordinate in checkList:
            if rowCoord - 1 >= 0 and rowCoord + 1 < self.rows:
                if columnCoord - 1 >= 0 and columnCoord + 1 < self.columns:
                    try:
                        if self.bricks[coordinate].bomb == True:
                            count += 1
                    except:
                        pass
        return count
