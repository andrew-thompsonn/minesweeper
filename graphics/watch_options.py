from PyQt5.QtWidgets import QCheckBox, QDialog, QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtWidgets import QComboBox, QPushButton, QFrame, QLineEdit, QCheckBox, QTextEdit
from PyQt5.QtGui import QIcon, QFont, QImage, QPalette, QBrush
from PyQt5.QtCore import QSize, Qt, pyqtSignal

from postgreSQL.psql_database import PsqlDatabase

class WatchOptions(QDialog):
    configuration = pyqtSignal(object)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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
        titleLabel = QLabel("Watch the Computer")
        titleLabel.setFont(QFont('Helvitica', 20))



        # Combo box for difficulty selection
        self.difficultyBox = QComboBox()
        # Options for difficulty
        difficulties = ["Easy (10x10, 10 Mines)","Medium (16x16, 40 Mines)","Hard (16x30, 99 Mines)"]
        # Adding dificulty items
        self.difficultyBox.addItems(difficulties)
        # Label for combo box
        difficultyLabel = QLabel("Select a difficulty")


        # Submission button
        submitButton = QPushButton("Watch")
        # Submission Label
        submitLabel = QLabel("Ready?")

        #-------------------------------------------------------------------------------------------
        # LAYOUT MANAGEMENT
        #-------------------------------------------------------------------------------------------
        # Adding title to titley layout
        titleLayout.addWidget(titleLabel)


        # Add the label for difficulties
        optionsLayout.addWidget(difficultyLabel)
        # Add combo box for difficulties
        optionsLayout.addWidget(self.difficultyBox)

        # Add label for submission
        buttonLayout.addWidget(submitLabel)
        # Add submit button
        buttonLayout.addWidget(submitButton)

        mainLayout.addLayout(titleLayout)
        mainLayout.addLayout(optionsLayout)
        mainLayout.addLayout(buttonLayout)

        #-------------------------------------------------------------------------------------------
        # SIGNAL MANAGEMENT
        #-------------------------------------------------------------------------------------------

        submitButton.clicked.connect(self.submitPressed)


    def submitPressed(self):
        config = 3
        computerDifficulty = self.difficultyBox.currentIndex()
        configuration = (config, computerDifficulty)
        self.configuration.emit(configuration)
        self.close()
