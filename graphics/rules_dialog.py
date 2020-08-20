#!/usr/bin/env python3

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt

import sys
import os

class RulesDialog(QDialog):
    """ A class to represent the dialog shown on a win """

    def __init__(self, *args, **kwargs):
        # Initialize parent class
        super().__init__(*args, **kwargs)
        # Set geometry
        self.setFixedSize(430, 540)

        #-------------------------------------------------------------------------------------------
        # LAYOUTS
        #-------------------------------------------------------------------------------------------
        mainLayout = QVBoxLayout(self)
        titleLayout = QHBoxLayout()
        textLayout = QHBoxLayout()
        iconLayout = QVBoxLayout()
        flagRow = QHBoxLayout()
        mineRow = QHBoxLayout()
        numberRow = QHBoxLayout()
        brickRow = QHBoxLayout()
        buttonLayout = QHBoxLayout()

        # Layout orientation
        flagRow.setSpacing(0)
        mineRow.setSpacing(0)
        numberRow.setSpacing(0)
        iconLayout.setAlignment(Qt.AlignHCenter)
        titleLayout.setAlignment(Qt.AlignHCenter)
        mainLayout.setSpacing(20)

        #-------------------------------------------------------------------------------------------
        # WIDGETS
        #-------------------------------------------------------------------------------------------
        # Title
        title = QLabel("Rules")
        title.setFont(QFont('Ariel', 14))

        # Text to be displayed
        text = "Depending on the board difficulty, there are varying amounts of \nmines hidden in "\
               "throughout the board. To reveal a squares contents,\nleft-click the square. "\
               "If a square is not touching any mines, it will be \nblank. If it is touching mines, "\
               "The revealed square will display a \nnumber representing the amount of mines it is "\
               "in contact with.\n\nTo mark squares confirmed as mines, use right-click to flag the mine."\
               "\n\nTo win the game, you must flag all mines or reveal all safe squares.\n\n"\
               "To race against the computer select multiplayer. In multiplayer mode, \nthe first "\
               "user to win the game is declared the winner. Additionally, if a \nplayer incorrectly "\
               "selects a mine then the opposing player is declared \nthe winner."

        # Create text label
        textLabel = QLabel(text)

        # Label for flag icon
        flagLabel = QLabel("Flag - right click")
        flagLabel.setFixedWidth(180)

        # Flag icon
        flagIcon = QIcon(os.path.join(sys.path[0], "graphics/images/flagIcon.png"))
        flag = QPushButton()
        flag.setFixedWidth(30)
        flag.setFixedHeight(30)
        flag.setIcon(flagIcon)

        # Label for bomb icon
        bombLabel = QLabel("Mine - Indicates Loss")
        bombLabel.setFixedWidth(180)

        # Bomb Icon
        bombIcon = QIcon(os.path.join(sys.path[0], "graphics/images/bombIcon.png"))
        bomb = QPushButton()
        bomb.setFixedSize(30, 30)
        bomb.setIcon(bombIcon)

        # Label for number Icon
        numberLabel = QLabel("Number - Nearby mines")
        numberLabel.setFixedWidth(180)

        # Number Icon
        number1 = QPushButton("1")
        number1.setFixedSize(30, 30)
        number1.setStyleSheet("color: blue;")

        # Label for button Icon
        buttonLabel = QLabel("Unclicked Square")

        # Button Icon
        button = QPushButton()
        button.setFixedWidth(30)
        button.setFixedHeight(30)
        styleSheet = "background:lightgrey;border-style:outset;border-width:4px;border-color:grey;width:20px;height:20px;"
        button.setStyleSheet(styleSheet)

        # Close button
        closeButton = QPushButton("close")

        #-------------------------------------------------------------------------------------------
        # LAYOUT MANAGEMENT
        #-------------------------------------------------------------------------------------------
        # Add text, title, and close button
        titleLayout.addWidget(title)
        textLayout.addWidget(textLabel)
        buttonLayout.addWidget(closeButton)

        # Add all icons and labels to rows
        flagRow.addWidget(flagLabel)
        flagRow.addWidget(flag)
        mineRow.addWidget(bombLabel)
        mineRow.addWidget(bomb)
        numberRow.addWidget(numberLabel)
        numberRow.addWidget(number1)
        brickRow.addWidget(buttonLabel)
        brickRow.addWidget(button)

        # Add all rows to the icon table
        iconLayout.addLayout(flagRow)
        iconLayout.addLayout(mineRow)
        iconLayout.addLayout(numberRow)
        iconLayout.addLayout(brickRow)

        # Add all layouts to main
        mainLayout.addLayout(titleLayout)
        mainLayout.addLayout(textLayout)
        mainLayout.addLayout(iconLayout)
        mainLayout.addLayout(buttonLayout)
        #-------------------------------------------------------------------------------------------
        # SIGNAL MANAGEMENT
        #-------------------------------------------------------------------------------------------
        # Connect the close button to the
        closeButton.clicked.connect(self.close)
