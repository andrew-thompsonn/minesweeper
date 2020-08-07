from PyQt5.QtWidgets import QCheckBox, QDialog, QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtWidgets import QComboBox, QPushButton, QFrame, QLineEdit, QCheckBox, QTextEdit
from PyQt5.QtGui import QIcon, QFont, QImage, QPalette, QBrush
from PyQt5.QtCore import QSize, Qt, pyqtSignal

from postgreSQL.psql_database import PsqlDatabase

class SinglePlayerOptions(QDialog):
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
        mainLayout.setSpacing(50)
        titleLayout = QHBoxLayout()
        nameLayout = QHBoxLayout()
        optionsLayout = QHBoxLayout()
        buttonLayout = QHBoxLayout()

        #-------------------------------------------------------------------------------------------
        # WIDGETS
        #-------------------------------------------------------------------------------------------
        # Title
        titleLabel = QLabel("Singleplayer")
        titleLabel.setFont(QFont('Helvitica', 20))

        # Player information
        nameLabel = QLabel("Enter your name")
        # Line for the player to enter their name
        self.nameLineEdit = QLineEdit()
        # Start cursor left
        self.nameLineEdit.setAlignment(Qt.AlignLeft)

        # Combo box for difficulty selection
        self.difficultyBox = QComboBox()
        # Options for difficulty
        difficulties = ["Easy (10x10, 10 Mines)","Medium (16x16, 40 Mines)","Hard (16x30, 99 Mines)"]
        # Adding dificulty items
        self.difficultyBox.addItems(difficulties)
        # Label for combo box
        difficultyLabel = QLabel("Select a difficulty")



        # Submission button
        submitButton = QPushButton("Play")
        # Submission Label
        submitLabel = QLabel("Ready?")

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

        submitButton.clicked.connect(self.sendConfiguration)
        self.nameLineEdit.textChanged.connect(self.checkName)


        self._exitCode = 1
    def checkName(self, name):
        if not any(char.isalpha() for char in name) or not name:
            self.nameLineEdit.setStyleSheet("color:red")
            self._exitCode = 1
        elif name in self.names:
            self.nameLineEdit.setStyleSheet("color:green;")
            self._exitCode = 0
        else:
            self.nameLineEdit.setStyleSheet("color:black")
            self._exitCode = 0


    def sendConfiguration(self):
        config = 1
        if self._exitCode == 0:
            name = self.nameLineEdit.text()
            self.nameSignal.emit(name)

            difficulty = self.difficultyBox.currentIndex()

            self.configuration.emit([config, difficulty])
            self.close()
