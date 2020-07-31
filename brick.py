#!/usr/bin/env python3


class Brick():
    def __init__(self, coordinates):
        # Coordinates
        self.coordinates = coordinates
        # Mine status
        self.mine = False
        # Flagged status
        self.flag = False
        # Number of mines touching
        self.touching = 0
        # Visibility status
        self.visible = False

    def setMine(self):
        # Set bomb to true
        self.mine = True

    def setFlag(self):
        # Set status of flag
        if self.flag:
            self.flag = False
        else:
            self.flag = True

    def setTouching(self, touching):
        # Set number of mines near
        self.touching = touching

    def setVisibility(self, visibility):
        # Set visibility of brick
        self.visible = visibility
