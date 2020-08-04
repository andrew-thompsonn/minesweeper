#!/usr/bin/env python3

from PyQt5.QtCore import QObject, pyqtSignal, QThread, QTimer
from PyQt5.QtWidgets import QApplication

import time
from random import randrange

from game_state import GameState
from computer_board import ComputerBoard
from player_board import PlayerBoard
from computer_player import ComputerPlayer
from rules import Rules



class Engine(QObject):
    # Signal for computer action
    computerStateChanged = pyqtSignal(GameState)
    # Signal for player action
    playerStateChanged = pyqtSignal(GameState)
    # Signal for game win
    winGame = pyqtSignal(object)
    # Signal for game loss
    loseGame = pyqtSignal(object)
    # Signal for number of flags
    playerFlagNumberChanged = pyqtSignal(int)
    # Signal for number of computer flags
    computerFlagNumberChanged = pyqtSignal(int)
####################################################################################################

    def __init__(self, config, difficulties, computerSkill):
        super().__init__()
        # Initialize Rules
        self.rules = Rules()
        # Get player difficulty
        playerDifficulty = difficulties[0]
        # Get computer difficulty
        computerDifficulty = difficulties[1]
        # Board properties that correspond to difficulty
        boardProperties = [(10, 10, 10), (16, 16, 40), (16, 30, 99)]

        #-------------------------------------------------------------------------------------------
        # PLAYER INITIALIZATION
        #-------------------------------------------------------------------------------------------
        # If no player difficulty
        if playerDifficulty == None:
            # Initialize a player gamestate
            self.playerGameState = GameState(10, 10, 10)
        else:
            # Get correct board size and number of mines according to difficulty
            sizeX = boardProperties[playerDifficulty][0]
            sizeY = boardProperties[playerDifficulty][1]
            mines = boardProperties[playerDifficulty][2]
            # Initialize a player gamestate
            self.playerGameState = GameState(sizeX, sizeY, mines)

        # Initialize a player board
        self.playerBoard = None
        # Enable player board graphics
        self.runGraphics(self.playerBoard, self.playerGameState, "human")

        #-------------------------------------------------------------------------------------------
        # COMPUTER INITIALIZATION
        #-------------------------------------------------------------------------------------------
        # If no player difficulty
        if computerDifficulty == None:
            # Initialize a computer gameState
            self.computerGameState = GameState(10, 10, 10)
        else:
            # Get correct board size and number of mines according to difficulty
            sizeX = boardProperties[computerDifficulty][0]
            sizeY = boardProperties[computerDifficulty][1]
            mines = boardProperties[computerDifficulty][2]
            # Initialize a computer gameState
            self.computerGameState = GameState(sizeX, sizeY, mines)

        # Initialize a computer player
        self.computerPlayer = ComputerPlayer("easy", self.computerGameState)
        # Initialize a computer board
        self.computerBoard = None
        # Enable computer board graphics
        self.runGraphics(self.computerBoard, self.computerGameState, "computer")
        # Initialize computer rightclick queue
        self.rightClickQueue = []
        # Initialize computer left click queue
        self.leftClickQueue = []

####################################################################################################
    #           Easy              Medium
    # Times: 0.610 seconds    20.11 seconds

    def getAIMove(self):
        # If the computer's game or the player's game is over
        if self.computerGameState.status != 0 or self.playerGameState.status != 0:
            # Stop the timer
            self.timer.stop()
            # Return nothing
            return None

        # If queue for mines is empty
        if not self.rightClickQueue and not self.leftClickQueue:
            # Try to get more moves for mines
            mines = self.computerPlayer.getMines(self.computerGameState)
            # Try to get more moves for safe bricks
            safes = self.computerPlayer.getSafeBricks(self.computerGameState)
            # If still no moves
            if not mines and not safes:
                # Get a random move
                randomCoord = self.computerPlayer.first()
                # Add the random move to the left click Queue
                self.leftClickQueue.append(randomCoord)
            # If new moves were found
            else:
                # Fill the right click queue with the new moves
                self.rightClickQueue = self.rightClickQueue + mines
                # Fill the left click queue with the new moves
                self.leftClickQueue = self.leftClickQueue + safes

        # If there are more right click moves in the queue
        elif len(self.rightClickQueue) > len(self.leftClickQueue):
            # Get action from the right click queue
            rClickCoord = self.rightClickQueue.pop(0)
            # Commit right click
            self.commitComputerAction("rightclick", rClickCoord, self.computerGameState)
        # If there are more left click moves in the queue
        elif len(self.rightClickQueue) <= len(self.leftClickQueue) and len(self.leftClickQueue)!= 0:
            # Get action from the left click queue
            lClickCoord = self.leftClickQueue.pop(0)
            # Commit left click
            self.commitComputerAction("leftclick", lClickCoord, self.computerGameState)

####################################################################################################

    def runAI(self):
        # Create a timer
        self.timer = QTimer()
        # Connect timer to AI moves
        self.timer.timeout.connect(self.getAIMove)
        # Start timer
        self.timer.start(1000)

####################################################################################################

    def runAIOnly(self):
        computer = self.computerPlayer
        # Get first move
        coordinates = computer.first()
        # Commit first move
        self.commitComputerAction("leftclick", coordinates, self.computerGameState)

        # While game is active
        while self.computerGameState.status == 0:
            # Get list of mines
            mines = computer.getMines(self.computerGameState)
            # For all confirmed mines
            for mine in mines:
                # Handle events
                QApplication.processEvents()
                # Commit action
                self.commitComputerAction("rightclick", mine, self.computerGameState)
            # Get list of safe bricks
            safeBricks = computer.getSafeBricks(self.computerGameState)
            # For all safe bricks
            for brick in safeBricks:
                # Handle events
                QApplication.processEvents()
                # Commit action
                self.commitComputerAction("leftclick", brick, self.computerGameState)
            # If no logical moves
            if not safeBricks and not mines:
                # Get random move
                coordinates = computer.first()
                # Commit commit random move
                self.commitComputerAction("leftclick", coordinates, self.computerGameState)

####################################################################################################

    def commitComputerAction(self, type, coordinate, gameState):
        # Get brick at coordinates
        brick = gameState.bricks[coordinate]
        # If action is a left click
        if type == "leftclick":
            # Check rules
            if self.rules.check(type, brick):
                # If brick is not a mine and not touching any mines
                if brick.touching == 0 and brick.mine == False:
                    # Reveal all empty squares in surrounding area
                    gameState.clickMany(coordinate)
                # Otherwise click single brick
                else: gameState.clickBrick(coordinate)
        # If action is a right click
        if type == "rightclick":
            # Check rules
            if self.rules.check(type, brick):
                # Flag square
                gameState.flagBrick(coordinate)
                # Emit computer flag number changed
                self.computerFlagNumberChanged.emit(self.computerGameState.flags)

        # Emit signal to update computer board
        self.computerStateChanged.emit(self.computerGameState)

        # If game is won
        if gameState.status == 1:
            # Emit win signal
            self.winGame.emit("computer")
        # If game is lost
        elif gameState.status == 2:
            # Emit lose signal
            self.loseGame.emit(["computer", coordinate])

####################################################################################################

    def commitPlayerClick(self, coordinates):
        # Get brick
        brick = self.playerGameState.bricks[coordinates]
        # If brick is not a mine and not touching any mines
        if brick.touching == 0 and brick.mine == False:
            # Reveal all empty squares in surrounding area
            self.playerGameState.clickMany(coordinates)
        # Otherwise reveal single bricks
        else: self.playerGameState.clickBrick(coordinates)
        # Emit signal that players board needs to change
        self.playerStateChanged.emit(self.playerGameState)

        # if game is won
        if self.playerGameState.status == 1:
            # Emit win signal
            self.winGame.emit("player")
        # If game is lost
        elif self.playerGameState.status == 2:
            # Emit lose signal
            self.loseGame.emit(coordinates)

####################################################################################################

    def commitPlayerFlag(self, coordinates):
        # Get the brick that was clicked
        brick = self.playerGameState.bricks[coordinates]
        # Flag the brick
        self.playerGameState.flagBrick(coordinates)
        # Emit signal for flags changed
        self.playerFlagNumberChanged.emit(self.playerGameState.flags)
        # Emit signal that players board needs to change
        self.playerStateChanged.emit(self.playerGameState)

        # If game is won
        if self.playerGameState.status == 1:
            # Emit win signal
            self.winGame.emit("player")

####################################################################################################

    def runGraphics(self, board, gameState, playerType):
        # If computer player
        if playerType == "computer":
            # Initialize computer board
            self.computerBoard = ComputerBoard(gameState, playerType)
        # If human player
        elif playerType == "human":
            print("Initializing player graphics")
            # Initialize human board
            self.playerBoard = PlayerBoard(gameState, playerType)
            # Connect left click signal
            self.playerBoard.buttonLeftClick.connect(self.commitPlayerClick)
            # Connect right click signal
            self.playerBoard.buttonRightClick.connect(self.commitPlayerFlag)

####################################################################################################
