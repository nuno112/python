# -*-coding:Utf-8 -*

"""This module contains the class Obstacle, which is the base class for all
things present in the labyrinth (doors, robots, walls, goal)"""


class Obstacle:

    def __init__(self, hasCollision):
        self.hasCollision = hasCollision
