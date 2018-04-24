# -*-coding:Utf-8 -*

"""This file contains the main source code of the game Roboc.

The game is a maze of obstacles: walls that are simply there to slow you down,
doors that can be crossed and at least one point through which you can leave
the labyrinth. If the robot arrives on this point, the game is considered won.
"""

import os

from map import Map
from helpers import *
from labyrinth import *

maps = []


def loadMaps():
    """This function loads the map files contained in the maps folder, and
    transforms the text into usable grids. The Maps objects created are saved
    in an array called maps"""

    # Load the existing maps
    for fileName in os.listdir("maps"):
        if fileName.endswith(".txt"):
            path = os.path.join("maps", fileName)
            mapName = fileName[:-4].lower()
            with open(path, "r") as file:
                content = file.read()

                # Creation of the map objects
                maps.append(Map(mapName, mapTextToGrid(content)))


def chooseMap():
    """This function asks the user to choose from the loaded list of maps"""

    # Display the loaded maps
    mapNumbers = []
    print("\nExisting labyrinths:\n")
    for i, map_ in enumerate(maps):
        print("{} - {}".format(i, map_.name))
        print(map_.labyrinth)
        mapNumbers.append(i)

    # Prompt the user to choose the map to play from the list of available maps
    choiceInt = -1
    while choiceInt not in mapNumbers:
        choice = input("Please choose the game map by entering" +
                       " the corresponding number: ")
        try:
            choiceInt = int(choice)
        except ValueError:
            print("Not a valid choice.")

    return choiceInt


def continueGame():
    """If there is a saved game, it will be displayed, and the user will be
    prompted to say if it wants to continue playing that game"""

    answer = ""

    # Check if the save file exists
    if "save.dat" in os.listdir("savedata"):
        labyrinth_ = readSaveData()

        # Check if there is a saved game, or if the save file is empty
        if isinstance(labyrinth_, Labyrinth):
            labyrinth_.updateRobotPosition(labyrinth_.robotPosition)
            print("There is a saved game: ")
            print(labyrinth_)

            # Ask user if he wants to continue the saved game
            while answer not in ("yes", "no", "y", "n"):
                answer = input("Do you wish to continue playing?" +
                               " (yes/no): ")
                answer.lower()
            if answer in ("yes", "y"):
                return (True, labyrinth_)
            else:
                return (False,)
        else:
            return (False,)
    else:
        return (False,)


def getUserMove():
    """ This function prompts the user for a letter and return it, to determine
    the action to take. If the user inputs a number after the letter, the robot
    will move that amount until it hits an obstacle, or not. """

    move = ""
    moveDirection = ""
    moveAmount = 1

    # Ask the user for a command to move the robot or quit
    while moveDirection not in ("q", "s", "n", "e", "w"):
        move = input("Where do you want to move? (S)outh, (N)orth, " +
                     "(E)ast, (W)est, or (Q)uit:  ")
        print("\n")
        move.lower()

        # Check if user wants to advance several blocks (direction followed by
        # a number)
        if len(move) > 1:
            moveDirection = move[0]
            try:
                moveAmount = int(move[1:])
            except ValueError:
                print("Not a valid move amount.")
        else:
            moveDirection = move
    return (moveDirection, moveAmount)


# main game flow
def main():

    # Setup the game and check if user wants to continue the saved game
    loadMaps()
    continueGameAnswer = continueGame()
    if continueGameAnswer[0]:
        currentGameLabyrinth = continueGameAnswer[1]
    else:

        # ask the user to choose te map, and use the choice to define the
        # current game map
        currentGameLabyrinth = maps[chooseMap()].labyrinth

    # This loop defines the main game flow, by getting the user input,
    # and moving the robot accordingly
    moveDirection = ""
    while moveDirection is not "q":
        print(currentGameLabyrinth)
        move = getUserMove()
        moveAmount = move[1]
        moveDirection = move[0]

        # Try to move moveAmount times
        while moveAmount > 0:
            x, y = currentGameLabyrinth.robotPosition
            if moveDirection == "s":
                x += 1
            elif moveDirection == "n":
                x -= 1
            elif moveDirection == "e":
                y += 1
            elif moveDirection == "w":
                y -= 1

            # Save the dat to a file
            writeSaveData(currentGameLabyrinth)

            # Check if the user has reached the goal and
            # updateRobotPosition
            win = currentGameLabyrinth.updateRobotPosition((x, y))
            if win:
                print(currentGameLabyrinth)
                print("You won! Congratulations!")
                moveDirection = "q"
                writeSaveData({})
                break
            moveAmount -= 1


if __name__ == "__main__":
    main()
