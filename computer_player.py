#!/usr/bin/env python3

from player import Player
from random import randrange

import time

class ComputerPlayer(Player):

####################################################################################################
    def __init__(self, skill, gameState):
        # Skill level of AI
        self.skillLevel = skill
        # Status on move
        self.firstMove = True
        # Board size in x direction
        self.sizeX = gameState.sizeX
        # Board size in y direction
        self.sizeY = gameState.sizeY
        # Current Gamestate
        self.gameState = gameState
        # A count of computer moves
        self.moveCount = 0

####################################################################################################

    def seeBoard(self, gameState):
        # Ensure the computer is only getting information the player can see
        visibleBricks = gameState.visibleBricks

        return visibleBricks, gameState.bricks

####################################################################################################

    def first(self):
        visibleBricks, allBricks = self.seeBoard(self.gameState)
        invisible = []
        for coord in allBricks:
            if not allBricks[coord].visible:
                invisible.append(coord)

        coordinates = invisible[randrange(len(invisible))]

        # Set first move to false
        self.firstMove = False
        # Return the coordinates of the first move
        return coordinates

####################################################################################################

    def getMines(self, gameState):
        # Get list of visible bricks
        visibleBricks, allBricks = self.seeBoard(gameState)
        # Initialize a list of confirmed mines
        mines = []
        # For all visible bricks
        for brick in visibleBricks:
            # Initialize a list of candidates for mines
            mineCandidates = []
            # Initialize a count of the number of bricks touching
            bricksTouching = 0
            # Get list of coordinates surrounding brick
            checklist = self.getNearCoordinates(brick.coordinates[0], brick.coordinates[1])
            # For each coordinate surrounding the brick
            for coordinate in checklist:
                # If the brick at coordinate is not visible and not a flag
                if not allBricks[coordinate].visible:
                    # Increment bricksTouching count
                    bricksTouching += 1
                    # Add to mineCandidates
                    mineCandidates.append(coordinate)
            # If brick is touching the same number of bricks as mines
            if brick.touching == bricksTouching:
                # All bricks it is touching is a mine
                for coordinate in mineCandidates:
                    # If coordinate not already in mine list
                    if coordinate not in mines and not allBricks[coordinate].flag:
                        # Append to mine list
                        mines.append(coordinate)

        # Return a list of mines
        return mines

####################################################################################################

    def getSafeBricks(self, gameState):
        # Get list of visible bricks
        visibleBricks, allBricks = self.seeBoard(gameState)
        # A list of confirmed safe bricks
        clearBricks = []
        # For every visible brick
        for brick in visibleBricks:
            # Number of flags the brick is touching
            touchingFlags = 0
            # Get coordinates of surrounding bricks
            checklist = self.getNearCoordinates(brick.coordinates[0], brick.coordinates[1])
            # For every surrounding brick
            for coordinate in checklist:
                # If the surrounding brick is flagged
                if allBricks[coordinate].flag:
                    # Increment flag touch count
                    touchingFlags += 1
            # If brick is touching the same number of flags as bombs
            if touchingFlags == brick.touching:
                # For every surrounding brick
                for coordinate in checklist:
                    # If the surrounding brick is not flagged and not visible
                    if not allBricks[coordinate].flag and not allBricks[coordinate].visible:
                        # If not already in clear bricks
                        if coordinate not in clearBricks:
                            # It is a safe brick to click
                            clearBricks.append(coordinate)
        # Return safe bricks
        return clearBricks

####################################################################################################

    def getNearCoordinates(self, xIndex, yIndex):
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
