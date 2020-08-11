#!/usr/bin/env python3

import random
import os
import psycopg2 as psql
from pprint import pprint

class PsqlDatabase:
####################################################################################################

    def __init__(self, _host="127.0.0.1", _port = 5433, _database="game", _user_name="username", _passwd="example"):
        self.cxn = None
        self.cursor = None

        self.host = _host
        self.database = _database
        self.port = _port
        self.user = _user_name
        self.password = _passwd

####################################################################################################

    def connectToDatabase(self):
        try:
            self.path = os.path.dirname(os.path.abspath(__file__))

            # Create a connection to the database
            self.cxn = psql.connect(
                host=self.host, database=self.database, port = self.port, user=self.user, password=self.password)

            # Create a cursor from the database connection
            self.cursor = self.cxn.cursor()

        except psql.Error as error:
            print("Error connecting to database. " + str(error))

####################################################################################################

    def commit(self):
        self.cxn.commit()

####################################################################################################

    def selectNames(self):
        """ Get all names of players who have played the game """
        # Select all names of players
        self.cursor.execute("SELECT name FROM player_info;")
        # Fetch all names
        packagedNames = self.cursor.fetchall()
        # Initialize list for cleaned names
        names = []
        # For all names that were fetched
        for name in packagedNames:
            # Add the inner contents to names
            names.append(name[0])
        # Return names
        return names

####################################################################################################

    def insertNewPlayer(self, name, isHuman):
        """ Insert a new player into the database """
        # Get list of all players
        names = self.selectNames()
        # If player is already in databases
        if name in names or name == None:
            # Print status message
            print("Player already in database")
            # Return nothing
            return 0
        print("Adding {} as new player. Welcome {}!".format(name, name))
        #Command to insert name
        insertString = "INSERT INTO player_info (name, type) VALUES ('{}', {})".format(name, isHuman)
        #Execute command
        self.cursor.execute(insertString)
        #Commit changes
        self.commit()

####################################################################################################

    def getPlayerID(self, name):
        """ Get the player id of an existing player """
        # Select playerID from database
        self.cursor.execute("SELECT playerid FROM player_info WHERE name = '{}'".format(name))
        # Fetch unique player
        playerID = int(self.cursor.fetchone()[0])
        # Return the player ID
        return playerID

####################################################################################################

    def insertGame(self, gameState, player, time, gameID, multiplayerFlag = None):
        """ Insert game data into the database, for games that have finished """
        # Get player ID
        playerID = self.getPlayerID(player.name)
        # Get game difficulty string
        difficulty = "("+str(gameState.sizeX)+", "+str(gameState.sizeY)+")"
        # Get number of mines left
        minesLeft = gameState.flags
        # Get status of game (in progress, lost, won)
        status = gameState.status
        # Get win
        if status == 1:
            # Gamestate status of 1 indicates win
            win = True
        # For any other gamestate status
        else:
            # A win is not true
            win = False
        if multiplayerFlag == None:
            # Strings for database insertion
            insertStr = "INSERT INTO game_info (gameid, playerid, difficulty, game_time, mines_left, win, status) "
            valueStr = "VALUES ({}, {}, '{}', '{}', {}, {}, {});".format(gameID, playerID, difficulty, time, minesLeft, win, status)
        else:
            insertStr = "INSERT INTO game_info (gameid, playerid, difficulty, game_time, mines_left, win, status, played_against) "
            valueStr = "VALUES ({}, {}, '{}', '{}', {}, {}, {}, {});".format(gameID, playerID, difficulty, time, minesLeft, win, status, multiplayerFlag)

        # Execute the command
        self.cursor.execute(insertStr + valueStr)
        # Commit changes to the database
        self.commit()
        # If a previously saved game has been completed delete the save
        self.cursor.execute("delete from save_state where gameid = {};".format(gameID))
        # Commit changes to the database
        self.commit()


####################################################################################################

    def insertSave(self, gameState, time, player):
        """ Insert game data into the database for a game in progress """
        # Create new game ID
        gameID = self.incrementGameID()
        # Create instance of in progress game in game_info table
        self.insertGame(gameState, player, time, gameID)
        # Create string to represent size
        size = "("+str(gameState.sizeX)+" x "+str(gameState.sizeY)+")"
        # Create new save id
        saveID = self.incrementSaveID()
        # Initialize list for visible brick coordinates
        visibleCoords = []
        # For all bricks that are visible
        for brick in gameState.visibleBricks:
            # Append coordinates to visible coordinate list
            visibleCoords.append(brick.coordinates)
        # Get a postgres array string for visible bricks
        visibleArrayString = self.createArrayString(visibleCoords)
        # Get a postgres array string for visible bricks
        mineArrayString = self.createArrayString(gameState.mineCoords)
        # If no bricks are flagged
        if not gameState.flagCoords:
            # Insert null into flag location columns
            flagArrayString = 'NULL'
        # Otherwise, get a postgres array string for flag locations
        else: flagArrayString = self.createArrayString(gameState.flagCoords)

        # Insert statement
        insertString = "INSERT INTO save_state (saveid, size, visible_bricks, mine_locations, flag_locations, gameID, datetime ) "
        # Values statement
        valueString = "VALUES ({},'{}', {}, {}, {}, {}, localtimestamp);".format(saveID, size, visibleArrayString, mineArrayString, flagArrayString, gameID)

        # Execute the insertion
        self.cursor.execute(insertString + valueString)
        # Commit changes
        self.commit()

####################################################################################################

    def selectSaves(self, name):
        """ Retrieve information about all of a player's saved games """
        # Get player id from player name
        self.cursor.execute("select playerid from player_info where name = '{}';".format(name))
        playerID = int(self.cursor.fetchone()[0])
        # Get all player games that have been saved in progress
        self.cursor.execute("select gameid from game_info where playerid = {} and status = 0;".format(playerID))
        gameIDs = self.cursor.fetchall()

        # Initialize a list of formatted game ids
        formattedGameIDs = []
        # For all game ids returned from the db
        for gameID in gameIDs:
            # Get the actual id
            id = gameID[0]
            # Append it to the formatted game ids
            formattedGameIDs.append(id)
        # Initialize a list of save information s
        saveInfo = []
        # For all gameIDs
        for gameID in formattedGameIDs:
            # Select size, date, and saveID
            self.cursor.execute("select size, to_char(datetime at time zone 'US/Mountain', 'MM/DD/YYYY HH12:MI:SS AM'), saveid from save_state where gameid = {};".format(gameID))
            # Get all saves for the game id
            savedGames = self.cursor.fetchall()
            # Add information to save information list
            saveInfo.append(savedGames)
        # Return the saved information
        return saveInfo

####################################################################################################

    def loadGame(self, saveID):
        # Select information needed to init a game in progress
        self.cursor.execute("select size, visible_Bricks, mine_locations, flag_locations, gameID from save_state where saveID = {};".format(saveID))
        # fetch single
        gameStateInformation = self.cursor.fetchone()

        # Get difficulty based on size
        size = gameStateInformation[0]
        if size == "(10 x 10)":
            difficulty = 0
        elif size == "(16 x 16)":
            difficulty = 1
        else:
            difficulty = 3

        # Convert visible bricks to a list of tuples
        visibleBrickCoords = []
        for coordinate in gameStateInformation[1]:
            visibleBrickCoords.append(tuple(coordinate))

        # Convert mine coordinates to a list of tuples
        mineCoords = []
        for coordinate in gameStateInformation[2]:
            mineCoords.append(tuple(coordinate))

        # Convert flag coordinates to a list of tuples
        flagCoords = []
        for coordinate in gameStateInformation[3]:
            flagCoords.append(tuple(coordinate))

        gameID = int(gameStateInformation[4])

        # Return game information
        return difficulty, visibleBrickCoords, mineCoords, flagCoords, gameID

####################################################################################################


    def finishSavedGame(self, gameState, player, gameID, time):

        # Deleter the save info
        self.cursor.execute("Delete from save_state where gameID = {};".format(gameID))
        self.commit()
        # Get the old game time
        self.cursor.execute("Select game_time from game_info where gameID = {};".format(gameID))
        # Get the old game time
        oldTime = float(self.cursor.fetchone()[0])
        # Add to new game time
        newTime = oldTime + time
        print(newTime)

        # Delete the game info
        self.cursor.execute("Delete from game_info where gameID = {};".format(gameID))
        self.commit()
        # Update with new game info
        self.insertGame(gameState, player, newTime, gameID)


####################################################################################################

    def createArrayString(self, coordinateList):
        # Initialize string to represnt postgres array
        arrayString = "ARRAY["
        # For all coordinates
        for coordinate in coordinateList:
            # Get x coordinate
            xCoord = coordinate[0]
            # Gey y coordinate
            yCoord = coordinate[1]
            # Create sub-array string
            coordString = "["+str(xCoord)+", "+str(yCoord)+"], "
            # Append to array string
            arrayString += coordString
        # Delete last two characters
        arrayString = arrayString[:-2]
        # End array with brace
        arrayString += "]"
        # Return array string
        return arrayString

####################################################################################################

    def incrementGameID(self):
        # Select highest game id
        self.cursor.execute("SELECT gameID from game_info order by gameID desc limit 1;")
        # Get highest game id
        try:
            currentGameID = int(self.cursor.fetchone()[0])
        except TypeError as error:
            currentGameID = 0

        # Increment by 1
        nextGameID = currentGameID + 1
        # Return next game id
        return nextGameID

####################################################################################################

    def incrementSaveID(self):
        # Select Highest saveID
        self.cursor.execute("SELECT saveID from save_state order by saveID desc limit 1;")
        try:
            currentSaveID = int(self.cursor.fetchone()[0])
        except TypeError as error:
            currentSaveID = 0
        print(currentSaveID)
        nextSaveID = currentSaveID + 1
        return nextSaveID

####################################################################################################
