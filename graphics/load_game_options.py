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

        self.gameDatabase = PsqlDatabase()
        self.gameDatabase.connectToDatabase()
        self.names = self.gameDatabase.selectNames()


        #-------------------------------------------------------------------------------------------
        # LAYOUTS
        #-------------------------------------------------------------------------------------------
        mainLayout = QVBoxLayout(self)
        mainLayout.setSpacing(50)
        titleLayout = QHBoxLayout()
        nameLayout = QHBoxLayout()
        buttonLayout = QHBoxLayout()
        saveLayout = QVBoxLayout()

        #-------------------------------------------------------------------------------------------
        # WIDGETS
        #-------------------------------------------------------------------------------------------
        # Title
        titleLabel = QLabel("Load Game")
        titleLabel.setFont(QFont('Helvitica', 20))

        # Player information
        nameLabel = QLabel("Enter your name")
        # Line for the player to enter their name
        self.nameLineEdit = QLineEdit()
        # Start cursor left
        self.nameLineEdit.setAlignment(Qt.AlignLeft)

        self.saveGameList = QListWidget()

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

        self.saveLabel = QLabel()
        saveLayout.addWidget(self.saveLabel)
        saveLayout.addWidget(self.saveGameList)
        saveLayout.setSpacing(1)

        mainLayout.addLayout(titleLayout)
        mainLayout.addLayout(nameLayout)
        mainLayout.addLayout(saveLayout)
        mainLayout.addLayout(buttonLayout)

        #-------------------------------------------------------------------------------------------
        # SIGNAL MANAGEMENT
        #-------------------------------------------------------------------------------------------

        self.nameLineEdit.textChanged.connect(self.checkName)
        submitButton.clicked.connect(self.sendConfiguration)
        self.saveGameList.currentRowChanged.connect(self.rowChanged)


        self._exitCode = 1
    def checkName(self, name):
        if name in self.names:
            self.nameLineEdit.setStyleSheet("color:green")
            self.saveLabel.setText("Detected saves for {}: ".format(self.nameLineEdit.text()))
            self.fillList(name)
        else:
            self._exitCode = 1
            self.saveLabel.setText("")
            self.clearList()
            self.nameLineEdit.setStyleSheet("color:red")

    def fillList(self, name):
        self.saveGameList.clear()
        self.savedGames = self.gameDatabase.selectSaves(name)

        # If only one save game

        self.saveIDs = []
        for game in self.savedGames:
            if game:
                self.saveGameList.addItem("{}  {}  {}".format(game[0][2], game[0][1], game[0][0]))
                self.saveIDs.append(game[0][2])

    def rowChanged(self):
        self._exitCode = 0

    def clearList(self):
        self.saveGameList.clear()

    def sendConfiguration(self):
        if self._exitCode == 0:
            saveID = self.saveIDs[self.saveGameList.currentRow() - 1]

            config = 10
            difficulty, visibleBrickCoords, mineCoords, flagCoords, gameID = self.gameDatabase.loadGame(saveID)
            coordinates = [visibleBrickCoords, mineCoords, flagCoords, gameID]
            configuration = [4, difficulty, coordinates]
            name = self.nameLineEdit.text()
            self.nameSignal.emit(name)
            self.configuration.emit(configuration)
            self.close()
