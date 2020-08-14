from PyQt5.QtWidgets import QCheckBox, QDialog, QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtWidgets import QComboBox, QPushButton, QFrame, QLineEdit, QCheckBox, QTextEdit
from PyQt5.QtGui import QIcon, QFont, QImage, QPalette, QBrush
from PyQt5.QtCore import QSize, Qt, pyqtSignal

####################################################################################################

class WatchOptions(QDialog):
    """ Class to represent the dialog box for watch options """

####################################################################################################

    def __init__(self, *args, **kwargs):
        # Initialize parent class
        super().__init__(*args, **kwargs)
        # Set geometry of window
        self.setFixedSize(315, 200)
        # Watch configuration code is 3
        self.config = 3

        #-------------------------------------------------------------------------------------------
        # LAYOUTS
        #-------------------------------------------------------------------------------------------
        mainLayout = QVBoxLayout(self)
        titleLayout = QHBoxLayout()
        nameLayout = QHBoxLayout()
        optionsLayout = QHBoxLayout()
        buttonLayout = QHBoxLayout()

        mainLayout.setSpacing(20)
        nameLayout.setSpacing(0)
        optionsLayout.setSpacing(0)
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
        # Adding title to title layout
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
        # Connect submit button to set configuration
        submitButton.clicked.connect(self.setConfiguration)

####################################################################################################

    def setConfiguration(self):
        """ Set the user's chosen configuration

            Inputs:     None
            Outputs:    None
        """
        # Get computer difficulty from combo box
        computerDifficulty = self.difficultyBox.currentIndex()
        # Create configuration
        self.configuration = (self.config, computerDifficulty)
        # Close window
        self.accept()

####################################################################################################

    def getConfiguration(self):
        """ Method to return the chosen configuration

            Inputs:     None
            Outputs:    configuration <tuple>
        """
        # Return configuration
        return self.configuration

####################################################################################################
