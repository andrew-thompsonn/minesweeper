#!/usr/bin/env python3


class Rules():
    def __init__(self):
        x = True

    def check(self, actionType, brick):
        # If action is a left click
        if actionType == "leftclick":
            # If clicked brick is already visible
            if brick.visible == True:
                # Invalid action
                return False
            else:
                return True

        elif actionType == "rightclick":
            # If clicked brick is already visible
            if brick.visible == True:
                # Invalid action
                return False
            else:
                return True
