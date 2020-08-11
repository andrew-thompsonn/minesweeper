from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QLineEdit, QCheckBox, QTextEdit
from PyQt5.QtGui import QIcon, QFont

class WinDialog(QDialog):
    def __init__(self, name, difficultyNum, time, *args, **kwargs):
        super().__init__(*args, **kwargs)



        self.setFixedSize(250, 150)

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
        titleLayout = QHBoxLayout()
        textLayout = QHBoxLayout()
        statLayout = QVBoxLayout()
        buttonLayout = QHBoxLayout()

        #-------------------------------------------------------------------------------------------
        # WIDGETS
        #-------------------------------------------------------------------------------------------
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
