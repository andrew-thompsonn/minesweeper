from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QListWidget
from PyQt5.QtWidgets import QPushButton, QFrame, QLineEdit, QCheckBox, QTextEdit
from PyQt5.QtGui import QIcon, QFont, QImage, QPalette, QBrush
from PyQt5.QtCore import QSize, Qt, pyqtSignal


####################################################################################################

class LoadGameOptions(QDialog):
    """ A class to represent the dialog for load game options """

####################################################################################################

    def __init__(self, database, *args, **kwargs):
        # Initialize parent class
        super().__init__(*args, **kwargs)
        # Set geometry
        self.setFixedSize(315, 350)
        # Get the database
        self.__database = database
        # Get all names in database
        self.names = ["Andrew"]
        """self.names = self.__database.selectNames()"""
        # Set exit code to 1
        self._exitCode = 1

        #-------------------------------------------------------------------------------------------
        # LAYOUTS
        #-------------------------------------------------------------------------------------------
        mainLayout = QVBoxLayout(self)
        titleLayout = QHBoxLayout()
        nameLayout = QHBoxLayout()
        buttonLayout = QHBoxLayout()
        saveLayout = QVBoxLayout()

        mainLayout.setSpacing(20)
        saveLayout.setSpacing(1)

        #-------------------------------------------------------------------------------------------
        # WIDGETS
        #-------------------------------------------------------------------------------------------
        # Title
        titleLabel = QLabel("Load Game")
        titleLabel.setFont(QFont('Helvitica', 20))

        # Player information
        nameLabel = QLabel("Enter your name")
        self.nameLineEdit = QLineEdit()
        self.nameLineEdit.setAlignment(Qt.AlignLeft)

        # Saved games
        self.saveGameList = QListWidget()
        self.saveLabel = QLabel()

        # Submission
        submitButton = QPushButton("Play")
        submitLabel = QLabel("Ready?")

        #-------------------------------------------------------------------------------------------
        # LAYOUT MANAGEMENT
        #-------------------------------------------------------------------------------------------
        # Adding title to titley layout
        titleLayout.addWidget(titleLabel)

        # Adding name widgets
        nameLayout.addWidget(nameLabel)
        nameLayout.addWidget(self.nameLineEdit)

        # Add submission widgets
        buttonLayout.addWidget(submitLabel)
        buttonLayout.addWidget(submitButton)

        # Add save widgets
        saveLayout.addWidget(self.saveLabel)
        saveLayout.addWidget(self.saveGameList)

        # Add all layouts to main
        mainLayout.addLayout(titleLayout)
        mainLayout.addLayout(nameLayout)
        mainLayout.addLayout(saveLayout)
        mainLayout.addLayout(buttonLayout)

        #-------------------------------------------------------------------------------------------
        # SIGNAL MANAGEMENT
        #-------------------------------------------------------------------------------------------
        # Connect line edit to check the validity of the name
        self.nameLineEdit.textChanged.connect(self.checkName)
        # Connect submit button to set configuration
        submitButton.clicked.connect(self.setConfiguration)
        # If a save is selected set exit code to 1
        self.saveGameList.currentRowChanged.connect(self.rowChanged)

####################################################################################################

    def checkName(self, name):
        """ Check the database to see if the player is already registered.

            Inputs:     name <string>
            Outputs:    None
        """
        # If name is in database
        if name in self.names:
            # Set the color to green
            self.nameLineEdit.setStyleSheet("color:green")
            # Show text to verify the user is in the database
            self.saveLabel.setText("Detected saves for {}: ".format(self.nameLineEdit.text()))
            # Fill the list with the players detected saves
            self.fillList(name)
        # Otherwise,
        else:
            # Set the exit code to 1
            self._exitCode = 1
            # Clear the label
            self.saveLabel.setText("")
            # Clear the list
            self.clearList()
            # Set the color to red
            self.nameLineEdit.setStyleSheet("color:red")

####################################################################################################

    def fillList(self, name):
        """ Fill the save list with information about a player's saved games

            Inputs:     name <string>
            Outputs:    None
        """
        # Clear any current contents of the list
        self.saveGameList.clear()
        # Get save information from database
        self.savedGames = self.__database.selectSaves(name)
        # Initialize a list of saveIDs
        self.saveIDs = []
        # For all saved games
        for game in self.savedGames:
            # If there is information
            if game:
                # Add to the list
                self.saveGameList.addItem("{}  {}  {}".format(game[0][2], game[0][1], game[0][0]))
                # Add the save id to the saveID list
                self.saveIDs.append(game[0][2])

####################################################################################################

    def rowChanged(self):
        """ If a save is selected, then the player may submit the dialog

            Inputs:     None
            Outputs:    None
        """
        # If any save is selected set exit code to 1
        self._exitCode = 0

####################################################################################################

    def clearList(self):
        """ A method to clear all items from the save list

            Inputs:     None
            Outputs:    None
        """
        # Clear the list
        self.saveGameList.clear()

####################################################################################################

    def setConfiguration(self):
        """ Set the player name variable and configuration variable. Close the window

            Inputs:     None
            Outputs:    None
        """
        # If a valid exit code
        if self._exitCode == 0:
            # Get the saveID
            saveID = self.saveIDs[self.saveGameList.currentRow()]
            # Check the saved game for multiplayer
            multiplayerFlag, computerSkill = self.__database.checkMultiplayer(saveID)

            print("Singleplayer save: {} multiplayer save: {}".format(saveID, multiplayerFlag))
            # If it is a multiplayer game
            if multiplayerFlag != None:
                # Get all save information from database about the player game
                pDiff,pVisible,pMines,pFlags,pGameID = self.__database.loadGame(saveID)
                # Get all save information from database about the computer game
                cDiff,cVisible,cMines,cFlags,cGameID = self.__database.loadGame(multiplayerFlag)
                # Concatenate player information
                pCoordinates = [pVisible, pMines, pFlags, pGameID]
                # Concatenate computer information
                cCoordinates = [cVisible, cMines, cFlags, cGameID]
                # Configuration code for loaded multiplayer game is 5
                config = 5
                # Set the configuration
                self.configuration = (config, pDiff, cDiff, computerSkill, [pCoordinates, cCoordinates])
                # Set the name
                self.name = self.nameLineEdit.text()
                # Close and accept
                self.accept()
            # Otherwise it is a singleplayer game
            else:
                # Configuration code for singleplayer load is 4
                config = 4
                # Get all save information from database
                difficulty,visibleBrickCoords,mineCoords,flagCoords,gameID=self.__database.loadGame(saveID)
                # Concatenate into single variable
                coordinates = [visibleBrickCoords, mineCoords, flagCoords, gameID]
                # Set the configuration
                self.configuration = (config, difficulty, coordinates)
                # Set the name
                self.name = self.nameLineEdit.text()
                # Close the dialog
                self.accept()

####################################################################################################

    def getConfiguration(self):
        """ Returns the configuration variable to the main window

        Inputs:     None
        Ouputs:     configuration <tuple>
        """
        # Return configuration
        return self.configuration

####################################################################################################

    def getName(self):
        """ Returns the configuration variable to the main window

        Inputs:     None
        Ouputs:     name <string>
        """
        # Return name
        return self.name

####################################################################################################
