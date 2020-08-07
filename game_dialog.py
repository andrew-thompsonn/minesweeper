#!/usr/bin/env python3

from engine import Engine
from graphics.lose_dialog import LoseDialog
from graphics.win_dialog import WinDialog

from PyQt5.QtWidgets import QDialog, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QApplication
from PyQt5.QtWidgets import QPushButton, QLineEdit, QFrame,  QLabel, QMenuBar
from PyQt5.QtCore import Qt, QThread, QTimer, QTime, QRunnable
from PyQt5.QtGui import QFont, QIcon

import os
import sys

class GameDialog(QDialog):
####################################################################################################
    def __init__(self, configuration, playerName, newGame = False, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Get overall configuration
        self.config = configuration[0]

        # A list of difficulties for the player and computer
        difficulties = []

        # Initialize player and computer difficulties
        playerDifficulty = None
        computerDifficulty = None
        computerSkill = None

        # If single player
        if self.config == 1:
            # Get player difficulty
            playerDifficulty = configuration[1]
        # If multi player
        if self.config == 2:
            # Get player difficulty
            playerDifficulty = configuration[1]
            # Get computer difficulty
            computerDifficulty = configuration[2]
            # Computer skill
            computerSkill = configuration[3]
        # If single player AI
        if self.config == 3:
            # Get computerDifficulty
            computerDifficulty = configuration[1]

        # Add in player difficulty and computer difficulty to list
        self.difficulties = [playerDifficulty, computerDifficulty]

        #-------------------------------------------------------------------------------------------
        # LAYOUTS
        #-------------------------------------------------------------------------------------------
        # Main layout
        mainLayout = QVBoxLayout(self)
        # ButtonLayout
        buttonLayout = QHBoxLayout()
        # Computer Layout
        computerLayout = QVBoxLayout()
        # Player Layout
        playerLayout = QVBoxLayout()
        # Board layout
        boardLayout = QHBoxLayout()
        # Title Layout
        titleLayout = QVBoxLayout()
        # Player info Layout
        playerInfoLayout = QHBoxLayout()
        # Computer info layout
        compInfoLayout = QHBoxLayout()

        # Game Engine
        self.engine = Engine(self.config, self.difficulties, computerSkill, playerName)

        # Get player board
        playerBoard = self.engine.playerBoard
        # Get computer board
        computerBoard = self.engine.computerBoard

        #-------------------------------------------------------------------------------------------
        # WIDGETS
        #-------------------------------------------------------------------------------------------
        # Title
        titleLabel = QLabel("Sweep Mines")
        titleLabel.setFont(QFont('Ariel', 20))
        titleLabel.setStyleSheet("Color:black;")

        # Start Button for AI
        startButton = QPushButton("Start")
        startButton.setFixedWidth(50)
        startButton.setFixedHeight(30)

        # Flag Icon
        flagCountIcon = QIcon(os.path.join(sys.path[0], "images/flagIcon.png"))

        # Flag count(Player)
        flagCountLabel = QPushButton()
        flagCountLabel.setFixedWidth(30)
        flagCountLabel.setFixedHeight(30)
        flagCountLabel.setIcon(flagCountIcon)
        self.playerFlagCount = QLabel(str(self.engine.playerGameState.mines))

        # Flag count(Computer)
        compFlagCountLabel = QPushButton()
        compFlagCountLabel.setFixedWidth(30)
        compFlagCountLabel.setFixedHeight(30)
        compFlagCountLabel.setIcon(flagCountIcon)
        self.compFlagCount = QLabel(str(self.engine.computerGameState.mines))

        # Initialize second counter
        self.seconds = 0
        # Initialize minute counter
        self.minutes = 0
        # Initialize millisecond counter
        self.milliseconds = 0
        # Timer label
        self.gameTime = QLabel("Time: 0:00")

        # Create a timer
        self.timer = QTimer()
        # Connect timer to AI moves
        self.timer.timeout.connect(self.timerDisplay)
        self.timeString = "0:00"
        if self.config == 1 or self.config == 2:
            # Start timer
            self.timer.start(1000)

        # Save Game button (Singleplayer human only)
        saveButton = QPushButton("Save and Quit")
        saveButton.setFixedWidth(100)
        saveButton.setFixedHeight(30)

        #-------------------------------------------------------------------------------------------
        # LAYOUT MANAGEMENT
        #-------------------------------------------------------------------------------------------
        # Add title to title layout
        titleLayout.addWidget(titleLabel)
        # Add timer to title layout
        titleLayout.addWidget(self.gameTime)
        # Set title alignment
        titleLayout.setAlignment(Qt.AlignCenter)

        # Add player game information
        playerInfoLayout.addWidget(flagCountLabel)
        playerInfoLayout.addWidget(self.playerFlagCount)

        # Add computer computer game information and start
        compInfoLayout.addWidget(compFlagCountLabel)
        compInfoLayout.addWidget(self.compFlagCount)

        # Add player info to player layout
        playerLayout.addLayout(playerInfoLayout)
        # Add player board to player layout
        playerLayout.addLayout(playerBoard)

        # Add computer info to computer layout
        computerLayout.addLayout(compInfoLayout)
        # Add computer board to computer layout
        computerLayout.addLayout(computerBoard)

        # If single-player is selected
        if self.config == 1:
            # Add save button
            playerLayout.addWidget(saveButton)
            # Add player board to board layout
            boardLayout.addLayout(playerLayout)


        # If multi-player is selected
        elif self.config == 2:
            # Add player board to board layout
            boardLayout.addLayout(playerLayout)
            # Add computer board to board layout
            boardLayout.addLayout(computerLayout)
            # Add spacing
            boardLayout.setSpacing(20)

        # If single-player AI selected
        elif self.config == 3:
            # Add computer board to board layout
            boardLayout.addLayout(computerLayout)
            # Add start button for AI
            titleLayout.addWidget(startButton)

        # Add title layout to main
        mainLayout.addLayout(titleLayout)
        # Add button layout to main
        mainLayout.addLayout(buttonLayout)
        # Add board layout to main
        mainLayout.addLayout(boardLayout)

        #-------------------------------------------------------------------------------------------
        # SIGNAL MANAGEMENT
        #-------------------------------------------------------------------------------------------

        # Connect changes in number of flags to handler
        self.engine.playerFlagNumberChanged.connect(self.handlePlayerFlagNumber)
        # Connect changes in number of flags to handler
        self.engine.computerFlagNumberChanged.connect(self.handleComputerFlagNumber)

        # If singleplayer
        if self.config == 1:
            # Connect option to save game
            saveButton.clicked.connect(self.saveGame)
        # If singleplayer AI
        if self.config == 3:
            # Connect the AI to the start button
            startButton.clicked.connect(self.startTime)
            startButton.clicked.connect(self.engine.runAIOnly)
        # If multiplayer
        if self.config == 2:
            # Start the AI when the game begins
            self.engine.runAI(computerSkill)

        # Connect game win signal
        self.engine.winGame.connect(self.winDialog)
        # Connect lose game signal
        self.engine.loseGame.connect(self.loseDialog)

####################################################################################################

    def timerDisplay(self):
        # If either game has ended
        if self.engine.computerGameState.status != 0 or self.engine.playerGameState.status != 0:
            # Stop the timer
            self.timer.stop()
        else:
            # Increment time
            self.seconds += 1

            if self.seconds == 60:
                self.minutes += 1
                self.seconds = 0

            if self.seconds < 10:
                secondsStr = "0"+str(self.seconds)
            else:
                secondsStr = str(self.seconds)

            self.timeString = str(self.minutes)+":"+secondsStr
            # Change timer text
            self.gameTime.setText("Time:    "+self.timeString)

####################################################################################################

    def winDialog(self, info):
        time = info[0]
        name = info[1]
        # If configuration is singleplayer
        if self.config == 1:
            # Send player difficulty
            difficulty = self.difficulties[0]
        # If configuration is singleplayer AI only
        elif self.config == 3:
            # Send compute difficulty
            difficulty = self.difficulties[1]
        # If configuration is multiplayer and computer win
        elif self.config == 2 and name == "computer":
            # Send computer difficulty
            difficulty = self.difficulties[1]
        # If configuration is multiplayer and player win
        else:
            # Send player difficulty
            difficulty = self.difficulties[0]
        # Create a win game dialog
        dialog = WinDialog(name, difficulty, time)
        # Execute the dialog
        response = dialog.exec()
        # Close game dialog
        self.close()

####################################################################################################

    def loseDialog(self, info):
        time = info[0]
        name = info[1]
        # If configuration is singleplayer
        if self.config == 1:
            # Send player difficulty
            difficulty = self.difficulties[0]
        # If configuration is singleplayer AI only
        elif self.config == 3:
            # Send compute difficulty
            difficulty = self.difficulties[1]
        # If configuration is multiplayer and computer win
        elif self.config == 2 and name == "computer":
            # Send computer difficulty
            difficulty = self.difficulties[1]
        # If configuration is multiplayer and player win
        else:
            # Send player difficulty
            difficulty = self.difficulties[0]
        # Dialog box for losing the game
        dialog = LoseDialog(name, difficulty, time)
        # Execute the dialog
        response = dialog.exec()
        # Close the game dialog
        self.close()


####################################################################################################

    def saveGame(self):
        self.engine.setGameTime(self.timeString)
        self.engine.saveGame()

####################################################################################################

    def handlePlayerFlagNumber(self, flags):
        # Change the flag count for the player
        self.playerFlagCount.setText(str(flags))

####################################################################################################

    def handleComputerFlagNumber(self, flags):
        # Change the flag count for the computer
        self.compFlagCount.setText(str(flags))

####################################################################################################

    def startTime(self):

        # Start timer
        self.timer.start(1000)

####################################################################################################
