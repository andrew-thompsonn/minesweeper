#!/usr/bin/env python3

import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QProcess
from main_window import MainWindow

# 4,568 Lines !

class Process(QProcess):
    def __init__(self):
        # Initialize base class
        QProcess.__init__(self)
        # Combine both standard in and standard error into one channel (standard in)
        self.setProcessChannelMode(QProcess.MergedChannels)

def main():
    #----------------------------------#
    # Create Process for web
    webProcess = Process()
    # Start web server
    webProcess.start("./web/website.py")
    #----------------------------------#
    # Create application
    app = QApplication(sys.argv)
    # Create Main window
    mainWindow = MainWindow()
    # Show the main window
    mainWindow.show()
    # Run the application
    exit(app.exec())
    # Stop the web process
    webProcess.stop()
    #----------------------------------#

if __name__ == "__main__":
    main()
