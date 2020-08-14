#!/usr/bin/env python3

from jinja2 import Environment, FileSystemLoader
import os
import os.path
import cherrypy
import random
import string

from postgreSQL.psql_database import PsqlDatabase

env = Environment(loader=FileSystemLoader('web/templates'))
####################################################################################################

class Application(object):
    """ A class to reptresent the web application  """

####################################################################################################

    @cherrypy.expose
    def index(self, *args, **kwargs):
        # Home page template
        template = env.get_template('home.html')
        # Render template
        return template.render()

####################################################################################################

    @cherrypy.expose
    def scores(self, *args, **kwargs):
        # Scores page template
        template = env.get_template('scores.html')
        # Create instance of database
        database = PsqlDatabase()
        # Connect to the database
        database.connectToDatabase()
        # Get single player score data
        easyData, mediumData, hardData = database.getSinglePlayerScores()
        # Get computer score data
        compEasyData, compMediumData, compHardData = database.getAIScores()
        # Get multiplayer data
        multiPlayerData = database.getMultiplayerScores()
        # Render template with game data
        return template.render(sEasy = easyData, sMed = mediumData, sHard = hardData,
                               cEasy = compEasyData, cMed = compMediumData, cHard = compHardData,
                               multiData = multiPlayerData)

####################################################################################################

if __name__ == "__main__":
    conf = {
        'global': {
            'server.socket_host': '0.0.0.0',
            'server.socket_port': 8080
        },
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './web/public'
        }
    }

####################################################################################################

webapp = Application()
cherrypy.quickstart(webapp, '/', conf)
