from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton, QFrame, QLineEdit, QCheckBox, QTextEdit
from PyQt5.QtGui import QIcon, QFont, QImage, QPalette, QBrush
from PyQt5.QtCore import QSize, Qt, pyqtSignal

####################################################################################################

class MultiPlayerOptions(QDialog):
    """ A class to represent the dialog box for multiplayer options """
    # Configuration signal
    configuration = pyqtSignal(object)
    # Name signal
    nameSignal = pyqtSignal(object)

####################################################################################################

    def __init__(self, database, *args, **kwargs):
        # Initialize parent class
        super().__init__(*args, **kwargs)
        # Set window geometry
        self.setFixedSize(420, 200)
        # Get database
        self.__database = database
        # Get all names in database
        self.names = self.__database.selectNames()
        # Set exit code to 1
        self._exitCode = 1
        # Multiplayer configuration code is 2
        self.config = 2
        #-------------------------------------------------------------------------------------------
        # LAYOUTS
        #-------------------------------------------------------------------------------------------
        mainLayout = QVBoxLayout(self)
        titleLayout = QHBoxLayout()
        nameLayout = QHBoxLayout()
        playerOptionsLayout = QHBoxLayout()
        computerOptionsLayout = QHBoxLayout()
        computerSkillLayout = QHBoxLayout()
        buttonLayout = QHBoxLayout()

        #-------------------------------------------------------------------------------------------
        # WIDGETS
        #-------------------------------------------------------------------------------------------
        # Title
        titleLabel = QLabel("Multiplayer Options")
        titleLabel.setFont(QFont('Helvitica', 20))

        # Player information
        nameLabel = QLabel("Enter your name")
        nameLabel.setFixedWidth(200)
        self.nameLineEdit = QLineEdit()
        self.nameLineEdit.setAlignment(Qt.AlignLeft)
        self.nameLineEdit.setFixedWidth(200)

        # Options - player
        difficulties = ["Easy (10x10, 10 Mines)","Medium (16x16, 40 Mines)","Hard (16x30, 99 Mines)"]
        self.playerDifficultyBox = QComboBox()
        self.playerDifficultyBox.setFixedWidth(200)
        self.playerDifficultyBox.addItems(difficulties)
        playerDifficultyLabel = QLabel("Select your difficulty")
        playerDifficultyLabel.setFixedWidth(200)

        # Options - computer
        self.computerDifficultyBox = QComboBox()
        self.computerDifficultyBox.setFixedWidth(200)
        self.computerDifficultyBox.addItems(difficulties)
        computerDifficultyLabel = QLabel("Select the computer's difficulty")
        computerDifficultyLabel.setFixedWidth(200)

        # Options - computer
        self.computerSkillBox = QComboBox()
        self.computerSkillBox.setFixedWidth(200)
        self.computerSkillBox.addItems(["Easy", "Medium", "Hard"])
        computerSkillLabel = QLabel("Select the computer's skill level")
        computerSkillLabel.setFixedWidth(200)

        # Submission
        submitButton = QPushButton("Play")
        submitLabel = QLabel("Ready?")
        submitButton.setFixedWidth(200)
        submitLabel.setFixedWidth(200)

        #-------------------------------------------------------------------------------------------
        # LAYOUT MANAGEMENT
        #-------------------------------------------------------------------------------------------
        # Add title
        titleLayout.addWidget(titleLabel)

        # Adding label for name
        nameLayout.addWidget(nameLabel)
        # Add line edit for name
        nameLayout.addWidget(self.nameLineEdit)

        # Add player options
        playerOptionsLayout.addWidget(playerDifficultyLabel)
        playerOptionsLayout.addWidget(self.playerDifficultyBox)

        # Add computer options
        computerOptionsLayout.addWidget(computerDifficultyLabel)
        computerOptionsLayout.addWidget(self.computerDifficultyBox)
        computerSkillLayout.addWidget(computerSkillLabel)
        computerSkillLayout.addWidget(self.computerSkillBox)

        # Add buttons
        buttonLayout.addWidget(submitLabel)
        buttonLayout.addWidget(submitButton)

        mainLayout.addLayout(titleLayout)
        mainLayout.addLayout(nameLayout)
        mainLayout.addLayout(playerOptionsLayout)
        mainLayout.addLayout(computerOptionsLayout)
        mainLayout.addLayout(computerSkillLayout)
        mainLayout.addLayout(buttonLayout)

        #-------------------------------------------------------------------------------------------
        # SIGNAL MANAGEMENT
        #-------------------------------------------------------------------------------------------
        # Connect submit button to set configuration
        submitButton.clicked.connect(self.setConfiguration)
        # Connect line edit to check name
        self.nameLineEdit.textChanged.connect(self.checkName)

####################################################################################################

    def checkName(self, name):
        """ Verify validity of user name.

            Inputs:     name <string>
            Outputs:    None
        """
        # If no letters or empty name
        if not any(char.isalpha() for char in name) or not name:
            # Red indicates invalid name
            self.nameLineEdit.setStyleSheet("color:red")
            # Exit code is 1
            self._exitCode = 1
        # If name already in system
        elif name in self.names:
            # Green to indicate a returning user
            self.nameLineEdit.setStyleSheet("color:green;")
            # Exit code is zero
            self._exitCode = 0
        # Otherwise
        else:
            # Normal text
            self.nameLineEdit.setStyleSheet("color:black")
            # Exit code is zero
            self._exitCode = 0

####################################################################################################

    def setConfiguration(self):
        """ Emit singals with user information and chosen configuration

            Inputs:     None
            Outputs:    None
        """
        # If valid exit code
        if self._exitCode == 0:
            # Get name for line edit
            self.name = self.nameLineEdit.text()
            # Get player difficulty
            playerDifficulty = self.playerDifficultyBox.currentIndex()
            # Get computer difficulty
            computerDifficulty = self.computerDifficultyBox.currentIndex()
            # Get computer skill
            computerSkill = self.computerSkillBox.currentIndex()
            # Assign configuration tuple
            self.configuration = (self.config, playerDifficulty, computerDifficulty, computerSkill)
            # Close window
            self.accept()

####################################################################################################

    def getName(self):
        """ Method to return the player's name

            Inputs:     None
            Outputs:    name <string>
        """
        # Return player's name
        return self.name

####################################################################################################

    def getConfiguration(self):
        """ Method to return the chosen configuration

            Inputs:     None
            Outputs:    configuration <tuple>
        """
        # Return the selected configuration
        return self.configuration

####################################################################################################
