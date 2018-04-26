# -*-coding:Utf-8 -*

"""This file contains helper functions"""
import pickle


def mapTextToGrid(text):
    """Transform the text into a usable labyrinth grid"""

    lines = text.split("\n")
    lineLength = len(lines[0])
    grid = [["" for x in range(lineLength)] for y in range(len(lines))]
    for i, line in enumerate(lines):
        for j, char in enumerate(line):
            if char != "\n":
                grid[i][j] = char
    return grid


def writeSaveData(labyrinth):
    """Save the game data (map object) as an object to a file"""

    with open("savedata/save.dat", "wb") as file:
        myPickler = pickle.Pickler(file)
        myPickler.dump(labyrinth)


def readSaveData():
    """Read the saved game data from the file"""

    with open("savedata/save.dat", "rb") as file:
        myPickler = pickle.Unpickler(file)
        data = myPickler.load()
        return data
