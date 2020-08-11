#!/usr/bin/env python3
from jinja2 import Environment, FileSystemLoader
import os
import os.path
import cherrypy
import random
import string

# from web.website import Application

import sys
from PyQt5.QtWidgets import QApplication
from main_window import MainWindow


# Created functions for multiprocessing, not sure exactly how this will work though

####################################################################################################

# def startGUI():
#     app = QApplication(sys.argv)
#
#     mainWindow = MainWindow()
#
#     mainWindow.show()
#
#     exit(app.exec())
#
# ####################################################################################################
#
# def startWeb():
#     # Configuration for cherrypy server
#     conf = {
#         'global': {
#             'server.socket_host': '0.0.0.0',
#             'server.socket_port': 8080
#         },
#         '/': {
#             'tools.sessions.on': True,
#             'tools.staticdir.root': os.path.abspath(os.getcwd())
#         },
#         '/static': {
#             'tools.staticdir.on': True,
#             'tools.staticdir.dir': './public'
#         }
#     }
#
#     webapp = Application()
#     cherrypy.quickstart(webapp, '/', conf)

####################################################################################################

def main():
    app = QApplication(sys.argv)

    mainWindow = MainWindow()

    mainWindow.show()

    exit(app.exec())

if __name__ == "__main__":
    main()
