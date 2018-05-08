# -*-coding:Utf-8 -*

"""This file contains the server source code of the game Roboc.

The game is a multiplayer PVP maze of obstacles: walls that are simply there to
slow you down, doors that can be crossed and at least one point through which
you can leave the labyrinth. If one of the robots arrives at this point, the
game is considered won. The robots can also create doors, or block them"""

import os
import socket
import select
import time
import pdb

from map import Map
from helpers import *
from labyrinth import *
from player import *
from robot import *

os.system("clear")

host = ""
port = 15008

maps = []
currentGameLabyrinth = {}


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
        print("{} - {}".format(i+1, map_.name))
        mapNumbers.append(i)

    # Prompt the user to choose the map to play from the list of available maps
    choiceInt = -1
    while choiceInt not in mapNumbers:
        choice = input("Please choose the game map by entering" +
                       " the corresponding number: ")
        try:
            choiceInt = int(choice) - 1
        except ValueError:
            print("Not a valid choice.")

    return choiceInt


def createConnection():
    """This funcion opens a connection through a TCP socket"""

    connection = socket.socket()
    connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    connection.bind((host, port))
    connection.listen(5)
    print("The server is listening at port {}".format(port))
    global serverLaunched
    serverLaunched = True
    return connection


def closeConnections(clientsConnected):
    """This function closes all connections with all clients"""

    for client in clientsConnected:
        client.send("close".encode())
        client.close()


def acceptConnections(clientsConnected, connection):
    global currentGameLabyrinth

    # Listen on the main connection for clients, and add them to the
    # pending connection list to be accepted
    requestedConnections, wlist, xlist = select.select([connection], [],
                                                       [], 0.05)
    for connection in requestedConnections:
        connectionWithClient, connectionInfo = connection.accept()
        print("{} joined.".format(connectionInfo))

        # Add the pending connections to the accepted connection list
        clientsConnected.append(connectionWithClient)

        # Create the robot that corresponds to this player
        player = Player(connectionWithClient)
        if currentGameLabyrinth:
            robot = Robot(currentGameLabyrinth.getEmptySpaces(), player)

            # Add the robot to the currentGameLabyrinth
            currentGameLabyrinth.addRobot(robot)

    # Listen to the connected clients. The clients returned by select are
    # the ones to be read (recv). Wait for 50 ms. Lock te call to
    # select.select in a try block. If the list of connected clients is
    # empty, an exception is raised
    if len(clientsConnected) >= 2:
        clientsToRead = []
        try:
            clientsToRead, wlist, xlist = select.select(clientsConnected, [],
                                                        [], 0.05)
        except select.error:
            pass

        # Go through the list of clients to read and check for the start game
        # command 'c'. If a client sends the start command, the server proceeds
        # to the labyrinth selection
        else:
            for client in clientsToRead:
                msgReceived = client.recv(1024)
                msgReceived = msgReceived.decode()
                if msgReceived == "c":

                    # The game starts.
                    for client in clientsConnected:
                        client.send("start".encode())
                    return False
    return True


def handleClientCommand(robot, command):
    """This function handles the command sent by client. It checks what it is
    and updates the labyrinth accordingly. The command validation is made in
    the client side"""

    global currentGameLabyrinth
    x, y = robot.position
    maxX, maxY = currentGameLabyrinth.getLabyrinthSize()

    if command == "s":
        x += 1
    elif command == "n":
        x -= 1
    elif command == "e":
        y += 1
    elif command == "w":
        y -= 1
    elif command[0] == "p":
        # Create a door in a wall
        direction = command[1]
        a, b = robot.position
        if direction == "s":
            a += 1
        elif direction == "n":
            a -= 1
        elif direction == "e":
            b += 1
        elif direction == "w":
            b -= 1

        # Check if the position to change is not a map border
        if a > 0 and a < maxX and b < maxY and b > 0:
            # Check if there's a wall to door in the place the user wanted
            if currentGameLabyrinth.grid[(a, b)] == "O":
                currentGameLabyrinth.grid[(a, b)] = "."
                return True
            else:
                return False
        else:
            return False
    elif command[0] == "m":
        # Create a wall in a door
        direction = command[1]
        a, b = robot.position
        if direction == "s":
            a += 1
        elif direction == "n":
            a -= 1
        elif direction == "e":
            b += 1
        elif direction == "w":
            b -= 1

        # Check if the position to change is not a map border
        if a > 0 and a < maxX and b < maxY and b > 0:

            # Check if there's a door to wall in the place the user wanted
            if currentGameLabyrinth.grid[(a, b)] == ".":
                currentGameLabyrinth.grid[(a, b)] = "O"
                return True
            else:
                return False
        else:
            return False
    # Check if the movement is valid and return True or False
    valid = currentGameLabyrinth.checkRobotMovement(robot, (x, y))
    return valid


def sendLabyrinthToAll():
    """This function sends the current labyrinth to all clients"""

    global currentGameLabyrinth

    for robot in currentGameLabyrinth.robots:

        # Update the robot display to be uppercase for the player's robot.
        # If the robot is in a door, don't update the display because it
        # becomes invisible
        if not robot.robotInDoor:
            currentGameLabyrinth.grid[robot.position] = "X"
            msgSent = "map" + str(currentGameLabyrinth)
            robot.player.connection.send(msgSent.encode())
            currentGameLabyrinth.grid[robot.position] = "x"
        else:
            msgSent = "map" + str(currentGameLabyrinth)
            robot.player.connection.send(msgSent.encode())


def sendDefeatToLosers(robot_):
    """This functions sends a msg to all users who lost, saying they lost"""

    global currentGameLabyrinth
    for robot in currentGameLabyrinth.robots:
        if robot_ != robot:
            robot.player.connection.send("lost".encode())


def main():
    """This funcion  defines the main game flow."""

    clientsConnected = []
    global currentGameLabyrinth

    # Setup the game
    mainConnection = createConnection()
    loadMaps()

    # Ask the server to choose the map, and use the choice to
    # define the current game map
    currentGameLabyrinth = maps[chooseMap()].labyrinth

    # Accept client connections while no one starts the game
    waitingForPlayers = True
    print("Waiting for at least 2 players to join...")
    while waitingForPlayers:
        waitingForPlayers = acceptConnections(clientsConnected,
                                              mainConnection)

    # Send the updated Laybrinth to all players
    sendLabyrinthToAll()

    # Loop through the connected players and, for each one, get the sent
    # command and handle it to check what to do
    while True:

        for robot in currentGameLabyrinth.robots:

            # Try to get a valid command from the client while it's his turn.
            # If the command is accepted, process it, update the labyrinth and
            # go to the next player
            nextPlayer = False
            client = robot.player.connection

            while not nextPlayer:

                # Tell the player it's his turn
                client.send("go".encode())

                # Get the user response
                msgReceived = client.recv(1024)
                msgReceived = msgReceived.decode()
                nextPlayer = handleClientCommand(robot, msgReceived)

            # Send the updated Laybrinth to all players
            sendLabyrinthToAll()

        # Check if someone has won
        if currentGameLabyrinth.won:
            client.send("won".encode())
            sendDefeatToLosers(robot)
            break

    # Close all connections
    print("Closing all connections...")
    closeConnections(clientsConnected)
    mainConnection.close()


if __name__ == "__main__":
    main()
