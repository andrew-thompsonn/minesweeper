#!/usr/bin/env python3

from engine import Engine
from Dialogs.lose_dialog import LoseDialog
from Dialogs.win_dialog import WinDialog

from PyQt5.QtWidgets import QDialog, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QApplication
from PyQt5.QtWidgets import QPushButton, QLineEdit, QFrame,  QLabel
from PyQt5.QtCore import Qt, QThread, QTimer, QTime
from PyQt5.QtGui import QFont, QIcon

import os
import sys

class GameDialog(QDialog):
####################################################################################################
    def __init__(self, configuration, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Get overall configuration
        config = configuration[0]

        # A list of difficulties for the player and computer
        difficulties = []

        # Initialize player and computer difficulties
        playerDifficulty = None
        computerDifficulty = None
        computerSkill = None

        # If single player
        if config == 1:
            # Get player difficulty
            playerDifficulty = configuration[1]
        # If multi player
        if config == 2:
            # Get player difficulty
            playerDifficulty = configuration[1]
            # Get computer difficulty
            computerDifficulty = configuration[2]
            # Computer skill
            computerSkill = configuration[3]
        # If single player AI
        if config == 3:
            # Get computerDifficulty
            computerDifficulty = configuration[1]

        # Add in player difficulty and computer difficulty to list
        difficulties = [playerDifficulty, computerDifficulty]

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
        self.engine = Engine(config, difficulties, computerSkill)

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


        # Initialize a count
        self.seconds = 0
        self.minutes = 0
        # Timer label
        self.gameTime = QLabel("Time: 0:00")

        # Create a timer
        self.timer = QTimer()
        # Connect timer to AI moves
        self.timer.timeout.connect(self.timerDisplay)



        #-------------------------------------------------------------------------------------------
        # LAYOUT MANAGEMENT
        #-------------------------------------------------------------------------------------------
        # Add title to title layout
        titleLayout.addWidget(titleLabel)
        # Add timer to title layout
        titleLayout.addWidget(self.gameTime)
        # Set title alignment
        titleLayout.setAlignment(Qt.AlignCenter)

        # Add player info to info layout
        playerInfoLayout.addWidget(flagCountLabel)
        playerInfoLayout.addWidget(self.playerFlagCount)

        # Add computer info to info layout
        compInfoLayout.addWidget(compFlagCountLabel)
        compInfoLayout.addWidget(self.compFlagCount)
        compInfoLayout.addWidget(startButton)

        # Add player info to player layout
        playerLayout.addLayout(playerInfoLayout)
        # Add player board to player layout
        playerLayout.addLayout(playerBoard)

        # Add computer info to computer layout
        computerLayout.addLayout(compInfoLayout)
        # Add computer board to computer layout
        computerLayout.addLayout(computerBoard)


        # If single-player is selected
        if config == 1:
            # Add player board to board layout
            boardLayout.addLayout(playerLayout)

        # If multi-player is selected
        elif config == 2:
            # Add player board to board layout
            boardLayout.addLayout(playerLayout)
            # Add computer board to board layout
            boardLayout.addLayout(computerLayout)
            # Add spacing
            boardLayout.setSpacing(20)

        # If single-player AI selected
        elif config == 3:
            # Add computer board to board layout
            boardLayout.addLayout(computerLayout)
            # Add start button to button layout
            buttonLayout.addWidget(startButton)

        # Add title layout to main
        mainLayout.addLayout(titleLayout)
        # Add button layout to main
        mainLayout.addLayout(buttonLayout)
        # Add board layout to main
        mainLayout.addLayout(boardLayout)

        #-------------------------------------------------------------------------------------------
        # SIGNAL MANAGEMENT
        #-------------------------------------------------------------------------------------------

        # Connect changes in player game to player board
        self.engine.playerStateChanged.connect(playerBoard.changeBoard)
        # Connect changes in number of flags to handler
        self.engine.playerFlagNumberChanged.connect(self.handlePlayerFlagNumber)

        # Connect changes in computer game to computer board
        self.engine.computerStateChanged.connect(computerBoard.changeBoard)
        # Connect changes in number of flags to handler
        self.engine.computerFlagNumberChanged.connect(self.handleComputerFlagNumber)

        if config == 3:
            startButton.clicked.connect(self.engine.runAIOnly)
            startButton.clicked.connect(self.startTime)
        else:
            # Connect start button to initiate AI
            startButton.clicked.connect(self.engine.runAI)
            # Start timer
            self.timer.start(1000)


        # Connect game win signal
        self.engine.winGame.connect(self.winDialog)
        # Connect lose game signal
        self.engine.loseGame.connect(self.loseDialog)

####################################################################################################

    def timerDisplay(self):
        print("Updating time")
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

            # Change timer text
            self.gameTime.setText("Time: "+str(self.minutes)+":"+secondsStr)

####################################################################################################

    def winDialog(self, name):
        # Dialog box for winning the game
        dialog = WinDialog(name)
        response = dialog.exec()
        self.accept()

####################################################################################################

    def loseDialog(self, name):
        # Dialog box for losing the game
        dialog = LoseDialog(name)
        response = dialog.exec()
        self.accept()

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
        print("Starting timer")

        # Start timer
        self.timer.start(1000)

####################################################################################################
