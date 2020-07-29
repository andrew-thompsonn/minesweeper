#!/usr/bin/env python3

from game_state import GameState
from computer_player import ComputerPlayer
from rules import Rules

class Engine():
####################################################################################################
    def __init__(self):
        # Initialize Rules
        self.rules = Rules()
        # Initialize a gameState
        self.gameState = GameState(10, 10, 10)
        # Print gameState
        self.gameState.printBoard()
        # Spin up a computer player
        self.runAI()
####################################################################################################
    def runAI(self):
        # Initialize computer player
        computer = ComputerPlayer("easy")
        # Get move from compute player
        actionType, coordinate = computer.getAction()
        # Commit move to game state
        self.commitAction(actionType, coordinate)
        # Print game state
        self.gameState.printBoard()
####################################################################################################
    def commitAction(self, type, coordinate):
        # Get brick at coordinates
        brick = self.gameState.bricks[coordinate]

        # If action is a left click
        if type == "leftclick":
            # Check rules
            if self.rules.check(type, brick):
                # If brick is not a mine and not touching any mines
                if brick.touching == 0 and brick.mine == False:
                    # Reveal all empty squares in surrounding area
                    self.gameState.clickMany(coordinate)
                # Otherwise click single brick
                else: self.gameState.clickBrick(coordinate)

        # If action is a right click
        if type == "rightclick":
            # Check rules
            if self.rules.check(type, brick):
                # Flag square
                self.gameState.flagBrick(coordinate)
####################################################################################################

def main():
    engine = Engine()

if __name__ == "__main__":
    main()
