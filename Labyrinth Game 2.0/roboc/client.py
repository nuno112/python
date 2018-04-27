# -*-coding:Utf-8 -*
"""This module contains the client code. This code communicates with the server
through a TCP socket. Sends the command inputed by the player, and receives
the labyrinth string to display"""

from player import *
import socket
import select

host = "localhost"
port = 13000


def connect():
    """This function creates a connection to the server through a TCP socket"""

    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.connect((host, port))
    print("Conection established with the server ate port {}".format(port))
    return connection


def main():
    playing = True
    print(("Hello! Welcome to Labyrinth Game 2.0. Please wait while we connect"
           "you to our server!"))
    connectionToServer = connect()
    while playing:
        msgReceived = connectionToServer.recv(1024)
        msgReceived = msgReceived.decode()

        # If the server send the msg 'go', it means it's this client's turn
        # and it is expecting an answer (the command inputed by the player)
        # If the message is 'end' the game is over
        if msgReceived[0:2] == "go":
            print(msgReceived[2:])
            move = getUserMove()
            connectionToServer.send(move.encode())
        elif msgReceived == "end":
            connectionToServer.close()
        else:
            print(msgReceived)


def getUserMove():
    """ This function prompts the user for a letter and returns it, to
    determine action to take. If the user inputs a number after the letter,
    the robot move that amount until it hits an obstacle, or not. """

    move = ""

    # TODO add the wall door and build door functionality

    # Ask the user for a command to move the robot
    while move[0] not in ("s", "n", "e", "w"):
        move = input("Where do you want to move? (S)outh, (N)orth, " +
                     "(E)ast, (W)est, or (Q)uit:  ")
        print("\n")
        move.lower()
    return move

    # Put this in the server
    """
    # Check if user wants to advance several blocks (direction followed by
    # a number)
    if len(move) > 1:
        moveDirection = move[0]
        try:
            moveAmount = int(move[1:])
        except ValueError:
            print("Not a valid move amount.")
    else:
        moveDirection = move """
