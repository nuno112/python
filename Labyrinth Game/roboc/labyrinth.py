# -*-coding:Utf-8 -*

"""This module contains the class Labyrinth"""


class Labyrinth:
    """Class that represents a labyrinth"""

    def __init__(self, grid):
        self.grid = grid
        self.robotPosition = [(ix, iy) for ix, row in enumerate(self.grid)
                              for iy, i in enumerate(row) if i == "X"][0]
        self.robotInDoor = False

    def __repr__(self):
        text = ""
        for i, line in enumerate(self.grid):
            for j, char in enumerate(line):
                text += char
            text += "\n"
        return text

    def updateRobotPosition(self, newPosiion):
        """This method tries to update the robot possition, and depending
        on the placed position, it is allowed or not. It also checks if the
        robot as reached the end of the labyrinth and thus, won"""

        oldPosition = self.robotPosition
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
