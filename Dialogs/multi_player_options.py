from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton, QFrame, QLineEdit, QCheckBox, QTextEdit
from PyQt5.QtGui import QIcon, QFont, QImage, QPalette, QBrush
from PyQt5.QtCore import QSize, Qt, pyqtSignal

class MultiPlayerOptions(QDialog):
    configuration = pyqtSignal(object)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #-------------------------------------------------------------------------------------------
        # LAYOUTS
        #-------------------------------------------------------------------------------------------
        mainLayout = QVBoxLayout(self)
        titleLayout = QHBoxLayout()
        playerOptionsLayout = QHBoxLayout()
        computerOptionsLayout = QHBoxLayout()
        buttonLayout = QHBoxLayout()

        #-------------------------------------------------------------------------------------------
        # WIDGETS
        #-------------------------------------------------------------------------------------------
        # Title
        titleLabel = QLabel("Multiplayer Options")

        # Options
        difficulties = ["Easy (10x10, 10 Mines)", "Medium (16x16, 40 Mines)", "Hard (16x30, 99 Mines)"]
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
        mainLayout.addLayout(playerOptionsLayout)
        mainLayout.addLayout(computerOptionsLayout)
        mainLayout.addLayout(buttonLayout)

        #-------------------------------------------------------------------------------------------
        # SIGNAL MANAGEMENT
        #-------------------------------------------------------------------------------------------
        submitButton.clicked.connect(self.sendConfiguration)
        backButton.clicked.connect(self.closeDialog)


    def sendConfiguration(self):
        config = 2
        playerDifficulty = self.playerDifficultyBox.currentIndex()
        computerDifficulty = self.computerDifficultyBox.currentIndex()
        computerSkill = self.computerSkillBox.currentIndex()
        configuration = (config, playerDifficulty, computerDifficulty, computerSkill)
        self.configuration.emit(configuration)
        self.close()

    def closeDialog(self):
        print("Here")
        self.rejected()
