# -*-coding:Utf-8 -*


from player import *
import socket
import select

host = "localhost"
port = 13000


def connect():
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.connect((host, port))
    print("Conection established with the server ate port {}".format(port))
    return connection


def main():
    print(("Hello! Welcome to Labyrinth Game 2.0. Please wait while we connect"
           "you to our server!"))
    connectionToServer = connect()
    move = getUserMove()
    connectionToServer.send(move.encode())


def getUserMove():
    """ This function prompts the user for a letter and returns it, to
    determine action to take. If the user inputs a number after the letter,
    the robot move that amount until it hits an obstacle, or not. """

    move = ""

    # TODO add the wall door and build door functionality

    # Ask the user for a command to move the robot or quit
    while move[0] not in ("p", "m" "s", "n", "e", "w"):
        move = input("Where do you want to move? (S)outh, (N)orth, " +
                     "(E)ast, (W)est, or (Q)uit:  ")
        print("\n")
        move.lower()

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

    return move
