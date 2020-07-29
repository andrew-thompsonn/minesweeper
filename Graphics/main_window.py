#!/usr/bin/env python3

from PyQt5.QtWidgets import QMainWindow
from central_widget import CentralWidget

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)

        self.setWindowTitle("Minesweeper")

        centralWidget = CentralWidget()

        self.setCentralWidget(centralWidget)
