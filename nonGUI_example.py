#!/usr/bin/env python3

from computer_player import ComputerPlayer
from game_state import GameState

import time

def main():
    gameState = GameState(10, 10, 10)
    computer = ComputerPlayer("easy", gameState)

    firstMove = computer.first()
    commitAction("leftclick", firstMove, gameState)
    while gameState.status == 0:
        mines = computer.getMines(gameState)
        clear = computer.getSafeBricks(gameState)

        for mine in mines:
            commitAction("rightclick", mine, gameState)
        for brick in clear:
            commitAction("leftclick", brick, gameState)

        if not mines and not clear:
            randomMove = computer.first()
            commitAction("leftclick", firstMove, gameState)

def commitAction(type, coordinate, gameState):
    time.sleep(1)
    # Get brick at coordinates
    brick = gameState.bricks[coordinate]
    # If action is a left click
    if type == "leftclick":
        # If brick is not a mine and not touching any mines
        if brick.touching == 0 and brick.mine == False:
            # Reveal all empty squares in surrounding area
            gameState.clickMany(coordinate)
        # Otherwise click single brick
        else: gameState.clickBrick(coordinate)
    # If action is a right click
    if type == "rightclick":
        gameState.flagBrick(coordinate)
    # print the board
    gameState.printBoard()

if __name__ == "__main__":
    main()
