# -*-coding:Utf-8 -*
"""This module contains the client code. This code communicates with the server
through a TCP socket. Sends the command inputed by the player, and receives
the labyrinth string to display"""

import socket
import select
import time
import re
import os

from threading import *

os.system("clear")

host = "localhost"
port = 15008
playing = False
remainingMove = []
command = ""
displayLock = RLock()
myTurn = False
gameOver = False


def isValidCommand(c):
    """Check if a command is valid"""
    s = "^['N','S','E','W']\d*$|^P['N','S','E','W']$|^M['N','S','E','W']$"
    x = re.match(s, c.upper())
    return x is not None


def connect():
    """This function creates a connection to the server through a TCP socket"""

    connection = socket.socket()
    connection.connect((host, port))
    print("Connection established with the server at port {}".format(port))
    return connection


def addMove(command):
    """This function expands the command entered
    i.e. 's3' becomes ['s', 's', 's']"""

    global remainingMove
    if command[0].upper() in ('N', 'S', 'E', 'O'):
        if len(command) > 1:
            rep = int(command[1:])
            for i in range(rep):
                remainingMove.append(command[0].lower())
        else:
            remainingMove.append(command[0].lower())
    else:
        # If it's a command to create/destroy a wall then add it directly
        remainingMove.append(command.lower())


def getServerResponse():
    global playing
    global myTurn
    global command
    global connectionToServer
    global gameOver
    global remainingMove

    while True:

        # If the game is over, terminate the thread
        if gameOver:
            return

        # Receive a message from the server
        msgReceived = connectionToServer.recv(1024)
        msgReceived = msgReceived.decode()

        if msgReceived == "start":
            print("\nGame has started.")
            playing = True
            myTurn = False

        # If the server sends map, the message is the updated labyrinth
        # to display
        if msgReceived[0:3] == "map":
            myTurn = False
            with displayLock:
                if "go" in msgReceived:
                    print("\n" + msgReceived[3:-2])
                else:
                    print("\n" + msgReceived[3:])

        # If the server send the msg 'go', it means it's this client's turn
        # and it is expecting an answer (the command inputed by the player)
        if "go" in msgReceived:
            playing = True
            myTurn = True
            print("It's your turn, please make a move: ", flush=True)

            # Check if there are buffered commands (i.e. user inputed 's3')
            if len(remainingMove) > 0:
                connectionToServer.send(remainingMove[0].encode())
                del(remainingMove[0])
            else:

                # Wait for the other thread if there is no command yet
                while command == "":
                    time.sleep(0.01)
                addMove(command)
                connectionToServer.send(remainingMove[0].encode())
                del(remainingMove[0])
                myTurn = False
                command = ""

        # If the message is won, then another player has won
        elif "won" in msgReceived:
            print("\nYou won!! GG\n")

        # If the message is lost, then another player has lost
        elif "lost" in msgReceived:
            print("\nYou lost...\n")

        # If the server sends close, the game is over and connections
        # are closing
        if "close" in msgReceived:
            connectionToServer.close()
            gameOver = True


def getUserMove():
    """ This function prompts the user for a letter and returns it, to
    determine action to take. If the user inputs a number after the letter,
    the robot move that amount until it hits an obstacle, or not. """

    move = ""
    global playing
    global command
    global myTurn
    global gameOver

    while True:

        # If the game is over, terminate the thread
        if gameOver:
            return

        with displayLock:
            if not playing:
                print("Enter C to start the game: ", end="", flush=True)
            elif myTurn:
                print("It's your turn, please make a move: ", flush=True)
            else:
                print("It isn't your turn yet, please wait", flush=True)

        move = input()

        # If the game hasn't started yet send command immediately to server
        if not playing:
            connectionToServer.send(move.encode())
        elif myTurn:

            # Check if the command is valid, and if so, set it to the command
            # to send to the server
            if (isValidCommand(move)):
                command = move.lower()

                # Wait for command to be handled by the other thread
                while command != "":
                    time.sleep(0.01)


if __name__ == "__main__":
    connectionToServer = connect()

    # Start 2 threads: one to get user's input, other to communicate with srvr
    getUserMoveThread = Thread(target=getUserMove)
    getServerResponseThread = Thread(target=getServerResponse)

    getServerResponseThread.start()
    getUserMoveThread.start()

    # wait till the end of the game
    getServerResponseThread.join()
