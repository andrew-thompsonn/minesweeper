#!/usr/bin/env python

import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QProcess
from graphics.main_window import MainWindow

################## THINGS TO CLEAN UP #######################
#       1. Sync engine.gameTime and gameDialog.gameTime     #   DONE
#                                                           #
#       2. Check bug in computer win                        #   DONE
#                                                           #
#       3. Make computer not an idiot                       #   As smart as it gonna get
#                                                           #
#       4. Change multiprocessing for no errors             #   DONE
#############################################################

def main():
    # Create application
    app = QApplication(sys.argv)
    # Create Main window
    mainWindow = MainWindow()
    # Show the main window
    mainWindow.show()
    # Run the application
    exit(app.exec())

if __name__ == "__main__":
    main()
