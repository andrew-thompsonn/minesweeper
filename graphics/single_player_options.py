from PyQt5.QtWidgets import QCheckBox, QDialog, QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtWidgets import QComboBox, QPushButton, QFrame, QLineEdit, QCheckBox, QTextEdit
from PyQt5.QtGui import QIcon, QFont, QImage, QPalette, QBrush
from PyQt5.QtCore import QSize, Qt, pyqtSignal

from web.postgreSQL.psql_database import PsqlDatabase

####################################################################################################

class SinglePlayerOptions(QDialog):
    """ Class to represent the dialog box for single player options """
    # configruation signal
    configuration = pyqtSignal(object)
    # Name signal
    nameSignal = pyqtSignal(object)

####################################################################################################

    def __init__(self, *args, **kwargs):
        # Initialize parent class
        super().__init__(*args, **kwargs)
        # Set default geometry
        self.setFixedSize(315, 200)
        # Create instance of database
        gameDatabase = PsqlDatabase()
        # Connect to database
        gameDatabase.connectToDatabase()
        # Get all names in the database
        self.names = gameDatabase.selectNames()
        # Set exit code to 1
        self._exitCode = 1

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
        submitButton.clicked.connect(self.sendConfiguration)
        # Connect name line edit to validate name
        self.nameLineEdit.textChanged.connect(self.checkName)

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

    def sendConfiguration(self):
        """ Emit a signal containing the user's chosen configuration

            Inputs:     None
            Outputs:    None
        """
        # Singliplayer configuration code is 1
        config = 1
        # If valid exit code
        if self._exitCode == 0:
            # Get the name from the line edit
            name = self.nameLineEdit.text()
            # Emit the player's name
            self.nameSignal.emit(name)
            # Get the difficulty from the combo box
            difficulty = self.difficultyBox.currentIndex()
            # Format configuration
            configuration = (config, difficulty)
            # Emit a signal containing the configuration code an difficulty
            self.configuration.emit(configuration)
            # Close window
            self.close()

####################################################################################################
