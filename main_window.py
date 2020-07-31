#!/usr/bin/env python3

from PyQt5.QtWidgets import QMainWindow
from central_widget import CentralWidget

from start_dialog import StartDialog

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)


        #dialog = StartDialog()
        #response = dialog.exec()

        self.setWindowTitle("Minesweeper")

        centralWidget = CentralWidget()

        self.setCentralWidget(centralWidget)

        #self.setMinimumSize(900, 450)
        #self.setMaximumSize(900, 450)
