from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QLineEdit, QCheckBox, QTextEdit
from PyQt5.QtGui import QIcon

class LoseDialog(QDialog):
    def __init__(self, name, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.__name = name

        #-------------------------------------------------------------------------------------------
        # LAYOUTS
        #-------------------------------------------------------------------------------------------
        mainLayout = QVBoxLayout(self)
        textLayout = QHBoxLayout()
        buttonLayout = QHBoxLayout()

        #-------------------------------------------------------------------------------------------
        # WIDGETS
        #-------------------------------------------------------------------------------------------
        congratsLabel = QLabel("Loss")
        closeButton = QPushButton("close")

        #-------------------------------------------------------------------------------------------
        # LAYOUT MANAGEMENT
        #-------------------------------------------------------------------------------------------
        textLayout.addWidget(congratsLabel)
        buttonLayout.addWidget(closeButton)

        mainLayout.addLayout(textLayout)
        mainLayout.addLayout(buttonLayout)

        #-------------------------------------------------------------------------------------------
        # SIGNAL MANAGEMENT
        #-------------------------------------------------------------------------------------------
        closeButton.clicked.connect(self.accept)
