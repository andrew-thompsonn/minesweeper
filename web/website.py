#!/usr/bin/env python3

from jinja2 import Environment, FileSystemLoader
import os
import os.path
import cherrypy
import random
import string

from postgreSQL.psql_database import PsqlDatabase

env = Environment(loader=FileSystemLoader('templates'))

class Application(object):
####################################################################################################
    @cherrypy.expose
    def index(self, *args, **kwargs):
        template = env.get_template('home.html')

        return template.render()

####################################################################################################
    @cherrypy.expose
    def scores(self, *args, **kwargs):
        template = env.get_template('scores.html')
        database = PsqlDatabase()
        database.connectToDatabase()
        easyData, mediumData, hardData = database.getSinglePlayerScores()
        compEasyData, compMediumData, compHardData = database.getAIScores()
        multiPlayerData = database.getMultiplayerScores()


        return template.render(sEasy = easyData, sMed = mediumData, sHard = hardData,
                               cEasy = compEasyData, cMed = compMediumData, cHard = compHardData,
                               multiData = multiPlayerData)

####################################################################################################
    @cherrypy.expose
    def about(self, *args, **kwargs):
        template = env.get_template('about.html')

        return template.render()

####################################################################################################
    # @cherrypy.expose
    # def about(self, *args, **kwargs):
    #     template = env.get_template('about.html')
    #
    #     # Create Database Object
    #     bvcDatabase = PsqlDatabase()
    #     # Connect to database
    #     bvcDatabase.connectToDatabase()
    #     # Get employee data
    #     data = bvcDatabase.select()
    #
    #     # Formatting employee data as list
    #     data1 = []
    #     for d in data:
    #         d1 = list(d)
    #         data1.append(d1)
    #
    #     # Render template with data
    #     return template.render(employees = data1)

    ################################################################################################
    # @cherrypy.expose
    # def signup(self, *args, **kwargs):
    #     template = env.get_template('signup.html')
    #     return template.render()

    ################################################################################################
    # @cherrypy.expose
    # def submitted(self, *args, **kwargs):
    #     template = env.get_template('submitted.html')
    #     return template.render()

    # @cherrypy.expose
    # def insertAppointment(self, fname, lname, number, email, pname, breed, date,
    #                       age, vet = None, groom = None, care = None, obedience = None,
    #                       advanced = None, adventure = None):
    #
    #     # Create Database object
    #     bvcDatabase = PsqlDatabase()
    #     # Connect to database
    #     bvcDatabase.connectToDatabase()
    #     # Insert appointment information
    #     bvcDatabase.insert(fname, lname, number, email, pname, breed, date,
    #                           age, vet, groom, care, obedience, advanced, adventure)
    #     # Display the submmitted page
    #     template = env.get_template('submitted.html')
    #     return template.render()

    ################################################################################################


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
            'tools.staticdir.dir': './public'
        }
    }

webapp = Application()
cherrypy.quickstart(webapp, '/', conf)
