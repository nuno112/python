# -*-coding:Utf-8 -*

"""This file contains helper functions"""


def mapTextToGrid(text):
    """Transform the text into a usable labyrinth grid"""

    lines = text.split("\n")
    lineLength = len(lines[0])
    grid = {}
    for i, line in enumerate(lines):
        for j, char in enumerate(line):
            if char != "\n":
                grid[(i, j)] = char
    return grid
