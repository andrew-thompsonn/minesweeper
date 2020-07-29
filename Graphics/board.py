from brick import Brick
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGridLayout
from PyQt5.QtGui import QIcon
from random import randrange

import os
import sys

# Need to add in condition for clicking on large area of empty bricks
# Need to add in condition for right clicking and flagging mines


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
        # For every brick
        for coord in self.bricks:
            # Get touch count for brick
            touchCount = self.getTouchingCount(coord[0], coord[1])
            # Set touch count for brick
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

        maxRowIndex = self.rows - 1
        maxColumnIndex = self.columns - 1

        count = 0

        # Coordinates to check for any brick not on the edge of the board
        checkAll = [(rowCoord-1,columnCoord-1),(rowCoord-1,columnCoord),(rowCoord-1,columnCoord+1),
                    (rowCoord+1,columnCoord-1),(rowCoord+1,columnCoord),(rowCoord+1,columnCoord+1),
                    (rowCoord, columnCoord-1) ,(rowCoord,columnCoord+1)]

        # Upper coordinates
        checkTop = [(rowCoord-1,columnCoord-1),(rowCoord-1,columnCoord),(rowCoord-1,columnCoord+1)]
        # Lower coordinates
        checkBottom = [(rowCoord+1,columnCoord-1),(rowCoord+1,columnCoord),(rowCoord+1,columnCoord+1)]
        # Coordinates to the right
        checkLeft = [(rowCoord-1,columnCoord-1), (rowCoord, columnCoord-1), (rowCoord+1, columnCoord-1)]
        # Coordinates to the left
        checkRight = [(rowCoord-1,columnCoord+1), (rowCoord,columnCoord+1), (rowCoord+1,columnCoord+1)]


        # Top row
        if rowCoord == 0 and (columnCoord < maxColumnIndex and columnCoord > 0):
            checklist = checkBottom
            checklist.append(checkRight[1])
            checklist.append(checkLeft[1])

        # Bottom row
        elif rowCoord == maxRowIndex and (columnCoord < maxColumnIndex and columnCoord > 0):
            checklist = checkTop
            checklist.append(checkLeft[1])
            checklist.append(checkRight[1])

        # Left column
        elif columnCoord == 0 and (rowCoord < self.rows - 1 and rowCoord > 0):
            checklist = checkRight
            checklist.append(checkTop[1])
            checklist.append(checkBottom[1])

        # Right column
        elif columnCoord + 1 == self.columns and (rowCoord < self.rows -1 and rowCoord > 0):
            checklist = checkLeft
            checklist.append(checkTop[1])
            checklist.append(checkBottom[1])

        # Top left corner
        elif columnCoord == 0 and rowCoord == 0:
            checklist = [checkBottom[1], checkBottom[2], checkRight[1]]
        # Bottom left corner
        elif columnCoord == 0 and rowCoord + 1 == self.rows:
            checklist = [checkTop[1], checkTop[2], checkRight[1]]
        # Top right corner
        elif columnCoord + 1 == self.columns and rowCoord == 0:
            checklist = [checkBottom[0], checkBottom[1], checkLeft[1]]
        # Bottom right corner
        elif columnCoord + 1 == self.columns and rowCoord + 1 == self.rows:
            checklist = [checkLeft[1], checkTop[0], checkTop[1]]

        # Anywhere not on border
        else:
            # Check everywhere
            checklist = checkAll

        # For each coordinate in the checklist
        for coordinate in checklist:
            # If a bomb exists at that coordinate, increment touchCount
            if self.bricks[coordinate].bomb == True:
                count += 1

        if count > 2:
            print(count, "({}, {})".format(rowCoord, columnCoord))
        # Return touch count
        return count
