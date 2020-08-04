#!/usr/bin/env python3

from PyQt5.QtWidgets import QMainWindow, QStackedWidget, QWidget
from PyQt5.QtGui import  QImage, QPalette, QBrush
from PyQt5.QtCore import QSize

from Dialogs.game_dialog import GameDialog

from Dialogs.multi_player_options import MultiPlayerOptions
from Dialogs.single_player_options import SinglePlayerOptions
from start_screen import StartScreen

class MainWindow(QMainWindow):
    """ Class for the main window of the application. Upon initialization, mutliple dialog boxes
        will be shown with configuration options for the application
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)

        # Start screen
        self.startScreen = StartScreen()
        # Set geometry
        self.setFixedSize(600, 400)
        # Create QImage
        oImage = QImage("images/watermine.jpg")
        # Scale QImage
        sImage = oImage.scaled(QSize(600,400))
        # Create a Palette
        palette = QPalette()
        # Set palette as background
        palette.setBrush(QPalette.Window, QBrush(sImage))
        # Set main window palette
        self.setPalette(palette)

        # Window title
        self.setWindowTitle("Minesweeper")
        # Central widget is the start screen
        self.setCentralWidget(self.startScreen)

        # Connect multiplayer button to multiplayer options
        self.startScreen.singlePlayerPressed.connect(self.singlePlayerOptions)
        # Connect single player button to single player options
        self.startScreen.multiPlayerPressed.connect(self.multiPlayerOptions)

    def singlePlayerOptions(self):
        """ Displays the options for singleplayer minesweeper gameplay and stores the users desired
            configuration
        """
        # Single player option dialog
        self.singleDialog = SinglePlayerOptions()
        # Connect submission of single player options to configuration
        self.singleDialog.configuration.connect(self.setConfiguration)
        # Execute the dialog box
        response = self.singleDialog.exec()

    def multiPlayerOptions(self):
        """ Displays the options for multiplayer minesweeper gameplay and stores the users desired
            configuration
        """
        # Multi player option dialog
        self.multiDialog = MultiPlayerOptions()
        # Connect Submission of multi player options to configuration
        self.multiDialog.configuration.connect(self.setConfiguration)
        # Execute the dialog box
        self.multiDialog.exec()

    def setConfiguration(self, configuration):
        """ Sets the MainWindow configuration variable """
        # Get the window that sent the signal
        sender = self.sender()
        # Close the window that sent the signal
        sender.close()
        # Set the configuration variable
        self.configuration = configuration
        # Create a game
        game = GameDialog(configuration)
        # Execute the game
        game.exec()
