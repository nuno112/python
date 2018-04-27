# -*-coding:Utf-8 -*

import unittest
import sys
sys.path.insert(0, "/home/pce/workspace/python/Labyrinth Game 2.0/roboc/")

from labyrinth import *
from robot import *
from obstacle import *
from helpers import *
from roboc import *


class LabyrinthTest(unittest.TestCase):
    """This test case tests the features associated with the creation of the
    labyrinth and the associated objects"""

    def setUp(self):
        path = ("/home/pce/workspace/python/"
                "Labyrinth Game 2.0/roboc/maps/easy.txt")
        with open(path, "r") as file:
            self.content = file.read().strip()
        self.labyrinth = Labyrinth(mapTextToGrid(self.content))
        self.player1 = Player("nuno")
        self.robot1 = Robot(self.labyrinth.getEmptySpaces(), self.player1)
        self.robot2 = Robot(self.labyrinth.getEmptySpaces(), self.player1)
        self.robot3 = Robot(self.labyrinth.getEmptySpaces(), self.player1)

    def test_labyrinthDisplay(self):

        labyrinthFromFile = self.content
        labyrinthFromObject = self.labyrinth.__str__()
        self.assertEqual(labyrinthFromFile, labyrinthFromObject)

    def test_robotCreation(self):

        self.labyrinth.addRobot(self.robot1)
        self.labyrinth.addRobot(self.robot2)
        self.labyrinth.addRobot(self.robot3)
        self.assertIn(self.robot1, self.labyrinth.robots)


unittest.main()
