from PyQt5.QtWidgets import QCheckBox, QDialog, QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtWidgets import QComboBox, QPushButton, QFrame, QLineEdit, QCheckBox, QTextEdit
from PyQt5.QtGui import QIcon, QFont, QImage, QPalette, QBrush
from PyQt5.QtCore import QSize, Qt, pyqtSignal


class WatchOptions(QDialog):
    configuration = pyqtSignal(object)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setFixedSize(315, 200)
        #-------------------------------------------------------------------------------------------
        # LAYOUTS
        #-------------------------------------------------------------------------------------------
        mainLayout = QVBoxLayout(self)
        mainLayout.setSpacing(20)
        titleLayout = QHBoxLayout()
        nameLayout = QHBoxLayout()
        nameLayout.setSpacing(0)
        optionsLayout = QHBoxLayout()
        optionsLayout.setSpacing(0)
        buttonLayout = QHBoxLayout()
        buttonLayout.setSpacing(0)

        #-------------------------------------------------------------------------------------------
        # WIDGETS
        #-------------------------------------------------------------------------------------------
        # Title
        titleLabel = QLabel("Watch the Computer")
        titleLabel.setFont(QFont('Helvitica', 20))

        # Combo box for difficulty selection
        self.difficultyBox = QComboBox()
        self.difficultyBox.setFixedWidth(180)
        # Options for difficulty
        difficulties = ["Easy (10x10, 10 Mines)","Medium (16x16, 40 Mines)","Hard (16x30, 99 Mines)"]
        # Adding dificulty items
        self.difficultyBox.addItems(difficulties)
        # Label for combo box
        difficultyLabel = QLabel("Select a difficulty")
        difficultyLabel.setFixedWidth(120)


        # Submission button
        submitButton = QPushButton("Watch")
        submitButton.setFixedWidth(180)
        # Submission Label
        submitLabel = QLabel("Ready?")
        submitLabel.setFixedWidth(120)

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
