from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QLineEdit, QCheckBox, QTextEdit
from PyQt5.QtGui import QIcon, QFont

class WinDialog(QDialog):
    """ A class to represent the dialog shown on a win """
    
    def __init__(self, name, difficultyNum, time, *args, **kwargs):
        # Initialize parent class
        super().__init__(*args, **kwargs)
        # Set window geometry
        self.setFixedSize(250, 150)
        # Get name
        self.name = name

        # If difficutly is 0
        if difficultyNum == 0:
            # Set easy difficulty string
            difficulty = "Easy (10x10 - 10 Mines)"
        # If difficulty is 1s
        elif difficultyNum == 1:
            # Set medium difficulty string
            difficulty = "Medium (16x16 - 40 Mines)"
        # If difficulty is 2
        else:
            # Set hard difficulty string
            difficulty = "Hard (16x30 - 99 Mines)"
        #-------------------------------------------------------------------------------------------
        # LAYOUTS
        #-------------------------------------------------------------------------------------------
        mainLayout = QVBoxLayout(self)
        titleLayout = QHBoxLayout()
        textLayout = QHBoxLayout()
        statLayout = QVBoxLayout()
        buttonLayout = QHBoxLayout()

        #-------------------------------------------------------------------------------------------
        # WIDGETS
        #-------------------------------------------------------------------------------------------
        # Title
        title = QLabel("WIN")
        title.setFont(QFont('Ariel', 14))

        # Label to declare winner
        congratsLabel = QLabel("Player: "+self.name)

        # Game info
        difficultyLabel = QLabel("Difficulty: {}".format(difficulty))
        timeLabel = QLabel("Time: "+time)

        # Close button
        closeButton = QPushButton("close")

        #-------------------------------------------------------------------------------------------
        # LAYOUT MANAGEMENT
        #-------------------------------------------------------------------------------------------
        titleLayout.addWidget(title)
        textLayout.addWidget(congratsLabel)
        statLayout.addWidget(difficultyLabel)
        statLayout.addWidget(timeLabel)
        buttonLayout.addWidget(closeButton)

        mainLayout.addLayout(titleLayout)
        mainLayout.addLayout(textLayout)
        mainLayout.addLayout(statLayout)
        mainLayout.addLayout(buttonLayout)

        #-------------------------------------------------------------------------------------------
        # SIGNAL MANAGEMENT
        #-------------------------------------------------------------------------------------------
        closeButton.clicked.connect(self.close)
