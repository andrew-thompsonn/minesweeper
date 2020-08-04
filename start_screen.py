from PyQt5.QtWidgets import QWidget, QDialog, QStackedWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QLineEdit, QCheckBox, QTextEdit
from PyQt5.QtGui import QIcon, QFont, QImage, QPalette, QBrush
from PyQt5.QtCore import QSize, Qt, pyqtSignal

class StartScreen(QWidget):
    singlePlayerPressed = pyqtSignal()
    multiPlayerPressed = pyqtSignal()
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #-------------------------------------------------------------------------------------------
        # LAYOUTS
        #-------------------------------------------------------------------------------------------
        mainLayout = QVBoxLayout(self)
        titleLayout = QVBoxLayout()
        buttonLayout = QHBoxLayout()


        titleLayout.setAlignment(Qt.AlignVCenter)
        #titleLayout.setAlignment(Qt.AlignLeft)
        titleLayout.setSpacing(1)

        buttonLayout.setSpacing(15)
        buttonLayout.setAlignment(Qt.AlignLeft)

        #-------------------------------------------------------------------------------------------
        # WIDGETS
        #-------------------------------------------------------------------------------------------
        titleLabel = QLabel("Minesweeper")


        titleLabel.setFont(QFont('Ariel', 40))
        titleLabel.setStyleSheet("color:maroon; background:transparent")

        subtitleLabel = QLabel("Created by Andrew Thompson")


        subtitleLabel.setFont(QFont('Ariel', 12))
        subtitleLabel.setStyleSheet("color:maroon; background:transparent")

        versionLabel = QLabel("Version 1.0.0")


        versionLabel.setFont(QFont('Ariel', 10))
        versionLabel.setStyleSheet("color:maroon; background:transparent")


        self.singlePlayerButton = QPushButton("Singleplayer")
        self.singlePlayerButton.setStyleSheet("background:slategrey;color:darkblue")
        self.singlePlayerButton.setFixedSize(260, 40)
        self.multiPlayerButton = QPushButton("Multiplayer")
        self.multiPlayerButton.setStyleSheet("background:slategrey;color:darkblue")
        self.multiPlayerButton.setFixedSize(260, 40)


        #-------------------------------------------------------------------------------------------
        # LAYOUT MANAGEMENT
        #-------------------------------------------------------------------------------------------

        titleLayout.addWidget(titleLabel)
        titleLayout.addWidget(subtitleLabel)
        titleLayout.addWidget(versionLabel)

        buttonLayout.addWidget(self.singlePlayerButton)
        buttonLayout.addWidget(self.multiPlayerButton)

        mainLayout.addLayout(titleLayout)
        mainLayout.addLayout(buttonLayout)
        #-------------------------------------------------------------------------------------------
        # SIGNAL MANAGEMENT
        #-------------------------------------------------------------------------------------------
        self.singlePlayerButton.clicked.connect(self.singlePlayerChosen)
        self.multiPlayerButton.clicked.connect(self.multiPlayerChosen)


    def singlePlayerChosen(self):
        self.singlePlayerPressed.emit()


    def multiPlayerChosen(self):
        self.multiPlayerPressed.emit()
