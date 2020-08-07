#!/usr/bin/env python3

from game_components.brick import Brick

from random import randrange
from os import system

class GameState():
    """ Class for the current game state of a minesweeper game."""
####################################################################################################

    def __init__(self, sizeX, sizeY, mines):
        # Size in x direction
        self.sizeX = sizeX
        # Size in Y direction
        self.sizeY = sizeY
        # Number of mines
        self.mines = mines
        # Game status 0 = active, 1 = won, 2 = lost
        self.status = 0
        # Dictionary with key = coordinates, value = brick
        self.bricks = {}
        # Mine coordinates
        self.mineCoords = []
        # Count of bricks flagged
        self.flags = mines
        # Visible bricks
        self.visibleBricks = []
        # Flag locations
        self.flagCoords = []

        # Initializing game board (Holds all bricks and their information)
        self.bricks = self.createBoard(self.sizeX, self.sizeY)
        # Filling the bricks in the board with mines
        self.fillMines(self.sizeX, self.sizeY, self.mines)
        # For every brick in board
        for coordinates in self.bricks:
            # Get surrounding coordinates
            checklist = self.surroundingCoordinates(coordinates[0], coordinates[1])
            # Calculate the number of mines near
            touching = self.getTouchingCount(checklist)
            # Set number of mines in brick
            self.bricks[coordinates].setTouching(touching)

####################################################################################################

    def createBoard(self, sizeX, sizeY):
        """ Create a dictionary containing a brick's coordinates as the key, and the brick as
            the value

            Inputs:     sizeX <int>
                        sizeY <int>
            Outputs:    board <dict>
        """
        # Initialize bricks dict
        bricks = {}
        # For all rows
        for yIndex in range(sizeY):
            # For all columns in row
            for xIndex in range(sizeX):
                # Define coordinates
                coordinates = (xIndex, yIndex)
                # Create new brick at current coordinate
                brick = Brick(coordinates)
                # Coordinates of brick
                coordinates = (xIndex, yIndex)
                # Add brick to dictionary
                bricks[coordinates] = brick
        # Return dictionary
        return bricks


####################################################################################################

    def fillMines(self, sizeX, sizeY, mines):
        """ Based on number of mines and size, picks random coordinates to place mines, and activates
            bricks as mines at those coordinates

            Inputs:     sizeX <int>
                        sizeY <int>
                        mines <int>
            Outputs:    None
        """
        # Number of mines added
        mineCount = 0
        # While number of mines is not the number requested
        while mineCount != mines:
            # Generate random x and y coordinate
            coordinates = (randrange(sizeX), randrange(sizeY))
            # Get brick at those coordinates
            currentbrick = self.bricks[coordinates]
            # If brick at coordinate is not a bomb
            if currentbrick.mine == False:
                # Set brick to be a bomb
                currentbrick.setMine()
                # Increment bomb count
                mineCount += 1
                # Save the coordinates of bomb (debugging only)
                self.mineCoords.append(coordinates)

####################################################################################################

    def surroundingCoordinates(self, xIndex, yIndex):
        """ Gets a list of the coordinates surrounding any brick. Takes into account corners and
            edges. Returns a list of tuples representing coordinates

            Inputs:     xIndex <int>
                        yIndex <int>
            Outputs:    checklist <[(int)]>
        """
        maxXIndex = self.sizeX - 1
        maxYIndex = self.sizeY - 1

        # Coordinates to check for any brick not on the edge of the board
        checkAll = [(xIndex, yIndex-1) ,(xIndex,yIndex+1), (xIndex-1,yIndex), (xIndex+1,yIndex),
                    (xIndex-1,yIndex-1),(xIndex-1,yIndex+1),(xIndex+1,yIndex-1),(xIndex+1,yIndex+1)]


        # Upper coordinates
        checkTop = [(xIndex-1,yIndex-1),(xIndex-1,yIndex),(xIndex-1,yIndex+1)]
        # Lower coordinates
        checkBottom = [(xIndex+1,yIndex-1),(xIndex+1,yIndex),(xIndex+1,yIndex+1)]
        # Coordinates to the right
        checkLeft = [(xIndex-1,yIndex-1), (xIndex, yIndex-1), (xIndex+1, yIndex-1)]
        # Coordinates to the left
        checkRight = [(xIndex-1,yIndex+1), (xIndex,yIndex+1), (xIndex+1,yIndex+1)]

        # Top row
        if xIndex == 0 and (yIndex < maxYIndex and yIndex > 0):
            checklist = checkBottom
            checklist.append(checkRight[1])
            checklist.append(checkLeft[1])
        # Bottom row
        elif xIndex == maxXIndex and (yIndex < maxYIndex and yIndex > 0):
            checklist = checkTop
            checklist.append(checkLeft[1])
            checklist.append(checkRight[1])
        # Far left column
        elif yIndex == 0 and (xIndex <  maxXIndex and xIndex > 0):
            checklist = checkRight
            checklist.append(checkTop[1])
            checklist.append(checkBottom[1])
        # Far right column
        elif yIndex == maxYIndex and (xIndex < maxXIndex and xIndex > 0):
            checklist = checkLeft
            checklist.append(checkTop[1])
            checklist.append(checkBottom[1])

        # Top left corner
        elif yIndex == 0 and xIndex == 0:
            checklist = [checkBottom[1], checkBottom[2], checkRight[1]]
        # Bottom left corner
        elif yIndex == 0 and xIndex == maxXIndex:
            checklist = [checkTop[1], checkTop[2], checkRight[1]]
        # Top right corner
        elif yIndex == maxYIndex and xIndex == 0:
            checklist = [checkBottom[0], checkBottom[1], checkLeft[1]]
        # Bottom right corner
        elif yIndex == maxYIndex and xIndex == maxXIndex:
            checklist = [checkLeft[1], checkTop[0], checkTop[1]]

        # Non-edges
        else:
            # Check everywhere
            checklist = checkAll

        return checklist

####################################################################################################

    def getTouchingCount(self, checklist):
        """ Get the number of mines a brick is touching. Will check any list of coordinates
            surrounding a brick and count the number of mines touching

            Inputs:     checklist [(<int>)]
            Outputs:    count <int>
        """
        # Mine counter
        count = 0
        # For all bricks touching xIndex,yIndex
        for coordinates in checklist:
            # If brick is a mine
            if self.bricks[coordinates].mine == True:
                # Increment count
                count += 1

        # Return the mine count
        return count

####################################################################################################

    def clickBrick(self, coordinate):
        """ Left click a brick. Checks for a win or loss.

            Inputs:     coordinate (<int>)
            Outputs:    None
        """
        # Set brick as visible
        self.bricks[coordinate].setVisibility(True)
        # Add to visible list
        self.visibleBricks.append(self.bricks[coordinate])
        # If brick is mine
        if self.bricks[coordinate].mine == True:
            # Lose game
            self.loseGame()
        # Check for win
        self.checkWin()

####################################################################################################

    def clickMany(self, coordinate):
        """ Clicks several bricks. Called when an empty brick is clicked that is touching no mines.
            If a brick is empty, checks for all near by empty bricks and clicks them as well

            Inputs:     coordinate (<int)
            Outputs:    None
        """
        # A count of empty bricks
        emptyBricks = 0
        # List of bricks to click
        clickList = [coordinate]
        # Empty brick list
        emptyList = [coordinate]

        # Counter
        count = 0
        # While more emptybricks exist
        while count < emptyBricks+1:
            # Current coordinates
            coordinates = emptyList[count]
            # Current brick
            currentBrick = self.bricks[coordinates]
            # Check list of surrounding bricks
            checklist = self.surroundingCoordinates(coordinates[0], coordinates[1])
            # For all bricks in checklist
            for coord in checklist:
                # If brick is empty
                if (self.bricks[coord].touching==0 and not self.bricks[coord].mine) and (coord not in emptyList):
                    # Increment empty brick found count
                    emptyBricks += 1
                    # Add coordinates to emptyList
                    emptyList.append(coord)
                    # Add coordinates to clickList
                    clickList.append(coord)
                # If brick is a number
                elif self.bricks[coord].touching>0 and not self.bricks[coord].mine and (coord not in clickList):
                    # Add coordinate to clickList
                    clickList.append(coord)
            # Increment count
            count += 1

        # For all bricks in the click list
        for brick in clickList:
            # Click the brick
            self.clickBrick(brick)

####################################################################################################

    def flagBrick(self, coordinates):
        """ Flags a brick and updates flag count. Checks for win.

            Inputs:     coordinates (<int>)
            Outputs     None
        """
        if not self.bricks[coordinates].visible:

            # Set brick as flagged
            self.bricks[coordinates].setFlag()
            # Increment flag count
            if self.bricks[coordinates].flag:
                # Add to flag location list
                self.flagCoords.append(coordinates)
                self.flags -= 1
            else:
                self.flagCoords.remove(coordinates)
                self.flags +=1
            # If same amount of flags as mine
            if self.flags == self.mines:
                # Check for a win
                self.checkWin()



####################################################################################################

    def checkWin(self):
        """ Checks for win by counting correct flags and number of visible bricks

            Inputs:     None
            Outputs:    None
        """
        # Correct number of flags
        correct = 0
        # For all mines
        for coordinates in self.mineCoords:
            # If mine is flagged
            if self.bricks[coordinates].flag:
                # Increment correct count
                correct += 1

        # Number of bricks that are visible
        visible = 0
        # For all bricks
        for coordinates in self.bricks:
            # If brick is visible
            if self.bricks[coordinates].visible:
                # Increment visible count
                visible += 1

        # If all mines are flagged or all bricks that aren't mines are visible
        if correct == self.mines or visible == (self.sizeX*self.sizeY) - self.mines:
            # Win the game !
            self.win()

####################################################################################################

    def win(self):
        """ Update game status to reflect a win, and show the whole board

            Inputs:     None
            Outputs:    None
        """
        # For all bricks
        for coord in self.bricks:
            # If brick is not a mine
            if not self.bricks[coord].mine:
                # Set visible
                self.bricks[coord].setVisibility(True)
            # If brick is a mine and not flagged
            elif self.bricks[coord].mine and not self.bricks[coord].flag:
                # Flag brick
                self.flagBrick(coord)
        # Set status to won
        self.status = 1

####################################################################################################

    def loseGame(self):
        """ Called when the game is lost. Reveals all bricks, and updates game status to reflect a
            Loss

            Inputs:     None
            Outputs:    None
        """
        # For all bricks
        for coord in self.bricks:
            # Set visibility to True
            self.bricks[coord].setVisibility(True)
        # Set status of game as lost
        self.status = 2

####################################################################################################

    def printBoard(self):
        """ Helper function to print the game board without using graphics """
        #system('clear')

        # Print y axis
        for yIndex in range(self.sizeY):
            print(" {}  ".format(yIndex), end = "")
        # Spacing
        print("\n\n")
        # For all rows
        for xIndex in range(self.sizeX):
            # For all columns
            for yIndex in range(self.sizeY):
                # If hidden and unflagged
                if self.bricks[(xIndex, yIndex)].visible == False and self.bricks[(xIndex, yIndex)].flag == False:
                    print("[-] ", end = "")
                # If hidden and flagged
                elif self.bricks[(xIndex, yIndex)].visible == False and self.bricks[(xIndex, yIndex)].flag == True:
                    print("[F] ", end = "")
                # If visible and mine
                elif self.bricks[(xIndex, yIndex)].visible == True and self.bricks[(xIndex, yIndex)].mine == True:
                    print("(#) ", end = "")
                # If visible and touching mines
                elif self.bricks[(xIndex, yIndex)].visible == True and self.bricks[(xIndex, yIndex)].touching > 0:
                    print("|{}| ".format(self.bricks[(xIndex, yIndex)].touching), end = "")
                # If visible and touching no mines
                else:
                    print("|_| ", end = "")
            # Print x axis
            print("\t{}".format(xIndex))
        # Spacing
        print("\n\n")

####################################################################################################
