#!/usr/bin/env python3

from player import Player
from random import randrange

import time

class ComputerPlayer(Player):
####################################################################################################
    def __init__(self, skill, gameState):
        # Skill level of AI
        self.skillLevel = skill
        # Queue for actions the AI decides to perform
        self.actionQueue = {}
        # Dictionary of bricks in current game state
        self.bricks = {}
        # Status on move
        self.firstMove = True
        # Board size in x direction
        self.sizeX = 0
        # Board size in y direction
        self.sizeY = 0
        # Current Gamestate
        self.gameState = gameState

####################################################################################################
    def seeBoard(self, gameState):
        # If it is the first move
        if self.firstMove:
            # Get the size of the board
            self.sizeX = gameState.sizeX
            self.sizeY = gameState.sizeY

        # Get bricks from game state
        self.bricks = gameState.bricks
####################################################################################################
    def getMove(self):
        # View the current game state
        self.seeBoard(self.gameState)

        # If it is the first move
        if self.firstMove:
            # Generate random coordinates
            coordinates = (randrange(self.sizeX), randrange(self.sizeY))
            # Action is a left click
            actionType = "leftclick"
            # No longer first move
            self.firstMove = False
            # Return actionType and coordinates for first move
            self.actionQueue[coordinates] = actionType

        # If it is not the first move
        else:
            # List of bricks that the computer can draw information from
            visibleBricks = []
            # Get all visible bricks
            for coord in self.bricks:
                # If brick is visible and unflagged
                if (self.bricks[coord].visible and self.bricks[coord].flag == False) and self.bricks[coord].touching > 0:
                    # Add to visible brick list
                    visibleBricks.append(self.bricks[coord])

            for brick in visibleBricks:
                # Get list of surrounding bricks
                checklist = self.surroundingCoordinates(brick.coordinates[0], brick.coordinates[1])
                # List of candidate squares for mines
                mineCandidates = []
                # For all surrounding bricks
                for coord in checklist:
                    # If brick is unclicked and unflagged
                    if self.bricks[coord].visible == False and self.bricks[coord].flag == False:
                        # Add brick as a candidate for mine
                        mineCandidates.append(coord)

                # If number of mine candidates equals the number of mines current brick is touching
                if len(mineCandidates) == brick.touching:
                    # For all mines in mine candidate list
                    for mine in mineCandidates:
                        # Create action for mine as flag
                        self.actionQueue[mine] = "rightclick"

            # If no logical move
            if not self.actionQueue:
                # Generate random coordinates
                coordinates = (randrange(self.sizeX), randrange(self.sizeY))
                # Action is a left click
                actionType = "leftclick"
                # No longer first move
                self.firstMove = False
                # Return actionType and coordinates for first move
                self.actionQueue[coordinates] = actionType


####################################################################################################
    def getAction(self):
        coordinate, actionType = self.actionQueue.popitem()
        print(actionType, coordinate)
        return actionType, coordinate

####################################################################################################
    def surroundingCoordinates(self, xIndex, yIndex):
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
