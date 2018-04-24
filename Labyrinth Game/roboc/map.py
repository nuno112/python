# -*-coding:Utf-8 -*

"""This module contains the class Map"""

from labyrinth import Labyrinth


class Map:
    """Transition object between a map file and a labyrinth."""

    def __init__(self, name, grid):
        self.name = name
        self.labyrinth = Labyrinth(grid)

    def __repr__(self):
        return "<Map {}>".format(self.name)
