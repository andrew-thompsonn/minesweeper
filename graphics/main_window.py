#!/usr/bin/env python3

from PyQt5.QtWidgets import QMainWindow, QStackedWidget, QWidget, QMessageBox
from PyQt5.QtGui import  QImage, QPalette, QBrush, QIcon,  QMovie, QPainter, QPixmap, QDesktopServices
from PyQt5.QtCore import QSize, QUrl

import sys
import os

# Graphics
from graphics.game_dialog import GameDialog
from graphics.multi_player_options import MultiPlayerOptions
from graphics.single_player_options import SinglePlayerOptions
from graphics.start_screen import StartScreen
from graphics.watch_options import WatchOptions
from graphics.load_game_options import LoadGameOptions

# Database
from web.postgreSQL.psql_database import PsqlDatabase, PsqlDatabaseError

####################################################################################################

class MainWindow(QMainWindow):
    """ Class for the main window of the application. """

    # Link to home page of website
    """  http://0.0.0.0:8080/  """

####################################################################################################
    def __init__(self, *args, **kwargs):
        """ Initialize a main window for the minesweeper application. Contains buttons connected
            to load game options, singleplayer options, multiplayer options, and watch options.

            Inputs:     None
            Outputs:    None
        """
        # Initialize parent class
        super().__init__(*args, *kwargs)

        # Create instance of database
        self.__database = PsqlDatabase()
        # Try to connect to the database
        try:
            # Connect to database
            self.__database.connectToDatabase()
        # Except a database error
        except PsqlDatabaseError as error:
            # String referencing README
            refString="\nRefer to README.txt section titled\n\"INSTALLING DOCKER AND INITIALIZING DATABASE\""
            # Critical error dialog
            criticalErrorDialog = QMessageBox.critical(self,'Database Error',str(error)+refString, QMessageBox.Ok)
            # Exit the application
            self.quit(1)

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

        # Theme menu
        aboutMenu = menuBar.addMenu("About")
        # Edit/preferences - will be able to change color theme
        aboutAction = aboutMenu.addAction("About")
        # This will do something eventually
        aboutAction.triggered.connect(self.openWeb)

        #-------------------------------------------------------------------------------------------
        # INITIALIZATION
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
        # Execute the dialog box
        response = watchDialog.exec()
        # If dialog was accepted
        if response == watchDialog.Accepted:
            # Set configuration
            configuration = watchDialog.getConfiguration()
            # Create a game with the configuration
            self.createGame(configuration)

####################################################################################################

    def singlePlayerOptions(self):
        """ Displays the options for singleplayer minesweeper gameplay and stores the users desired
            configuration

            Inputs:     None
            Outputs:    None
        """
        # Single player option dialog
        singleDialog = SinglePlayerOptions(self.__database)
        # Execute the dialog and get a response
        response = singleDialog.exec()
        # If the dialog was accepted
        if response == singleDialog.Accepted:
            # Set the player name
            self.playerName = singleDialog.getName()
            # Set the configuration
            configuration = singleDialog.getConfiguration()
            # Create a game with the configuration
            self.createGame(configuration)

####################################################################################################

    def multiPlayerOptions(self):
        """ Displays the options for multiplayer minesweeper gameplay and stores the users desired
            configuration

            Inputs:     None
            Outputs:    None
        """
        # Multi player option dialog
        multiDialog = MultiPlayerOptions(self.__database)
        # Execute dialog and get a response
        response = multiDialog.exec()
        # If the dialog was accepted
        if response == multiDialog.Accepted:
            # Set the player name
            self.playerName = multiDialog.getName()
            # Set the configuration
            configuration = multiDialog.getConfiguration()
            # Create a game with the configuration
            self.createGame(configuration)

####################################################################################################

    def loadGameOptions(self):
        """ Displays the options for loading a previously save game.

            Inputs:     None
            Outputs:    None
        """
        # Load game options dialog
        loadDialog = LoadGameOptions(self.__database)
        # Execute dialog box and get response
        response = loadDialog.exec()
        # If dialog was accepted
        if response == loadDialog.Accepted:
            # Set the player name
            self.playerName = loadDialog.getName()
            # Set the configuration
            configuration = loadDialog.getConfiguration()
            # Create a game with the configuration
            self.createGame(configuration)

####################################################################################################

    def createGame(self, configuration):
        """ Executes a dialog based off the selected configuration

            Inputs:     configuration <list>
            Outputs:    None
        """
        # Create a game
        game = GameDialog(configuration, self.playerName, self.__database)
        # Execute the game
        game.exec()

####################################################################################################

    def openWeb(self):
        """ Opens the application's web component

            Inputs:     None
            Outputs:    None
        """
        # Open the url for game website
        QDesktopServices.openUrl(QUrl("http://0.0.0.0:8080/"))


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
        # Get current frame
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
