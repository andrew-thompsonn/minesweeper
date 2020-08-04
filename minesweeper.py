#!/usr/bin/env python3


import sys
from PyQt5.QtWidgets import QApplication
from main_window import MainWindow



def main():
    app = QApplication(sys.argv)


    mainWindow = MainWindow()


    mainWindow.show()

    exit(app.exec())

if __name__ == "__main__":
    main()
