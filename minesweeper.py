#!/usr/bin/env python3

import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QProcess
from main_window import MainWindow

class Process(QProcess):
    def __init__(self):
        # Initialize base class
        QProcess.__init__(self)

        # Combine both standard in and standard error into one channel (standard in)
        self.setProcessChannelMode(QProcess.MergedChannels)

def main():


    app = QApplication(sys.argv)

    #------------------------------
    # webProcess = Process()
    # webProcess.start("./web/website.py")
    #
    # guiProcess = Process()
    # guiProcess.start()

    #------------------------------

    mainWindow = MainWindow()

    mainWindow.show()

    exit(app.exec())

    webProcess.stop()

if __name__ == "__main__":
    main()
