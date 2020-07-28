#!/usr/bin/env python3

from board import Board

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGridLayout
from PyQt5.QtWidgets import QPushButton, QLineEdit, QFrame,  QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

import sys
import os

class CentralWidget(QWidget):
    ############################################################################
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        mainLayout = QVBoxLayout(self)
        board = Board(10, 10, 10)
        mainLayout.addLayout(board)
