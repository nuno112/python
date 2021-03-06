# -*-coding:Utf-8 -*

"""This module contains the class Labyrinth"""


class Labyrinth:
    """Class that represents a labyrinth"""

    maxY = 20
    maxX = 20

    def __init__(self, grid):
        self.grid = grid
        self.robots = []
        self.won = False

    def __repr__(self):
        text = ""
        for x in range(0, self.maxX):
            for y in range(0, self.maxY):
                if (x, y) in self.grid:
                    text += self.grid[(x, y)]
            text += "\n"
        return text.strip()

    def getLabyrinthSize(self):
        """This method gets the max coordinates of the labyrinth"""
        maxX = 0
        maxY = 0
        for coords in self.grid:
            x, y = coords
            if x > maxX:
                maxX = x
            if y > maxY:
                maxY = y
        return (maxX, maxY)

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

    def checkRobotMovement(self, robot, newPosition):
        """This method checks if the robot can move to the inputed possition
        It also checks if the robot as reached the end of the labyrinth
        and thus, won"""

        oldPosition = robot.position

        occupiedSpaces = (".", "O", "U", "x")
        if (self.grid[newPosition] not in occupiedSpaces
           and not robot.robotInDoor):
            robot.updateRobotPosition(newPosition, False)
            self.grid[newPosition] = "X"
            self.grid[oldPosition] = " "
            return True

        elif self.grid[newPosition] == ".":
            robot.updateRobotPosition(newPosition, True)
            robot.position = newPosition
            self.grid[oldPosition] = " "
            return True

        elif self.grid[newPosition] == "O":
            return False

        # TODO Put this elsewhere
        elif self.grid[newPosition] == "U":
            robot.updateRobotPosition(newPosition, False)
            self.grid[newPosition] = "X"
            self.grid[oldPosition] = " "
            self.won = True
            return True

        elif self.grid[newPosition] == "X":
            return False

        elif robot.robotInDoor:
            robot.updateRobotPosition(newPosition, False)
            self.grid[newPosition] = "X"
            self.grid[oldPosition] = "."
            return True
