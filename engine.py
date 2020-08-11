#!/usr/bin/env python3
# 3,406

import time
from random import randrange

# Game Components
from game_components.game_state import GameState
from game_components.computer_player import ComputerPlayer
from game_components.rules import Rules
from game_components.player import Player

# Graphics
from graphics.computer_board import ComputerBoard
from graphics.player_board import PlayerBoard
from PyQt5.QtCore import QObject, pyqtSignal, QThread, QTimer
from PyQt5.QtWidgets import QApplication

# Database
from postgreSQL.psql_database import PsqlDatabase

####################################################################################################

class Engine(QObject):
    """ A class to connect and manage signals between player/computer graphics, and insert the
        player's and computer's actions into their respective game states
    """
    # Signal for number of flags
    playerFlagNumberChanged = pyqtSignal(int)
    # Signal for number of computer flags
    computerFlagNumberChanged = pyqtSignal(int)
    # Signal for game win
    winGame = pyqtSignal(list)
    # Signal for game loss
    loseGame = pyqtSignal(list)

####################################################################################################

    def __init__(self, config, difficulties, computerSkill, playerName, coordinates = [], *args, **kwargs):
        """ Initialize a player gameState, player board, computer game state, computer board,
            according to the difficulties and skills selected. If the user requests to load a game
            initialize a gamestate from load info.

            Inputs:     config <int>
                        difficulties [<int>]
                        computerSkill [<int>]
            Outputs:    None
        """
        # Initialize parent class
        super().__init__(*args, **kwargs)
        # Make config a class variable
        self.configuration = config
        # Initialize Rules
        self.rules = Rules()
        # Initialize GameTime
        self.gameTime = 0
        # Board properties that correspond to difficulty
        self.boardProperties = [(10, 10, 10), (16, 16, 40), (16, 30, 99)]
        # Database for save games, player info, and game logs
        self.gameDatabase = PsqlDatabase()
        # Connect to database
        self.gameDatabase.connectToDatabase()
        # Get player difficulty
        playerDifficulty = difficulties[0]
        # Get computer difficulty
        computerDifficulty = difficulties[1]
        # make computerskill a class variable
        self.computerSkill = computerSkill

        # Computer initialization
        self.initComputer(computerDifficulty, computerSkill, config)
        # Player initialization
        self.initPlayer(playerDifficulty, playerName, config)

        # Default loadGameID to invalid value
        self.loadGameID = 0
        # If load game info was passed
        if coordinates:
            # Load the game into current gameState
            self.playerGameState.loadGame(coordinates)
            # Update the graphics
            self.playerBoard.changeMany(self.playerGameState)
            # Loaded game ID
            self.loadGameID = coordinates[3]

        # If configuration is single or multiplayer
        if config == 1 or config == 2:
            # Start timer upon initialization
            self.startTime = time.time()

####################################################################################################

    def initPlayer(self, playerDifficulty, playerName, config):
        """ Initialize all aspects of a human player, including board, new gamestate, and player
            profile. If player doesn't already exist in database add to database. Run and
            initialize player graphics

            Inputs:     playerDifficulty <int>
                        playerName <str>
            Outputs:    None
        """
        # If watch AI only is enabled
        if config == 3:
            # Initialize a default player game state
            self.playerGameState = GameState(10, 10, 10)
        else:
            # Get correct board size and number of mines according to difficulty
            sizeX = self.boardProperties[playerDifficulty][0]
            sizeY = self.boardProperties[playerDifficulty][1]
            mines = self.boardProperties[playerDifficulty][2]
            # Initialize a player gamestate
            self.playerGameState = GameState(sizeX, sizeY, mines)

        # Initialize a human player
        self.player = Player(playerName, True)
        # Update database with players info
        self.gameDatabase.insertNewPlayer(playerName, True)

        # Initialize a player board
        self.playerBoard = None
        # Enable player board graphics
        self.initGraphics(self.playerBoard, self.playerGameState, self.player.isHuman)

####################################################################################################

    def initComputer(self, computerDifficulty, computerSkill, config):
        """ Initialize all aspects of a computer player, including board, new gamestate, and
            computer player. Always uses an existing computer player. Computer player profiles
            are already in the database.

            Inputs:     computerDifficulty <int>
                        computerSkill      <int>
            Outputs:    None
        """
        # If computer is not active
        if computerDifficulty == None:
            # Initialize a computer gameState
            self.computerGameState = GameState(10, 10, 10)
            # Computer has the skill of chuck norris
            computerSkill = 69
        else:
            # Get correct board size and number of mines according to difficulty
            sizeX = self.boardProperties[computerDifficulty][0]
            sizeY = self.boardProperties[computerDifficulty][1]
            mines = self.boardProperties[computerDifficulty][2]
            # Initialize a computer gameState
            self.computerGameState = GameState(sizeX, sizeY, mines)
        # If singleplayer AI
        if config == 3:
            # Computer skill is max
            computerSkill = 3

        # Initialize a computer player
        self.computerPlayer = ComputerPlayer(computerSkill, self.computerGameState)
        # Add computer player to database (In case we make more versions of the computer)
        self.gameDatabase.insertNewPlayer(self.computerPlayer.name, self.computerPlayer.isHuman)
        # Initialize a computer board
        self.computerBoard = None
        # Enable computer board graphics
        self.initGraphics(self.computerBoard, self.computerGameState, self.computerPlayer.isHuman)
        # Initialize computer rightclick queue
        self.rightClickQueue = []
        # Initialize computer left click queue
        self.leftClickQueue = []

####################################################################################################

    def getAIMove(self):
        """ Get moves from computer based on the current game state, and add them to a queue.
            When called, commit a single move from the queue, and if the queues are empty, call the
            computer to produce more moves

            Inputs:     None
            Outputs:    None
        """
        # If the computer's game or the player's game is over
        if self.computerGameState.status != 0 or self.playerGameState.status != 0:
            # Stop the timer
            self.timer.stop()
            # Return nothing
            return None

        # If queue for mines is empty
        if not self.rightClickQueue and not self.leftClickQueue:
            # Try to get more moves for mines
            mines = self.computerPlayer.getMines(self.computerGameState)
            # Try to get more moves for safe bricks
            safes = self.computerPlayer.getSafeBricks(self.computerGameState)
            # If still no moves
            if not mines and not safes:
                # Get a random move
                randomCoord = self.computerPlayer.first()
                # Add the random move to the left click Queue
                self.leftClickQueue.append(randomCoord)
            # If new moves were found
            else:
                # Fill the right click queue with the new moves
                self.rightClickQueue = self.rightClickQueue + mines
                # Fill the left click queue with the new moves
                self.leftClickQueue = self.leftClickQueue + safes

        # If there are more right click moves in the queue
        elif len(self.rightClickQueue) > len(self.leftClickQueue):
            # Get action from the right click queue
            rClickCoord = self.rightClickQueue.pop(0)
            # Commit right click
            self.commitComputerAction("rightclick", rClickCoord, self.computerGameState)
        # If there are more left click moves in the queue
        elif len(self.rightClickQueue) <= len(self.leftClickQueue) and len(self.leftClickQueue)!= 0:
            # Get action from the left click queue
            lClickCoord = self.leftClickQueue.pop(0)
            # Commit left click
            self.commitComputerAction("leftclick", lClickCoord, self.computerGameState)

####################################################################################################

    def runAI(self, computerSkill):
        """ Initialize a timer to run in background and call the getAIMove method. Time intervals
            depend on the level of skill the user selected for the computer

            Inputs:     computer skill <int>
            Outputs:    None
        """
        # Create a timer
        self.timer = QTimer()
        # Connect timer to AI moves
        self.timer.timeout.connect(self.getAIMove)
        # If computer skill is bad
        if computerSkill == 0:
            # Start timer with 1 move every second
            self.timer.start(1000)
        # If computer skill is medium
        elif computerSkill == 1:
            # Start timer with 1 move every 0.75 seconds
            self.timer.start(750)
        # If computer skill is good
        else:
            # Start timer with 1 move every 0.5 second
            self.timer.start(500)

####################################################################################################

    def runAIOnly(self):
        """ Runs the AI by itself, as fast as it can go. Updates computer knowledge of the current
            gamestate and commits actions the computer chooses. If computer can't produce a move
            requests a guess from the computer

            Inputs:     None
            Outputs:    None
        """
        # Start timer
        self.startTime = time.time()
        # Get computer player
        computer = self.computerPlayer
        # Get first move
        coordinates = computer.first()
        # Commit first move
        self.commitComputerAction("leftclick", coordinates, self.computerGameState)

        # While game is active
        while self.computerGameState.status == 0:
            # Get list of mines
            mines = computer.getMines(self.computerGameState)
            # For all confirmed mines
            for mine in mines:
                # Handle events
                QApplication.processEvents()
                # Commit action
                self.commitComputerAction("rightclick", mine, self.computerGameState)
                # If game over
                if self.computerGameState.status != 0:
                    # Exit loop
                    break
            # If game over
            if self.computerGameState.status != 0:
                # Exit loop
                break
            # Get list of safe bricks
            safeBricks = computer.getSafeBricks(self.computerGameState)
            # For all safe bricks
            for brick in safeBricks:
                # Handle events
                QApplication.processEvents()
                # Commit action
                self.commitComputerAction("leftclick", brick, self.computerGameState)
                # If game over
                if self.computerGameState.status != 0:
                    # Exit loop
                    break
            # If game over
            if self.computerGameState.status != 0:
                # Exit loop
                break
            # If no logical moves
            if not safeBricks and not mines:
                if len(self.computerGameState.visibleBricks) < 10:
                    # Get first move
                    coordinates = computer.first()
                else:
                    # Get a probabilistic guess
                    coordinates, prob = computer.probability(self.computerGameState)
                    print("Guessing {} with probability of {}".format(coordinates, prob))
                # Commit guess
                self.commitComputerAction("leftclick", coordinates, self.computerGameState)
                # Handle evenets
                QApplication.processEvents()

####################################################################################################

    def commitComputerAction(self, type, coordinate, gameState):
        """ Commits actions generated by the computer into the computer's current gameState. Filters
            out action types to determine the correct gamestate method to call and checks for
            wins/losses.

            Inputs:     action type <str>
                        coordinates (<int>, <int>)
                        gameState   <GameState>
            Outputs:    None
        """
        # Get brick at coordinates
        brick = gameState.bricks[coordinate]
        # If action is a left click
        if type == "leftclick":
            # Check rules
            if self.rules.check(type, brick):
                # If brick is not a mine and not touching any mines
                if brick.touching == 0 and brick.mine == False:
                    # Reveal all empty squares in surrounding area
                    gameState.clickMany(coordinate)
                    # Change many bricks in board
                    self.computerBoard.changeMany(self.computerGameState)
                # Otherwise click single brick
                else:
                    gameState.clickBrick(coordinate)
                    # Change single brick in board
                    self.computerBoard.changeBrick([coordinate, self.computerGameState])
        # If action is a right click
        if type == "rightclick":
            # Check rules
            if self.rules.check(type, brick):
                # Flag square
                gameState.flagBrick(coordinate)
                # Emit computer flag number changed
                self.computerFlagNumberChanged.emit(self.computerGameState.flags)
                # Change single brick in board
                self.computerBoard.changeBrick([coordinate, self.computerGameState])
        # If game is won
        if gameState.status == 1:
            # Change many bricks in board
            self.computerBoard.changeMany(self.computerGameState)
            # Get time at end of game
            self.endTime = time.time()
            # Document player as losing (Only matters if multiplayer enabled )
            self.playerGameState.status = 2
            # Calculate total time
            self.gameTime = self.endTime - self.startTime
            # Format into string to display to user
            strTime = self.convertTime(self.gameTime)
            # Emit win signal
            self.winGame.emit([strTime, "computer "+self.computerPlayer.name])
            # Commit computer game into database
            self.insertGameIntoDatabase(self.computerGameState, self.computerPlayer)
        # If game is lost
        elif gameState.status == 2:
            # Change many bricks in board
            self.computerBoard.changeMany(self.computerGameState)
            # Get time at end of game
            self.endTime = time.time()
            # Document player as winning (Only matters if multiplayer enabled )
            self.playerGameState.status = 1
            # Calculate total time
            self.gameTime = self.endTime - self.startTime
            # Format into string to display to user
            strTime = self.convertTime(self.gameTime)
            # Emit lose signal
            self.loseGame.emit([strTime, "computer "+self.computerPlayer.name])
            # Commit computer game into database
            self.insertGameIntoDatabase(self.computerGameState, self.computerPlayer)

####################################################################################################

    def commitPlayerClick(self, coordinates):
        """ Commit left click actions from the player into the player's game state. Checks for
            a player win/loss. If game is won/lost, emit win/lose game signal and stop the game
            timer.

            Inputs:     coordinates (<int>, <int>)
            Outputs:    None
        """
        # Get brick
        brick = self.playerGameState.bricks[coordinates]
        # If brick is not a mine and not touching any mines
        if brick.touching == 0 and brick.mine == False:
            # Reveal all empty squares in surrounding area
            self.playerGameState.clickMany(coordinates)
            # Change many bricks in board
            self.playerBoard.changeMany(self.playerGameState)
        # Otherwise reveal single bricks
        else:
            self.playerGameState.clickBrick(coordinates)
            # Change single brick in board
            self.playerBoard.changeBrick([coordinates, self.playerGameState])

        # if game is won
        if self.playerGameState.status == 1:
            # Change many bricks in board
            self.playerBoard.changeMany(self.playerGameState)
            # Get time at end of game
            self.endTime = time.time()
            # Document computer as losing (only matters if multiplayer enabled)
            self.computerGameState.status = 2
            # Calculate total time
            self.gameTime = self.endTime - self.startTime
            # Format into string to display to user
            strTime = self.convertTime(self.gameTime)
            # Emit win signal
            self.winGame.emit([strTime, self.player.name])
            # Commit player game to database
            self.insertGameIntoDatabase(self.playerGameState, self.player)
        # If game is lost
        elif self.playerGameState.status == 2:
            # Change many bricks in board
            self.playerBoard.changeMany(self.playerGameState)
            # Get time at end of game
            self.endTime = time.time()
            # Document computer as winning (only matters if multiplayer enabled)
            self.computerGameState.status = 1
            # Calculate total time
            self.gameTime = self.endTime - self.startTime
            # Format into string to display to user
            strTime = self.convertTime(self.gameTime)
            # Emit win signal
            self.loseGame.emit([strTime, self.player.name])
            # Commit player game to database
            self.insertGameIntoDatabase(self.playerGameState, self.player)

####################################################################################################

    def commitPlayerFlag(self, coordinates):
        """ Commits action for a player right click into the player's game state. Checks for
            a player win.  If game is won/lost, emit win/lose game signal and stop the game
            timer.

            Inputs:     coordinates (<int>, <int>)
            Outputs:    None
        """
        # Get the brick that was clicked
        brick = self.playerGameState.bricks[coordinates]
        # Flag the brick
        self.playerGameState.flagBrick(coordinates)
        # Emit signal for flags changed
        self.playerFlagNumberChanged.emit(self.playerGameState.flags)
        # Change single brick in board
        self.playerBoard.changeBrick([coordinates, self.playerGameState])

        # If game is won
        if self.playerGameState.status == 1:
            # Change many bricks in board
            self.playerBoard.changeMany(self.playerGameState)
            # Get time at end of game
            self.endTime = time.time()
            # Calculate total time
            self.gameTime = self.endTime - self.startTime
            # Format into string to display to user
            strTime = self.convertTime(self.gameTime)
            # Emit win signal
            self.winGame.emit([strTime, self.player.name])
            # Commit player win to database
            self.insertGameIntoDatabase(self.playerGameState, self.player)

####################################################################################################

    def initGraphics(self, board, gameState, human):
        """ Initialize the graphical representation for the game state of the requested player
            type. Connect signals from the player board to engine methods for commiting player
            clicks and flags to the gamestate

            Inputs:     board <Board>
                        gameState <GameState>
                        player type <str>
            Outputs:    None
        """
        # If computer player
        if not human:
            # Initialize computer board
            self.computerBoard = ComputerBoard(gameState, "computer")
        # If human player
        elif human:
            # Initialize human board
            self.playerBoard = PlayerBoard(gameState, "human")
            # Connect left click signal
            self.playerBoard.buttonLeftClick.connect(self.commitPlayerClick)
            # Connect right click signal
            self.playerBoard.buttonRightClick.connect(self.commitPlayerFlag)

####################################################################################################

    def insertGameIntoDatabase(self, gameState, player):
        """ Inserts game information into game_info table in database. Depending on configuration,
            will call the PsqlDatabase.insertGame() method one or multiple times. If the current
            game was loaded from a previous one, will call the finishSavedGame() method to
            update the database appropriately

            Inputs:     gameState <GameState>
                        player    <Player>
            Outputs:    None
        """
        print("INSERTING NEW GAME INTO DATABASE... ")
        # Get time value
        time = round(self.gameTime, 3)
        # If there was a loaded game
        if self.loadGameID != 0:
            # Update the database to finish a loaded game
            self.gameDatabase.finishSavedGame(gameState, self.player, self.loadGameID, time)
        # If multiplayer is enabled
        elif self.configuration == 2:
            # Get gameID for computer
            compGameID = self.gameDatabase.incrementGameID()
            # Get gameID for player
            playerGameID = compGameID + 1
            # playing against computer
            playerAgainstID = compGameID
            # playing against player
            compAgainstID = playerGameID
            # Insert computer
            self.gameDatabase.insertGame(self.computerGameState,self.computerPlayer,time,compGameID,compAgainstID)
            # Insert player
            self.gameDatabase.insertGame(self.playerGameState,self.player,time,playerGameID,playerAgainstID)
        # Otherwise insert the desired player and game into db
        else:
            # Get game ID
            gameID = self.gameDatabase.incrementGameID()
            # Insert into database
            self.gameDatabase.insertGame(gameState, player, time, gameID)
        print("done")

####################################################################################################

    def saveGame(self):
        """ Inserts a game in progress that the user has saved into the database.

            Inputs:     None
            Outputs:    None
        """
        print("SAVING GAME ...")
        # Get player gamestate
        gameState = self.playerGameState
        # Get player info
        player = self.player
        # Get end time
        self.endTime = time.time()
        # Calculate total time
        self.gameTime = self.convertTime(self.endTime - self.startTime)
        # Save the game to the database
        self.gameDatabase.insertSave(gameState, self.gameTime, player)

####################################################################################################

    def convertTime(self, time):
        """ Convert the game time from seconds to minutes/seconds/milliseconds. Create a string to
            represent the game time for the user.

            Inputs:     time <int>
            Outputs     timeString <str>
        """
        # If time is over an hour
        if time > 3600:
            # User needs to spend less time watching tv.
            timeString = "Your an idiot. You took over an hour. Find something better to do"
        # If time greater than a minute
        elif time >= 60:
            # Calculate minutes
            minutes = int(round(time / 60))
            # Calculate seconds
            seconds = round(time % 60, 3)
            # Create string representing time
            timeString = str(minutes)+":"+str(seconds)
        # Otherwise time is less than a minute
        else:
            # Calculate seconds
            seconds = round(time % 60, 3)
            # Create string representing time
            timeString = str(seconds)

        # Return the time string
        return timeString

####################################################################################################
