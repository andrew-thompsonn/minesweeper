#!/usr/bin/env python3

from PyQt5.QtCore import QObject, pyqtSignal, QThread
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
####################################################################################################

    def __init__(self, config):
        super().__init__()
        # Initialize Rules
        self.rules = Rules()

        # Initialize a computer gameState
        self.computerGameState = GameState(16, 16, 40)
        # Initialize a computer board
        self.computerBoard = None
        # Enable computer board graphics
        self.runGraphics(self.computerBoard, self.computerGameState, "computer")

        # Initialize a player gamestate
        self.playerGameState = GameState(10, 10, 10)
        # Initialize a player board
        self.playerBoard = None
        # Enable player board graphics
        self.runGraphics(self.playerBoard, self.playerGameState, "human")


####################################################################################################

    def runAI(self):
        # Initialize computer player
        computer = ComputerPlayer("easy", self.computerGameState)
        # Get first move
        coordinates = computer.first()
        # Commit first move
        self.commitComputerAction("leftclick", coordinates, self.computerGameState)
        #Emit signal to update computer board
        self.computerStateChanged.emit(self.computerGameState)

        while self.computerGameState.status == 0:
            # Get locations of mines
            QApplication.processEvents()
            mines = computer.getMines(self.computerGameState)
            print(mines)

            for mine in mines:
                # Handle events
                QApplication.processEvents()
                # Wait
                #QThread.msleep(500)
                # Commit action
                self.commitComputerAction("rightclick", mine, self.computerGameState)
                # Emit signal to update computer board
                self.computerStateChanged.emit(self.computerGameState)

            # Get locations of safe bricks
            safeBricks = computer.getSafeBricks(self.computerGameState)
            print(safeBricks)

            for brick in safeBricks:
                # Handle events
                QApplication.processEvents()
                # Wait
                #QThread.msleep(500)
                # Commit action
                self.commitComputerAction("leftclick", brick, self.computerGameState)
                # Emit signal to update computer board
                self.computerStateChanged.emit(self.computerGameState)

            if not safeBricks and not mines:
                # Get random move
                coordinates = computer.first()
                # Commit commit random move
                self.commitComputerAction("leftclick", coordinates, self.computerGameState)
                #Emit signal to update computer board
                self.computerStateChanged.emit(self.computerGameState)

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

        if gameState.status == 1:
            self.computerStateChanged.emit(self.computerGameState)
            self.winGame.emit("computer")
        elif gameState.status == 2:
            self.computerStateChanged.emit(self.computerGameState)
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
