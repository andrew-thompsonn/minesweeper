#!/usr/bin/env python3

from PyQt5.QtWidgets import QMainWindow, QStackedWidget, QWidget
from PyQt5.QtGui import  QImage, QPalette, QBrush, QIcon,  QMovie, QPainter, QPixmap
from PyQt5.QtCore import QSize

import sys
import os

from game_dialog import GameDialog
from graphics.multi_player_options import MultiPlayerOptions
from graphics.single_player_options import SinglePlayerOptions
from graphics.start_screen import StartScreen
from graphics.watch_options import WatchOptions
from graphics.load_game_options import LoadGameOptions

class MainWindow(QMainWindow):
    """ Class for the main window of the application. """
####################################################################################################
    def __init__(self, *args, **kwargs):
        """ Initialize a main window for the minesweeper application. Contains buttons connected
            to load game options, singleplayer options, multiplayer options, and watch options.

            Inputs:     None
            Outputs:    None
        """
        super().__init__(*args, *kwargs)

        #-------------------------------------------------------------------------------------------
        # MENU BAR
        #-------------------------------------------------------------------------------------------
        # Add a menu bar
        menuBar = self.menuBar()
        # Make it sexy
        menuBar.setStyleSheet("background:rgba(100, 100, 125, 0.7);")

        # File menu
        fileMenu = menuBar.addMenu("File")
        # File/Load
        loadAction = fileMenu.addAction("Load")
        # Connect load to load dialog
        loadAction.triggered.connect(self.loadGameOptions)
        # File/Quit
        quitAction = fileMenu.addAction("Quit")
        # Connect quit to quit app
        quitAction.triggered.connect(lambda: self.quit(0))
        # Standard shortcut
        quitAction.setShortcut("CTRL+Q")

        # Edit menu
        editMenu = menuBar.addMenu("Edit")
        # Edit/preferences - will be able to change color theme
        prefAction = editMenu.addMenu("Preferences")
        # This will do something eventually

        #-------------------------------------------------------------------------------------------
        # INIT
        #-------------------------------------------------------------------------------------------
        # Start screen
        startScreen = StartScreen()
        # Set geometry
        self.setFixedSize(600, 338)

        # Create moving background
        self.movie = QMovie("graphics/images/movingMines.gif")
        # Connect changes in background to repaint
        self.movie.frameChanged.connect(self.repaint)
        # Start the movie
        self.movie.start()

        # Window title
        self.setWindowTitle("Minesweeper")
        # Central widget is the start screen
        self.setCentralWidget(startScreen)

        # Set a default player name
        self.playerName = ""

        # Connect multiplayer button to multiplayer options
        startScreen.singlePlayerPressed.connect(self.singlePlayerOptions)
        # Connect single player button to single player options
        startScreen.multiPlayerPressed.connect(self.multiPlayerOptions)
        # Connect Watch button to AI options
        startScreen.watchButtonPressed.connect(self.watchOptions)

####################################################################################################

    def watchOptions(self):
        """ Displays the options for watching the AI playe minesweeper and stores the user's desired
            configuration

            Inputs:     None
            Outputs:    None
        """
        # Watch options dialog
        watchDialog = WatchOptions()
        # Connect submission to to configuration
        watchDialog.configuration.connect(self.setConfiguration)
        # Execute the dialog box
        watchDialog.exec()

####################################################################################################

    def singlePlayerOptions(self):
        """ Displays the options for singleplayer minesweeper gameplay and stores the users desired
            configuration

            Inputs:     None
            Outputs:    None
        """
        # Single player option dialog
        singleDialog = SinglePlayerOptions()
        # Get player name
        singleDialog.nameSignal.connect(self.setName)
        # Connect submission of single player options to configuration
        singleDialog.configuration.connect(self.setConfiguration)
        # Execute the dialog box
        singleDialog.exec()

####################################################################################################

    def multiPlayerOptions(self):
        """ Displays the options for multiplayer minesweeper gameplay and stores the users desired
            configuration

            Inputs:     None
            Outputs:    None
        """
        # Multi player option dialog
        multiDialog = MultiPlayerOptions()
        # Get Player name
        multiDialog.nameSignal.connect(self.setName)
        # Connect Submission of multi player options to configuration
        multiDialog.configuration.connect(self.setConfiguration)
        # Execute the dialog box
        multiDialog.exec()

####################################################################################################

    def loadGameOptions(self):
        """ Displays the options for loading a previously save game.

            Inputs:     None
            Outputs:    None
        """
        # Load game options dialog
        loadDialog = LoadGameOptions()
        # Get player name
        loadDialog.nameSignal.connect(self.setName)
        # Connect submission of load game to configuration
        loadDialog.configuration.connect(self.setConfiguration)
        # Execute dialog box
        loadDialog.exec()

####################################################################################################

    def setConfiguration(self, configuration):
        """ Sets the MainWindow configuration variable and executes a dialog based off the selected
            configuration

            Inputs:     configuration <list>
            Outputs:    None
        """
        # Get the window that sent the signal
        sender = self.sender()
        # Close the window that sent the signal
        sender.close()
        # Create a game
        game = GameDialog(configuration, self.playerName)
        # Execute the game
        game.exec()

####################################################################################################

    def setName(self, name):
        """ Sets the mainWindow player name variable

            Inputs:     name <string>
            Outputs:    None
        """
        # Set player name
        self.playerName = name

####################################################################################################

    def quit(self, returnCode):
        """ A shortcut function used to quit the application

            Inputs:     None
            Outputs:    None
        """
        exit(returnCode)

####################################################################################################

    def paintEvent(self, event):
        """ Function to allow for continuous background animation

            Inputs:     event <event>
            Outputs:    None
        """
        # Get current fram
        currentFrame = self.movie.currentPixmap()
        # Current frame rectangle
        frameRect = currentFrame.rect()
        # Current frame center
        frameRect.moveCenter(self.rect().center())
        # If frame has changed
        if frameRect.intersects(event.rect()):
            # Create a painter
            painter = QPainter(self)
            # Redraw background
            painter.drawPixmap(frameRect.left(), frameRect.top(), currentFrame)

####################################################################################################
