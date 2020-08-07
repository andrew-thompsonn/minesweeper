from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QLineEdit, QCheckBox, QTextEdit
from PyQt5.QtGui import QIcon

class WinDialog(QDialog):
    def __init__(self, name, difficultyNum, time, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.name = name
        if difficultyNum == 0:
            difficulty = "Easy (10x10 - 10 Mines)"
        elif difficultyNum == 1:
            difficulty = "Medium (16x16 - 40 Mines)"
        else:
            difficulty = "Hard (16x30 - 99 Mines)"

        #-------------------------------------------------------------------------------------------
        # LAYOUTS
        #-------------------------------------------------------------------------------------------
        mainLayout = QVBoxLayout(self)
        textLayout = QHBoxLayout()
        statLayout = QVBoxLayout()
        buttonLayout = QHBoxLayout()

        #-------------------------------------------------------------------------------------------
        # WIDGETS
        #-------------------------------------------------------------------------------------------
        # Label to declare winner
        congratsLabel = QLabel(self.name + " wins!")

        # Game info

        difficultyLabel = QLabel("Difficulty: {}".format(difficulty))
        timeLabel = QLabel("Time: "+time)

        # Close button
        closeButton = QPushButton("close")


        #-------------------------------------------------------------------------------------------
        # LAYOUT MANAGEMENT
        #-------------------------------------------------------------------------------------------
        textLayout.addWidget(congratsLabel)
        statLayout.addWidget(difficultyLabel)
        statLayout.addWidget(timeLabel)
        buttonLayout.addWidget(closeButton)

        mainLayout.addLayout(textLayout)
        mainLayout.addLayout(statLayout)
        mainLayout.addLayout(buttonLayout)

        #-------------------------------------------------------------------------------------------
        # SIGNAL MANAGEMENT
        #-------------------------------------------------------------------------------------------
        closeButton.clicked.connect(self.close)