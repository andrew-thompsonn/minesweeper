from PyQt5.QtWidgets import QCheckBox, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton, QFrame, QLineEdit, QCheckBox, QTextEdit
from PyQt5.QtGui import QIcon, QFont, QImage, QPalette, QBrush
from PyQt5.QtCore import QSize, Qt, pyqtSignal

class SinglePlayerOptions(QDialog):
    configuration = pyqtSignal(object)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #self.setFixedSize(600, 400)

        #self.setFixedSize(300, 300)

        # Default Configuration
        self.config = 1
        # Default Difficulty
        self.difficulty = 0
        #-------------------------------------------------------------------------------------------
        # LAYOUTS
        #-------------------------------------------------------------------------------------------
        mainLayout = QVBoxLayout(self)
        mainLayout.setSpacing(50)
        titleLayout = QHBoxLayout()
        optionsLayout = QHBoxLayout()
        buttonLayout = QHBoxLayout()

        #-------------------------------------------------------------------------------------------
        # WIDGETS
        #-------------------------------------------------------------------------------------------
        # Title
        titleLabel = QLabel("Singleplayer")
        titleLabel.setFont(QFont('Helvitica', 20))

        # Options
        self.difficultyBox = QComboBox()
        difficulties = ["Easy (10x10, 10 Mines)", "Medium (16x16, 40 Mines)", "Hard (16x30, 99 Mines)"]
        self.difficultyBox.addItems(difficulties)

        difficultyLabel = QLabel("Select a difficulty")

        self.computerOnlyBox = QCheckBox()
        self.computerOnlyBox.setText("Watch AI only")

        # Submission
        submitButton = QPushButton("Play")

        submitLabel = QLabel("Ready?")

        #-------------------------------------------------------------------------------------------
        # LAYOUT MANAGEMENT
        #-------------------------------------------------------------------------------------------
        titleLayout.addWidget(titleLabel)

        optionsLayout.addWidget(difficultyLabel)
        optionsLayout.addWidget(self.difficultyBox)
        optionsLayout.addWidget(self.computerOnlyBox)

        buttonLayout.addWidget(submitLabel)
        buttonLayout.addWidget(submitButton)

        mainLayout.addLayout(titleLayout)
        mainLayout.addLayout(optionsLayout)
        mainLayout.addLayout(buttonLayout)

        #-------------------------------------------------------------------------------------------
        # SIGNAL MANAGEMENT
        #-------------------------------------------------------------------------------------------

        submitButton.clicked.connect(self.sendConfiguration)


    def sendConfiguration(self):
        if self.computerOnlyBox.isChecked():
            self.config = 3
        else:
            self.config = 1

        difficulty = self.difficultyBox.currentIndex()
        config = (self.config, difficulty)
        print(config)
        print("sending configuration", self.config, difficulty)
        self.configuration.emit(config)
        self.close()
