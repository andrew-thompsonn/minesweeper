#!/usr/bin/env python3


from player import Player


class ComputerPlayer(Player):
    def __init__(self, skill):
        self.skillLevel = skill

        self.action = []

        self.bricks = None

        #self.actionQueue


    def seeBoard(self, gameState):

        self.bricks = gameState.bricks


    def getAction(self):

        actionType = "leftclick"
        actionCoord = (4, 4)
        return actionType, actionCoord
