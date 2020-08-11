from PyQt5.QtWidgets import QWidget, QDialog, QStackedWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QLineEdit, QCheckBox, QTextEdit
from PyQt5.QtGui import QIcon, QFont, QImage, QPalette, QBrush
from PyQt5.QtCore import QSize, Qt, pyqtSignal

class StartScreen(QWidget):
    """ The main menu screen """
    singlePlayerPressed = pyqtSignal()
    multiPlayerPressed = pyqtSignal()
    watchButtonPressed = pyqtSignal()
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #-------------------------------------------------------------------------------------------
        # LAYOUTS
        #-------------------------------------------------------------------------------------------
        # Main Layout
        mainLayout = QVBoxLayout(self)
        mainLayout.setAlignment(Qt.AlignTop)
        mainLayout.setSpacing(5)
        # Title layout
        titleLayout = QVBoxLayout()
        # button layout
        buttonLayout = QVBoxLayout()

        # Set orientation of title layout
        titleLayout.setAlignment(Qt.AlignHCenter)
        #titleLayout.setAlignment(Qt.AlignTop)
        titleLayout.setSpacing(1)

        # Set orientation of button layout
        buttonLayout.setAlignment(Qt.AlignHCenter)
        buttonLayout.setSpacing(10)

        #-------------------------------------------------------------------------------------------
        # WIDGETS
        #-------------------------------------------------------------------------------------------
        # Title font and color
        titleLabel = QLabel("Minesweeper")
        titleLabel.setFixedSize(355, 90)
        titleLabel.setFont(QFont('Ariel', 40))
        titleLabel.setStyleSheet("color:black; background:transparent")

        # Subtitle font and color
        subtitleLabel = QLabel("Created by Andrew Thompson")
        subtitleLabel.setFixedSize(245, 20)
        subtitleLabel.setAlignment(Qt.AlignCenter)
        subtitleLabel.setFont(QFont('Ariel', 12))
        subtitleLabel.setStyleSheet("color:black; background:transparent")

        # Version font and color
        versionLabel = QLabel("Version 1.0.0")
        versionLabel.setFixedSize(90, 20)
        versionLabel.setAlignment(Qt.AlignCenter)
        versionLabel.setFont(QFont('Ariel', 10))
        versionLabel.setStyleSheet("color:black; background:transparent")

        # Button for single player options
        self.singlePlayerButton = QPushButton("Singleplayer")
        self.singlePlayerButton.setStyleSheet("background:rgba(100, 100, 125, 0.7);")
        self.singlePlayerButton.setFixedSize(195, 35)

        # Button for multiplayer options
        self.multiPlayerButton = QPushButton("Multiplayer")
        self.multiPlayerButton.setStyleSheet("background:rgba(100, 100, 125, 0.7);")
        self.multiPlayerButton.setFixedSize(195, 35)

        # Button for loading previous saves
        self.watchButton = QPushButton("Watch")
        self.watchButton.setStyleSheet("background:rgba(100, 100, 125, 0.7);")
        self.watchButton.setFixedSize(195, 35)

        #-------------------------------------------------------------------------------------------
        # LAYOUT MANAGEMENT
        #-------------------------------------------------------------------------------------------
        # Add titles to title layout
        titleLayout.addWidget(titleLabel)
        titleLayout.addWidget(subtitleLabel)
        titleLayout.addWidget(versionLabel)

        # Add buttons to button layout

        #buttonLayout.addStretch(1)
        buttonLayout.addWidget(self.singlePlayerButton)

        buttonLayout.addWidget(self.multiPlayerButton)
        buttonLayout.addWidget(self.watchButton)
        buttonLayout.addStretch(0)

        # Add all to main layout
        mainLayout.addLayout(titleLayout)

        mainLayout.addLayout(buttonLayout)

        #-------------------------------------------------------------------------------------------
        # SIGNAL MANAGEMENT
        #-------------------------------------------------------------------------------------------
        self.singlePlayerButton.clicked.connect(self.singlePlayerChosen)
        self.multiPlayerButton.clicked.connect(self.multiPlayerChosen)
        self.watchButton.clicked.connect(self.watchChosen)

    def singlePlayerChosen(self):
        self.singlePlayerPressed.emit()

    def multiPlayerChosen(self):
        self.multiPlayerPressed.emit()

    def watchChosen(self):
        self.watchButtonPressed.emit()
