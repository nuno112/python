# -*-coding:Utf-8 -*

import unittest
import sys
import socket
import select
sys.path.insert(0, "/home/pce/workspace/python/Labyrinth Game 2.0/roboc/")

from labyrinth import *
from robot import *
from helpers import *
from server import *
from client import *


class NetworkingTest(unittest.TestCase):
    """This class has methods for unittesting the
    networking part of the game"""

    def setUp(self):
        self.clientsConnected = []
        self.mainConnection = createConnection()
        self.clientConnection = connect()
        reqConnections, wlist, xlist = select.select([self.mainConnection], [],
                                                     [], 0.05)
        for connection in reqConnections:
            self.connectionWithClient, connectionInfo = connection.accept()

    def test_serverCreation(self):
        self.assertIsInstance(self.mainConnection, socket.socket)

    def test_serverAcceptsClients(self):
        self.assertTrue(acceptConnections(self.clientsConnected,
                                          self.mainConnection))

    def test_clientConnecting(self):
        acceptConnections(self.clientsConnected, self.mainConnection)
        self.assertIsInstance(self.clientConnection, socket.socket)

    def test_serverMessagesClient(self):
        self.connectionWithClient.send(b"test")
        self.msgReceived = self.clientConnection.recv(1024)
        self.assertEqual(b"test", self.msgReceived)

    def test_clientMessagesServer(self):
        self.clientConnection.send(b"test")
        self.msgReceived = self.connectionWithClient.recv(1024)
        self.assertEqual(b"test", self.msgReceived)

    def test_closeConnections(self):
        self.mainConnection.close()
        with self.assertRaises(OSError):
            self.mainConnection.send(b"test")

    def tearDown(self):
        self.mainConnection.close()
        self.connectionWithClient.close()
        self.clientConnection.close()


unittest.main(exit=False)
