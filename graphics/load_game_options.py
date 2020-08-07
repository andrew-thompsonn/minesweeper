from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QListWidget
from PyQt5.QtWidgets import QPushButton, QFrame, QLineEdit, QCheckBox, QTextEdit
from PyQt5.QtGui import QIcon, QFont, QImage, QPalette, QBrush
from PyQt5.QtCore import QSize, Qt, pyqtSignal

from postgreSQL.psql_database import PsqlDatabase

class LoadGameOptions(QDialog):
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

        # Add label for submission
        buttonLayout.addWidget(submitLabel)
        # Add submit button
        buttonLayout.addWidget(submitButton)

        mainLayout.addLayout(titleLayout)
        mainLayout.addLayout(nameLayout)
        mainLayout.addLayout(buttonLayout)

        #-------------------------------------------------------------------------------------------
        # SIGNAL MANAGEMENT
        #-------------------------------------------------------------------------------------------

        self.nameLineEdit.textChanged.connect(self.checkName)
        submitButton.clicked.connect(self.sendConfiguration)


        self._exitCode = 1
    def checkName(self, name):
        if name in self.names:
            self._exitCode = 0
            self.nameLineEdit.setStyleSheet("color:green")
        else:
            self._exitCode = 1
            self.nameLineEdit.setStyleSheet("color:red")

    def sendConfiguration(self):
        config = 10
        if self._exitCode == 0:
            name = self.nameLineEdit.text()
            self.nameSignal.emit(name)

            difficulty = self.difficultyBox.currentIndex()

            self.configuration.emit([config, difficulty])
            self.close()
