# -*-coding:Utf-8 -*

"""This module contains the class Robot"""

from random import choice
from obstacle import *
from player import *


class Robot(Obstacle):

    def __init__(self, emptySpaces, player):
        Obstacle.__init__(self, hasCollision=True)
        self.robotInDoor = False
        self.position = choice(emptySpaces)
        self.player = player

    def __repr__(self):
        return "x"

    def updateRobotPosition(self, newPosiion, robotInDoor):
        """This method updates the robot possition."""

        self.position = newPosiion
        self.robotInDoor = robotInDoor
