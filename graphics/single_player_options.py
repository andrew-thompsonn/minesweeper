from PyQt5.QtWidgets import QCheckBox, QDialog, QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtWidgets import QComboBox, QPushButton, QFrame, QLineEdit, QCheckBox, QTextEdit
from PyQt5.QtGui import QIcon, QFont, QImage, QPalette, QBrush
from PyQt5.QtCore import QSize, Qt, pyqtSignal

####################################################################################################

class SinglePlayerOptions(QDialog):
    """ Class to represent the dialog box for single player options """
    # configruation signal
    configuration = pyqtSignal(object)
    # Name signal
    nameSignal = pyqtSignal(object)

####################################################################################################

    def __init__(self, database, *args, **kwargs):
        # Initialize parent class
        super().__init__(*args, **kwargs)
        # Set default geometry
        self.setFixedSize(315, 200)
        # Get database
        self.__database = database
        # Get all names in the database
        self.names = self.__database.selectNames()
        # Set exit code to 1
        self._exitCode = 1
        # Single player configuration code is 1
        self.config = 1

        #-------------------------------------------------------------------------------------------
        # LAYOUTS
        #-------------------------------------------------------------------------------------------
        mainLayout = QVBoxLayout(self)
        titleLayout = QHBoxLayout()
        nameLayout = QHBoxLayout()
        optionsLayout = QHBoxLayout()
        buttonLayout = QHBoxLayout()

        titleLayout.setSpacing(0)
        nameLayout.setSpacing(0)
        optionsLayout.setSpacing(0)
        buttonLayout.setSpacing(0)

        mainLayout.setAlignment(Qt.AlignTop)
        mainLayout.setSpacing(20)

        #-------------------------------------------------------------------------------------------
        # WIDGETS
        #-------------------------------------------------------------------------------------------
        # Title
        titleLabel = QLabel("Singleplayer")
        titleLabel.setFont(QFont('Helvitica', 20))

        # Player information
        nameLabel = QLabel("Enter your name")
        nameLabel.setFixedWidth(120)
        self.nameLineEdit = QLineEdit()
        self.nameLineEdit.setFixedWidth(180)
        self.nameLineEdit.setAlignment(Qt.AlignLeft)

        # Player options
        difficulties = ["Easy (10x10, 10 Mines)","Medium (16x16, 40 Mines)","Hard (16x30, 99 Mines)"]
        self.difficultyBox = QComboBox()
        self.difficultyBox.setFixedWidth(180)
        self.difficultyBox.addItems(difficulties)
        difficultyLabel = QLabel("Select a difficulty")
        difficultyLabel.setFixedWidth(120)

        # Submission
        submitButton = QPushButton("Play")
        submitButton.setFixedWidth(180)
        submitLabel = QLabel("Ready?")
        submitLabel.setFixedWidth(120)

        #-------------------------------------------------------------------------------------------
        # LAYOUT MANAGEMENT
        #-------------------------------------------------------------------------------------------
        # Adding title to titley layout
        titleLayout.addWidget(titleLabel)

        # Adding label for name
        nameLayout.addWidget(nameLabel)
        # Add line edit for name
        nameLayout.addWidget(self.nameLineEdit)

        # Add the label for difficulties
        optionsLayout.addWidget(difficultyLabel)
        # Add combo box for difficulties
        optionsLayout.addWidget(self.difficultyBox)

        # Add label for submission
        buttonLayout.addWidget(submitLabel)
        # Add submit button
        buttonLayout.addWidget(submitButton)

        mainLayout.addLayout(titleLayout)
        mainLayout.addLayout(nameLayout)
        mainLayout.addLayout(optionsLayout)
        mainLayout.addLayout(buttonLayout)

        #-------------------------------------------------------------------------------------------
        # SIGNAL MANAGEMENT
        #-------------------------------------------------------------------------------------------
        # Connect submit button to send configuration
        submitButton.clicked.connect(self.setConfiguration)
        # Connect name line edit to validate name
        self.nameLineEdit.textChanged.connect(self.checkName)
        #submitButton.clicked.connect(self.accept)

####################################################################################################

    def checkName(self, name):
        """ Check the validity of a user's name.

            Inputs:     name <string>
            Outputs:    None
        """
        # If no letters or empty string
        if not any(char.isalpha() for char in name) or not name:
            # Set color to red
            self.nameLineEdit.setStyleSheet("color:red")
            # Set exit code to 1
            self._exitCode = 1
        # If name is already in the databse
        elif name in self.names:
            # Set color to green
            self.nameLineEdit.setStyleSheet("color:green;")
            # Set exit code to 0
            self._exitCode = 0
        # Otherwise,
        else:
            # Set color to black
            self.nameLineEdit.setStyleSheet("color:black")
            # Set exit code to 0
            self._exitCode = 0

####################################################################################################

    def setConfiguration(self):
        """ Set the user's chosen configruration

            Inputs:     None
            Outputs:    None
        """
        # If valid exit code
        if self._exitCode == 0:
            # Get the name from the line edit
            self.name = self.nameLineEdit.text()
            # Get the difficulty from the combo box
            difficulty = self.difficultyBox.currentIndex()
            # Format the configuration
            self.configuration = (self.config, difficulty)
            # Close window
            self.accept()

####################################################################################################

    def getName(self):
        """ Method to return the player's name

            Inputs:     None
            Outputs:    name <string>
        """
        return self.name

####################################################################################################

    def getConfiguration(self):
        """ Method to return the chosen configuration

            Inputs:     None
            Outputs:    configruation <tuple>
        """
        return self.configuration

####################################################################################################
