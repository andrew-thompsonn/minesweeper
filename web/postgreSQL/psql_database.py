#!/usr/bin/env python3

import random
import os
import psycopg2 as psql


####################################################################################################

class PsqlDatabaseError(Exception):
    """ Class to represent database error """
    pass

####################################################################################################

class PsqlDatabase:
    """ A class to represent and interact with the database """

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
        """ Method to make the initial connection to the database

            Inputs:     None
            Outputs:    None
        """
        try:
            # Set the path
            self.path = os.path.dirname(os.path.abspath(__file__))
            # Create a connection to the database
            self.cxn = psql.connect(
                host=self.host, database=self.database, port = self.port, user=self.user, password=self.password)
            # Create a cursor from the database connection
            self.cursor = self.cxn.cursor()
        # Except a psql error (error in connecting )
        except psql.Error as error:
            # Create error message
            errorMessage = "Error connecting to database. " + str(error)
            # Print error message
            print(errorMessage)
            # Raise a PsqlDatabaseError
            raise PsqlDatabaseError(errorMessage)

####################################################################################################

    def commit(self):
        """ Method to commit insertions or deletions to the database

            Inputs:     None
            Outputs:    None
        """
        self.cxn.commit()

####################################################################################################

    def selectNames(self):
        """ Get all names of players who have played the game.

            Inputs:     None
            Outputs:    names [string]
        """
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
        """ Insert a new player into the database/ check if player is already in database

            Inputs:     name <string>
                        isHuman <bool>
            Outputs:    None
        """
        # Get list of all players
        names = self.selectNames()
        # If player is already in databases
        if name in names or name == None:
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
        """ Get the player id of an existing player

            Inputs:     name <string>
            Outputs:    playerID <int>
        """
        # Select playerID from database
        self.cursor.execute("SELECT playerid FROM player_info WHERE name = '{}'".format(name))
        # Fetch unique player
        playerID = int(self.cursor.fetchone()[0])
        # Return the player ID
        return playerID

####################################################################################################

    def insertGame(self, gameState, player, time, gameID, multiplayerFlag=None):
        """ Insert game data into the database for games that have been saved or completed.

            Inputs:     gameState <GameState>
                        player <player>
                        time <float>
                        gameID <int>
                        multiplayerFlag <bool>
            Outputs:    None
        """
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

    def checkMultiplayer(self, saveID):
        """ Check if a saved game was multiplayer. If it was, return the opponents gameID. If not
            return None.

            Inputs:     saveID <int>
            Outputs:    None/oppopnentGameID <int>
        """
        # Query to get the game ID for the saved game
        self.cursor.execute("SELECT gameID from save_state where saveID = {};".format(saveID))
        # Get the game ID
        gameID = int(self.cursor.fetchone()[0])
        # Query to get games played against the same gameID
        self.cursor.execute("SELECT played_against from game_info where gameid = {};".format(gameID))
        # Get the opponents gameID
        opponentGameID = self.cursor.fetchone()
        # If not a multiplayer game
        if opponentGameID[0] == None:
            # Return None
            return None, None
        # If a multiplayter game
        else:
            # Get opponents gameID
            gameID = int(opponentGameID[0])
            # Query for computer name
            self.cursor.execute("SELECT name from player_info inner join game_info on player_info.playerID = game_info.playerID where game_info.gameID = {};".format(gameID))
            # Get Computer name
            computerName = self.cursor.fetchone()[0]
            # Dictionary of computer names and skills
            computerSkills = {"Computer_1": 0, "Computer_2":1, "Computer_3":2}
            # Get the skill based on computer name
            skill = computerSkills[computerName]
            # Query for save id
            self.cursor.execute("select saveid from save_state where gameid = {};".format(gameID))
            # Get the save id
            saveID = int(self.cursor.fetchone()[0])
            # Return the save id and computer skill
            return saveID, skill

####################################################################################################

    def insertSave(self, gameState, time, player, loadGameID=None, multiPlayerFlag=None):
        """ Insert game data as a new save_state in the database. If previously saved, use the old
            gameID, and update the information in the game_info table.

            Inputs:     gameState <GameState>
                        time <float>
                        player <Player>
                        loadGameID <int>
            Outputs:    None
        """

        # If game was not loaded
        if loadGameID == None:
            # Create new game ID
            gameID = self.incrementGameID()
            # If a multiplayer game
            if multiPlayerFlag != None :
                # Insert game with played against column
                self.insertGame(gameState, player, time, gameID, multiPlayerFlag)
            # Otherwise,
            else:
                # Insert game as singleplayer
                self.insertGame(gameState, player, time, gameID)

        # If game was loaded
        else:
            # Use the loaded game id
            gameID = loadGameID
            # Delete the old save_state entry
            self.cursor.execute("DELETE FROM save_state where gameID = {};".format(gameID))
            # Delete the old game_info entry
            self.cursor.execute("DELETE FROM game_info where gameID = {};".format(gameID))
            # If a multiplayer game
            if multiPlayerFlag != None:
                # Insert with multiplayer flag
                self.insertGame(gameState, player, time, gameID, multiPlayerFlag)
            # If singleplayer
            else:
                # Insert game as singleplayer
                self.insertGame(gameState, player, time, gameID)
            # Commit to db
            self.commit()

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
        """ Retrieve information about all of a player's saved games.

            Inputs:     name <string>
            Outputs:    saveInfo [(<string>, <string>, <int>)]
        """
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
        """ Get the information required to load a previously saved game

            Inputs:     saveID <int>
            Outputs:    difficulty <string>
                        visibleBrickCoords [(<int>, <int>)]
                        mineCoords [(<int>, <int>)]
                        flagCoords [(<int>, <int>)]
                        gameID <int>
        """
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
            difficulty = 2

        # Convert visible bricks to a list of tuples
        visibleBrickCoords = []
        for coordinate in gameStateInformation[1]:
            visibleBrickCoords.append(tuple(coordinate))

        # Convert mine coordinates to a list of tuples
        mineCoords = []
        for coordinate in gameStateInformation[2]:
            mineCoords.append(tuple(coordinate))

        # Initialize array for flag coordinates
        flagCoords = []
        # If no flagged bricks
        if not gameStateInformation[3]:
            # Do nothing
            pass
        # Otherwise
        else:
            # Convert flag coordinates to a list of tuples
            for coordinate in gameStateInformation[3]:
                flagCoords.append(tuple(coordinate))

        gameID = int(gameStateInformation[4])

        # Return game information
        return difficulty, visibleBrickCoords, mineCoords, flagCoords, gameID

####################################################################################################

    def finishSavedGame(self, gameState, player, gameID, time, multiplayerFlag=False):
        """ Takes care of housekeeping when a previously saved game is finished.

            Inputs:     gameState <GameState>
                        player <Player>
                        gameID <int>
                        time <float>
            Outputs:    None
        """

        # If multiplayer game
        if multiplayerFlag:
            # Query for the game it was played against
            self.cursor.execute("Select played_against from game_info where gameid = {};".format(gameID))
            # Get played against gameID
            playedAgainst = int(self.cursor.fetchone()[0])

        # Deleter the save info
        self.cursor.execute("Delete from save_state where gameID = {};".format(gameID))
        self.commit()
        # Get the old game time
        self.cursor.execute("Select game_time from game_info where gameID = {};".format(gameID))
        # Get the old game time
        oldTime = float(self.cursor.fetchone()[0])
        # Add to new game time
        newTime = round(oldTime + time, 3)
        # Delete the game info
        self.cursor.execute("Delete from game_info where gameID = {};".format(gameID))
        self.commit()

        if not multiplayerFlag:
            # Update with new game info
            self.insertGame(gameState, player, newTime, gameID)
        else:
            # Update with new game info (and multiplayer info)
            self.insertGame(gameState, player, newTime, gameID, playedAgainst)



####################################################################################################

    def createArrayString(self, coordinateList):
        """ Create a string representing an Array in postgresql syntax.

            Inputs:     coordinateList [(<int>, <int>)]
            Outputs:    arrayString <string>
        """
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

    def getSinglePlayerScores(self):
        """ Gets the top 5 singelplayer times for each difficulty.

            Inputs:     None
            Outputs:    easyData <list>
                        hardData <list>
                        mediumData <list>
        """
        # Difficulties in database
        difficulties = ['(10, 10)', '(16, 16)', '(16, 30)']
        # Get easy names and times
        easyData = self.getScores(True, difficulties[0])
        # Get medium names and times
        mediumData = self.getScores(True, difficulties[1])
        # Get hard names and times
        hardData = self.getScores(True, difficulties[2])
        # Return all score data
        return easyData, mediumData, hardData

####################################################################################################

    def getAIScores(self):
        """ Gets the top 5 AI times for each difficulty.

            Inputs:     None
            Outputs:    easyData <list>
                        mediumData <list>
                        hardData <list>
        """
        # Difficulties in database
        difficulties = ['(10, 10)', '(16, 16)', '(16, 30)']
        # Easy names and times
        easyData = self.getScores(False, difficulties[0])
        # Medium names and times
        mediumData = self.getScores(False, difficulties[1])
        # Hard names and times
        hardData = self.getScores(False, difficulties[2])
        # Return all score data
        return easyData, mediumData, hardData

####################################################################################################

    def getScores(self, isHuman, difficulty):
        """ Queries the database for the top 5 times for a human or computer player on a selected
            difficulty.

            Inputs:     isHuman <bool>
                        difficulty <string>
            Outputs:    data <list>
        """
        # Query to get names and times in ascending order for specific type of player
        self.cursor.execute("select name, game_time from player_info inner join game_info on game_info.playerID = player_info.playerID where type = {} and difficulty = '{}' and win = True and played_against is NULL order by game_time asc limit 5;".format(isHuman, difficulty))
        # Get all 5 names and times
        games = self.cursor.fetchall()
        # Initialize a list of data
        data = []
        # For all gamess
        for game in games:
            # Get name
            name = game[0]
            # Get time
            time = float(game[1])
            # Convert time to a string in mm:ss.ms
            timeString = self.getTimeString(time)
            # Add name and time to data
            data.append([name, timeString])
        # Return names and times
        return data

####################################################################################################

    def getMultiplayerScores(self):
        """ Select most recent multiplayer games winner and loser information

            Inputs:     None
            Outputs:    multiPlayerData <list>
        """
        # Query to get multiplayer winners
        self.cursor.execute("select name, game_time, difficulty, gameid from game_info inner join player_info on game_info.playerid = player_info.playerid where win = True and played_against is not null;")
        # Get results from query
        winners = self.cursor.fetchall()
        # Initialize a list of losers
        losers = []
        # For every multiplayer winner
        for winner in winners:
            # Get the game ID
            gameID = winner[3]
            # Query for the loser's information
            self.cursor.execute("select name, difficulty from game_info inner join player_info on game_info.playerid = player_info.playerid where win = False and played_against = {};".format(gameID))
            # Execute Query
            loser = self.cursor.fetchone()
            # Add loser information to losers list
            losers.append(loser)
        # Initialize a list of data representing multiplayer games
        multiPlayerData = []
        # For all winners and losers
        for index in range(len(winners)):
            # Get a winner
            winner = winners[index]
            # Get corresponding loser
            loser = losers[index]
            # Add a list of information about winner and loser to data list
            multiPlayerData.append([winner[0], winner[2], loser[0], loser[1], self.getTimeString(float(winner[1]))])
        # Return multiplayer data
        return multiPlayerData

####################################################################################################

    def incrementGameID(self):
        """ Increment the current highest game ID

            Inputs:     None
            Outputs:    nextGameID <int>
        """
        # Select highest game id
        self.cursor.execute("SELECT gameID from game_info order by gameID desc limit 1;")
        # Get highest game id
        try:
            # Try to get the highest value
            currentGameID = int(self.cursor.fetchone()[0])
        # If no value (no games have been played yet)
        except TypeError as error:
            # Use 0 As the current highest value
            currentGameID = 0
        # Increment by 1
        nextGameID = currentGameID + 1
        # Return next game id
        return nextGameID

####################################################################################################

    def incrementSaveID(self):
        """ Increment the current highest save ID

            Inputs:     None
            Outputs:    nextSaveID <int>
        """
        # Select Highest saveID
        self.cursor.execute("SELECT saveID from save_state order by saveID desc limit 1;")
        # Get highest save id
        try:
            # Try to get the highest value
            currentSaveID = int(self.cursor.fetchone()[0])
        # If no value (No games have been saved yet)
        except TypeError as error:
            # Use 0 as the current highest value
            currentSaveID = 0
        # Increment by 1
        nextSaveID = currentSaveID + 1
        # Return next save id
        return nextSaveID

####################################################################################################

    def getTimeString(self, time):
        """ Convert the game time from seconds to minutes/seconds/milliseconds. Create a string to
            represent the game time for the user.

            Inputs:     time <float>
            Outputs     timeString <str>
        """
        # If time is over an hour
        if time > 3600:
            # User needs to spend less time watching tv.
            timeString = "1+ hours"
        # If time greater than a minute
        elif time >= 60:
            # Calculate minutes
            minutes = int(round(time / 60))
            # Calculate seconds
            seconds = round(time % 60, 3)
        # Otherwise time is less than a minute
        else:
            minutes = 0
            # Calculate seconds
            seconds = round(time % 60, 3)
        # Get a string to represent seconds
        secondString = str(seconds)
        # If seconds is a single digit
        if seconds < 10:
            # Add a zero at the beginning
            secondString = "0"+str(seconds)
        # If seconds is a decimal only
        if seconds < 1:
            # Add two zeros at the beginning
            secondString == "00"+str(seconds)
        # Get a string to represent minutes
        minuteString = str(minutes)
        # If time is less than 10 minutes
        if minutes < 10:
            # Add a 0 at the beginning
            minuteString = "0"+str(minutes)
        # If time is less than 1 minute
        if minutes < 1:
            # Make the minute string 2 zeros
            minuteString = "00"
        # Concatenate minutes : seconds
        timeString = minuteString+":"+secondString
        # Return the time represented as a string mm:ss.ms
        return timeString

####################################################################################################
