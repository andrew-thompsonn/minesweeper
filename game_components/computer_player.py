#!/usr/bin/env python3

from game_components.player import Player
from random import randrange

import time

class ComputerPlayer(Player):
    """ A class to represent the computer player and the actions the computer wants to commit based
        on the current gamestate """

####################################################################################################
    def __init__(self, skill, gameState, *args, **kwargs):
        """ Get correct computer name based on the skill of the computer, set skill, initialize
            variables, and document the current gamestate

            Inputs:     skill <int>
                        gameState <GameState>
        """
        name = self.getName(skill)
        super().__init__(name, False)
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
        # Bricks that don't reveal any information
        self.questionBricks = set()

####################################################################################################

    def getName(self, skill):
        """ Get the name of the computer

            Inputs:     skill <int>
            Outputs:    name <string>
        """
        # Dictionary of computer skills corresponding to names
        names = {0:'Computer_1', 1:'Computer_2', 2:'Computer_3', 3:'Computer', 69:None}
        # Get name
        name = names[skill]
        # Return name
        return name

####################################################################################################

    def seeBoard(self, gameState):
        """ Get information about the gameState that the computer requires to make decisions.

            Inputs:     gameState <GameState>
            Outputs:    visibleBricks [(<int>, <int>)]
        """
        # Get visible bricks
        visibleBricks = gameState.visibleBricks
        self.visibleBricks = gameState.visibleBricks
        # Return all bricks, and visible bricks
        return visibleBricks, gameState.bricks

####################################################################################################

    def first(self):
        """ Get a random coordinate to click. Always called on the computer's first move. Only
            chooses coordinates that are not visible.

            Inputs:     None
            Outputs:    Coordinates (<int>, <int>)
        """
        # Get information from gamestate
        visibleBricks, allBricks = self.seeBoard(self.gameState)
        # Initialize list of invisible bricks
        invisible = []
        # For every brick
        for coord in allBricks:
            # If brick is invisible
            if not allBricks[coord].visible:
                # Append coordinates of invisible brick to list
                invisible.append(coord)
        # Pick a random coordinate from the invisible brick list
        coordinates = invisible[randrange(len(invisible))]
        # Set first move to false
        self.firstMove = False
        # Return the coordinates of the first move
        return coordinates

####################################################################################################

    def getMines(self, gameState):
        """ Get a list of bricks that have to be mines.

            Inputs:     gameState
            Outputs:    mines [(<int>, <int>)]
        """
        # Get list of visible bricks
        visibleBricks, allBricks = self.seeBoard(gameState)
        # Initialize a list of confirmed mines
        mines = []
        # For all visible bricks
        for brick in visibleBricks:
            # If the brick is touching mines
            if brick.touching > 0:
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
                    if brick in self.questionBricks:
                        self.questionBricks.remove(brick)
                else:
                    self.questionBricks.add(brick)

        # Return a list of mines
        return mines

####################################################################################################

    def getSafeBricks(self, gameState):
        """ Get list of bricks that cannot be mines.

            Inputs:     gameState <GameState>
            Outputs:    clearBricks [(<int>, <int>)]
        """
        # Get list of visible bricks
        visibleBricks, allBricks = self.seeBoard(gameState)
        # A list of confirmed safe bricks
        clearBricks = []
        # For every visible brick
        for brick in visibleBricks:
            # If the brick is touching mines
            if brick.touching > 0:
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
                    if brick in self.questionBricks:
                        self.questionBricks.remove(brick)
                else:
                    self.questionBricks.add(brick)
        # Return safe bricks
        return clearBricks

####################################################################################################

    def probability(self, gameState):
        """ Calculate the probability of all unclicked bricks as being mines. Only calculates for
            bricks that are touching visible numbers

            Currently the computer's probabilistic guesses are correct 80.7% of the time
            This function is not optimized, and the calculated probabilities have an uncertainty
            of +/- 7%.

            Inputs:     gameState <GameState>
            Outputs:    coordinates (<int>, <int>)
                        probability <int>
        """
        #-------------------------------------------------------------------------------------------
        # Initialization
        #-------------------------------------------------------------------------------------------
        # Dictionary containing a question brick as the key, and mine candidates for that
        # Question brick as the value
        brickCandidates = {}
        # Dictionary containing coordinates and probability of mine
        mineProbabilities = {}
        # Get list of visible bricks
        visibleBricks, allBricks = self.seeBoard(gameState)

        #-------------------------------------------------------------------------------------------
        # Get mine candidates
        #-------------------------------------------------------------------------------------------
        # For brick that reveals no info
        for brick in self.questionBricks:
            # Get all surrounding coordinates
            checklist = self.getNearCoordinates(brick.coordinates[0], brick.coordinates[1])
            # Initialize a list for mine candidates
            mineCandidates = []

            # For all coordinates surrounding brick
            for coordinate in checklist:
                # If the brick at the coordinite is not visible
                if not allBricks[coordinate].visible and not allBricks[coordinate].flag:
                    # Append to mine candidates
                    mineCandidates.append(coordinate)

            # Fill dictionary for current brick with all the mine candidates it is touching
            brickCandidates[brick] = mineCandidates

            #---------------------------------------------------------------------------------------
            # Get probability based on current brick
            #---------------------------------------------------------------------------------------
            # Number of invisible bricks our current brick is touching
            touchingBricks = len(mineCandidates)
            # Get number of flags the brick is touching
            flagCount = self.countFlags(brick.coordinates)
            # Probability of mine is (mines touching / bricks touching)
            mineProbability = (brick.touching - flagCount)/touchingBricks

            #---------------------------------------------------------------------------------------
            # Deal with multiple bricks touching the same mine candidate
            #---------------------------------------------------------------------------------------
            # List containing duplicate mine candidates
            mineMultiples = []
            # For every coordinate in mine candidates
            for candidate in mineCandidates:
                # If the candidate is already in the dictionary
                if candidate in mineProbabilities:
                    # Add it to the list of multiples
                    mineMultiples.append(candidate)
                    # Count the number of times it has appeared
                    occurences = mineMultiples.count(candidate)
                    # Calculate the weighted probability
                    combinedProbability = (((occurences)*mineProbabilities[candidate])+mineProbability)/2
                    # Add weighted probability to dictionary
                    mineProbabilities[candidate] = combinedProbability
                else:
                    # Add to dictionary
                    mineProbabilities[candidate] = mineProbability

            #---------------------------------------------------------------------------------------
            # Change probabilities of candidates that are effected by more than one brick
            #---------------------------------------------------------------------------------------
            # Initialize a list of probabilities
            probList = []
            # For coordinates in the brick's candidate mine list
            for coordinates in brickCandidates[brick]:
                # Append the probability
                probList.append(mineProbabilities[coordinates])
            # Get the difference between what the probability sum should be and the value
            delta = allBricks[candidate].touching - sum(probList)
            # If the difference is greater than 1/10
            if delta > 0.1:
                # Get the minimum probability in the list
                minimum = min(probList)
                # Initialize a list of probabilities that need to change
                incorrectProbs = []
                # For coordinates in the brick's candidate mine list
                for candidateCoords in brickCandidates[brick]:
                    # If probability is not the minimum
                    if mineProbabilities[candidateCoords] != minimum:
                        # Add the coordinates to the list
                        incorrectProbs.append(candidateCoords)
                # The correct sum for incorrect probabilities
                correctBrickProbSum = (len(brickCandidates[brick]) - len(incorrectProbs)) * minimum
                # The desired sum
                desiredSum = allBricks[candidate].touching - correctBrickProbSum
                # Determine a scaling factor
                scaleFactor = desiredSum / correctBrickProbSum
                # For all bricks that need probability to be scaled
                for candidateCoords in incorrectProbs:
                    # Check to make sure probability is too low
                    if mineProbabilities[candidateCoords] in incorrectProbs:
                        # Scale the probability by the scale factor
                        mineProbabilities[candidate] *= scaleFactor

        #---------------------------------------------------------------------------------------
        # Get the minimum probability to return
        #---------------------------------------------------------------------------------------
        try:
            # Get the minimum probability
            minValue = min(mineProbabilities.values())
            # Get list of bricks with minimum probability (could be multiple)
            minKeys = [k for k, v in mineProbabilities.items() if v == minValue]
            # Return the coordinates and probability
            return minKeys[0], minValue
        # If no minumum value
        except ValueError as error:
            # Get a random move
            coordinates = self.first()
            # Random probability
            probability = "RANDOM"
            # Return coordinates and probability
            return coordinates, probability

####################################################################################################

    def countFlags(self, coordinates):
        """ Count the number of flags a brick is touching.

            Inputs:     coordinates (<int>, <int>)
            Outputs:    flagCount <int>
        """
        # Get surrounding cordinates
        checklist = self.getNearCoordinates(coordinates[0], coordinates[1])
        # Initialize a flag count
        flagCount = 0
        # For every surrounding coordinate
        for coord in checklist:
            # If the brick at the coordinate is flagged
            if self.gameState.bricks[coord].flag:
                # Increment the flag count
                flagCount += 1
        # Return the flag count
        return flagCount

####################################################################################################

    def getNearCoordinates(self, xIndex, yIndex):
        """ Get all surrounding coordinates of an x and y coordinate.

            Inputs:     xIndex <int>
                        yIndex <int>
            Outputs:    checklist [(<int>, <int>)]
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
