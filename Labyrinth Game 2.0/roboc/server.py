# -*-coding:Utf-8 -*

"""This file contains the server source code of the game Roboc.

The game is a multiplayer PVP maze of obstacles: walls that are simply there to
slow you down, doors that can be crossed and at least one point through which
you can leave the labyrinth. If one of the robots arrives at this point, the
game is considered won. The robots can also create doors, or block them"""

import os
import socket
import select

from map import Map
from helpers import *
from labyrinth import *


host = ""
port = 13000
serverLaunched = False

maps = []

# Add players (Player class) which has the connection info for a certain player
# Associate the players to each robot, then cycle through robot list to check
# which robot belongs to the current player sending info, and change the robot
# accordingly
players = []


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


def createConnection():
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.bind((host, port))
    connection.listen(5)
    print("The server is listening at port {}".format(port))
    serverLaunched = True
    return connection


def closeConnections(clientsConnected):
    for client in clientsConnected:
        client.close()


# main game flow
def main():

    clientsConnected = []
    # Setup the game
    mainConnection = createConnection()
    loadMaps()
    while serverLaunched:

        # Listen on the main connection for clients, and add them to the
        # pending connection list to be accepted
        requestedConections, wlist, xlist = select.select([mainConnection], [],
                                                          [], 0.05)
        for connection in requestedConections:
            connectionWithClient, connectionInfo = connection.accept()

            # Add the pending connections to the accepted connection list
            clientsConnected.append(connectionWithClient)

        # Listen to the connected clients. The clients returned by select are
        # the ones to be read (recv). Wait for 50 ms. Lock te call to
        # select.select in a try block. If the list of connected clients is
        # empty, an exception is raised
        clientsToRead = []
        try:
            clientsToRead, wlist, xlist = select.select(clientsConnected, [],
                                                        [], 0.05)
        except select.error:
            pass
        else:
            # Go through the list of clients to read
            for client in clientsToRead:
                msgReceived = client.recv(1024)
                msgReceived = msgReceived.decode()

    # ask the user to choose te map, and use the choice to define the
    # current game map
    currentGameLabyrinth = maps[chooseMap()].labyrinth

    # This loop defines the main game flow, by getting the user input,
    # and moving the robot accordingly
    moveDirection = ""
    while moveDirection is not "q":
        print(currentGameLabyrinth)

        # TODO change this to accept data from the client through TCP
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

            # Check if the user has reached the goal and
            # updateRobotPosition
            win = currentGameLabyrinth.updateRobotPosition((x, y))
            if win:
                print(currentGameLabyrinth)
                print("You won! Congratulations!")
                moveDirection = "q"
                break
            moveAmount -= 1

    # Close all connections
    print("Closing all connections...")
    closeConnections(clientsConnected)
    mainConnection.close()


if __name__ == "__main__":
    main()
