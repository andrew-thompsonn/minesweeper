from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton, QFrame, QLineEdit, QCheckBox, QTextEdit
from PyQt5.QtGui import QIcon, QFont, QImage, QPalette, QBrush
from PyQt5.QtCore import QSize, Qt, pyqtSignal

from postgreSQL.psql_database import PsqlDatabase

class MultiPlayerOptions(QDialog):
    configuration = pyqtSignal(object)
    nameSignal = pyqtSignal(object)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        gameDatabase = PsqlDatabase()
        gameDatabase.connectToDatabase()
        self.names = gameDatabase.selectNames()

        #-------------------------------------------------------------------------------------------
        # LAYOUTS
        #-------------------------------------------------------------------------------------------
        mainLayout = QVBoxLayout(self)
        titleLayout = QHBoxLayout()
        nameLayout = QHBoxLayout()
        playerOptionsLayout = QHBoxLayout()
        computerOptionsLayout = QHBoxLayout()
        buttonLayout = QHBoxLayout()

        #-------------------------------------------------------------------------------------------
        # WIDGETS
        #-------------------------------------------------------------------------------------------
        # Title
        titleLabel = QLabel("Multiplayer Options")
        titleLabel.setFont(QFont('Helvitica', 20))

        # Player information
        nameLabel = QLabel("Enter your name")
        # Line for the player to enter their name
        self.nameLineEdit = QLineEdit()
        # Start cursor left
        self.nameLineEdit.setAlignment(Qt.AlignLeft)

        # Options
        difficulties = ["Easy (10x10, 10 Mines)","Medium (16x16, 40 Mines)","Hard (16x30, 99 Mines)"]
        self.playerDifficultyBox = QComboBox()
        self.playerDifficultyBox.addItems(difficulties)
        playerDifficultyLabel = QLabel("Select your difficulty")

        self.computerDifficultyBox = QComboBox()
        self.computerDifficultyBox.addItems(difficulties)
        computerDifficultyLabel = QLabel("Select the computer's difficulty")

        self.computerSkillBox = QComboBox()
        self.computerSkillBox.addItems(["Easy", "Medium", "Hard"])
        computerSkillLabel = QLabel("Select the computer's skill level")

        # Submission
        submitButton = QPushButton("Play")
        submitLabel = QLabel("Ready?")

        backButton = QPushButton("Back")


        #-------------------------------------------------------------------------------------------
        # LAYOUT MANAGEMENT
        #-------------------------------------------------------------------------------------------
        titleLayout.addWidget(titleLabel)

        # Adding label for name
        nameLayout.addWidget(nameLabel)
        # Add line edit for name
        nameLayout.addWidget(self.nameLineEdit)

        playerOptionsLayout.addWidget(playerDifficultyLabel)
        playerOptionsLayout.addWidget(self.playerDifficultyBox)

        computerOptionsLayout.addWidget(computerDifficultyLabel)
        computerOptionsLayout.addWidget(self.computerDifficultyBox)
        computerOptionsLayout.addWidget(computerSkillLabel)
        computerOptionsLayout.addWidget(self.computerSkillBox)

        buttonLayout.addWidget(backButton)
        buttonLayout.addWidget(submitLabel)
        buttonLayout.addWidget(submitButton)

        mainLayout.addLayout(titleLayout)
        mainLayout.addLayout(nameLayout)
        mainLayout.addLayout(playerOptionsLayout)
        mainLayout.addLayout(computerOptionsLayout)
        mainLayout.addLayout(buttonLayout)

        #-------------------------------------------------------------------------------------------
        # SIGNAL MANAGEMENT
        #-------------------------------------------------------------------------------------------
        submitButton.clicked.connect(self.sendConfiguration)
        self.nameLineEdit.textChanged.connect(self.checkName)
        backButton.clicked.connect(self.closeDialog)

        self._exitCode = 1

    def checkName(self, name):
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

    def sendConfiguration(self):
        if self._exitCode == 0:
            # Get name for line edit
            name = self.nameLineEdit.text()
            # Emit name
            self.nameSignal.emit(name)
            # Set multiplayer configuration
            config = 2
            # Get player difficulty
            playerDifficulty = self.playerDifficultyBox.currentIndex()
            # Get computer difficulty
            computerDifficulty = self.computerDifficultyBox.currentIndex()
            # Get computer skill
            computerSkill = self.computerSkillBox.currentIndex()
            # Assign configuration tuple
            configuration = (config, playerDifficulty, computerDifficulty, computerSkill)
            # Send configuration
            self.configuration.emit(configuration)
            # Close window
            self.close()

    def closeDialog(self):
        self.close()
