#!/usr/bin/env python3

# Current:# 891 Lines of code

from engine import Engine
from win_dialog import WinDialog
from lose_dialog import LoseDialog

import time

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QApplication
from PyQt5.QtWidgets import QPushButton, QLineEdit, QFrame,  QLabel
from PyQt5.QtCore import Qt, QThread
from PyQt5.QtGui import QFont, QIcon

import os
import sys

class CentralWidget(QWidget):
####################################################################################################
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        config = 3

        #-------------------------------------------------------------------------------------------
        # LAYOUTS
        #-------------------------------------------------------------------------------------------
        # Main layout
        mainLayout = QVBoxLayout(self)
        # ButtonLayout
        buttonLayout = QHBoxLayout()
        # Board layout
        boardLayout = QHBoxLayout()
        # Title Layout
        titleLayout = QHBoxLayout()
        # Info Layout
        infoLayout = QHBoxLayout()

        # Game Engine
        self.engine = Engine(config)

        # If single-player selected
        if config == 1:
            # Get player board
            playerBoard = self.engine.playerBoard

        # If multi-player selected
        elif config == 2:
            # Get computer board
            computerBoard = self.engine.computerBoard
            # Get player board
            playerBoard = self.engine.playerBoard

        # If single-player AI selected
        elif config == 3:
            # Get computer board
            computerBoard = self.engine.computerBoard

        #-------------------------------------------------------------------------------------------
        # WIDGETS
        #-------------------------------------------------------------------------------------------
        # Title
        titleLabel = QLabel("Sweep the Mines Bitch")
        titleLabel.setFont(QFont('Ariel', 20))
        titleLabel.setStyleSheet("Color:black;")

        # Start Button for AI
        startButton = QPushButton("Start AI ")
        startButton.setFixedWidth(50)
        startButton.setFixedHeight(30)

        # Flag count icon
        flagCountIcon = QIcon(os.path.join(sys.path[0], "images/flagIcon.png"))
        flagCountLabel = QPushButton()
        flagCountLabel.setFixedWidth(20)
        flagCountLabel.setFixedHeight(20)
        flagCountLabel.setIcon(flagCountIcon)
        flagCount = QLabel(str(self.engine.playerGameState.mines))

        #-------------------------------------------------------------------------------------------
        # LAYOUT MANAGEMENT
        #-------------------------------------------------------------------------------------------
        # If single-player is selected
        if config == 1:
            # Add player board to board layout
            boardLayout.addLayout(playerBoard)

        # If multi-player is selected
        elif config == 2:
            # Add player board to board layout
            boardLayout.addLayout(playerBoard)
            # Add computer board to board layout
            boardLayout.addLayout(computerBoard)
            # Add start button to button layout
            buttonLayout.addWidget(startButton)

        # If single-player AI selected
        elif config == 3:
            # Add computer board to board layout
            boardLayout.addLayout(computerBoard)
            # Add start button to button layout
            buttonLayout.addWidget(startButton)

        # Add title to title layout
        titleLayout.addWidget(titleLabel)
        titleLayout.setAlignment(Qt.AlignCenter)

        # Add info to info layout
        infoLayout.addWidget(flagCountLabel)
        infoLayout.addWidget(flagCount)

        # Add title layout to main
        mainLayout.addLayout(titleLayout)
        # Add info layout to main
        mainLayout.addLayout(infoLayout)
        # Add button layout to main
        mainLayout.addLayout(buttonLayout)
        # Add board layout to main
        mainLayout.addLayout(boardLayout)

        #-------------------------------------------------------------------------------------------
        # SIGNAL MANAGEMENT
        #-------------------------------------------------------------------------------------------
        if config == 1:
            # Connect changes in player game to player board
            self.engine.playerStateChanged.connect(playerBoard.changeBoard)

        elif config == 2:
            # Connect changes in player game to player board
            self.engine.playerStateChanged.connect(playerBoard.changeBoard)
            # Connect changes in computer game to computer board
            self.engine.computerStateChanged.connect(computerBoard.changeBoard)
            # Connect start button to initiate AI
            startButton.clicked.connect(self.engine.runAI)

        elif config == 3:
            # Connect changes in computer game to computer board
            self.engine.computerStateChanged.connect(computerBoard.changeBoard)
            # Connect start button to initiate AI
            startButton.clicked.connect(self.engine.runAI)

        # Connect game win signal
        self.engine.winGame.connect(self.winDialog)
        # Connect lose game signal
        self.engine.loseGame.connect(self.loseDialog)

####################################################################################################

    def winDialog(self, name):
        dialog = WinDialog(name)
        response = dialog.exec()

####################################################################################################

    def loseDialog(self, name):
        dialog = LoseDialog(name)
        response = dialog.exec()

####################################################################################################
