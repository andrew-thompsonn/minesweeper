from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QLineEdit, QCheckBox, QTextEdit
from PyQt5.QtGui import QIcon, QFont

class StartDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)



        #-------------------------------------------------------------------------------------------
        # LAYOUTS
        #-------------------------------------------------------------------------------------------
        mainLayout = QVBoxLayout(self)
        titleLayout = QHBoxLayout()
        buttonLayout = QHBoxLayout()

        #-------------------------------------------------------------------------------------------
        # WIDGETS
        #-------------------------------------------------------------------------------------------
        titleLabel = QLabel("Minesweeper")
        titleLabel.setFont(QFont('Ariel', 15))
        titleLabel.setStyleSheet("color:Darkblue")

        singlePlayerButton = QPushButton("Singleplayer")
        singlePlayerButton.setStyleSheet("background:slategrey;color:darkblue")
        multiPlayerButton = QPushButton("Multiplayer")
        multiPlayerButton.setStyleSheet("background:slategrey;color:darkblue")

        #-------------------------------------------------------------------------------------------
        # LAYOUT MANAGEMENT
        #-------------------------------------------------------------------------------------------

        titleLayout.addWidget(titleLabel)
        buttonLayout.addWidget(singlePlayerButton)
        buttonLayout.addWidget(multiPlayerButton)

        mainLayout.addLayout(titleLayout)
        mainLayout.addLayout(buttonLayout)
        #-------------------------------------------------------------------------------------------
        # SIGNAL MANAGEMENT
        #-------------------------------------------------------------------------------------------
        singlePlayerButton.clicked.connect(self.singlePlayerChosen)
        multiPlayerButton.clicked.connect(self.multiPlayerChosen)


    def singlePlayerChosen(self):
        self.accept()

    def multiPlayerChosen(self):
        self.accept(2)
