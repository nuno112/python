# -*-coding:Utf-8 -*

"""This module contains the class Labyrinth"""


class Labyrinth:
    """Class that represents a labyrinth"""

    maxY = 20
    maxX = 20

    def __init__(self, grid):
        self.grid = grid
        self.robots = []

    def __repr__(self):
        text = ""
        for x in range(0, self.maxX):
            for y in range(0, self.maxY):
                if (x, y) in self.grid:
                    text += self.grid[(x, y)]
            text += "\n"
        return text.strip()

    def getEmptySpaces(self):
        """This method returns the currently empty spaces in a labyritnh
        as a list containing tuples in the form (x, y)"""

        emptySpaces = []
        for x in range(0, self.maxX):
            for y in range(0, self.maxY):
                if (x, y) in self.grid and self.grid[(x, y)] == " ":
                    emptySpaces.append((x, y))
        return emptySpaces

    def addRobot(self, robot):
        """This methods adds a robot to the labyrinth as a player connects"""

        self.robots.append(robot)
        self.grid[robot.position] = "x"

    def checkRobotMovement(self, newPosiion):
        """This method checks if the robot can move to the inputed possition
        It also checks if the robot as reached the end of the labyrinth
        and thus, won"""

        # TODO alter this shit to just check if it can move, and then call
        # robot.updateRobotPosition
        oldPosition = self.position
        a, b = newPosiion
        occupiedSpaces = (".", "O", "U", "X")
        if self.grid[a][b] not in occupiedSpaces and not self.robotInDoor:
            self.robotPosition = newPosiion
            self.grid[a][b] = "X"
            a, b = oldPosition
            self.grid[a][b] = " "

        elif self.grid[a][b] == ".":
            self.robotPosition = newPosiion
            a, b = oldPosition
            self.grid[a][b] = " "
            self.robotInDoor = True

        elif self.grid[a][b] == "O":
            print("\nYou can't move there!\n")

        elif self.grid[a][b] == "U":
            self.robotPosition = newPosiion
            self.grid[a][b] = "X"
            a, b = oldPosition
            self.grid[a][b] = " "
            return True

        elif self.robotInDoor:
            self.robotPosition = newPosiion
            self.grid[a][b] = "X"
            a, b = oldPosition
            self.grid[a][b] = "."
            self.robotInDoor = False
