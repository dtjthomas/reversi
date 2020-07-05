# reversi.py

# reversi board game with modified rules

import socket
from board import *
from player import *


class Game:
    """Encapsulates all relevant data and functionality for playing reversi"""
    def __init__(self, player1, player2, board):
        self.player1 = player1
        self.player2 = player2
        self.currentPlayer = player1
        self.board = board

    def nextPlayer(self):
        if self.currentPlayer == self.player1:
            self.currentPlayer = self.player2
        else:
            self.currentPlayer = self.player1


    def gameIsOver(self):
        if self.player1.canMove() or self.player2.canMove():
            return False
        else:
            return True

    def playGame(self):
        while not self.gameIsOver():
            self.currentPlayer.takeTurn()
            self.nextPlayer()
        self.board.output()
        self.finalScoring()

    def finalScoring(self):
        player1Score = self.player1.getScore()
        player2Score = self.player2.getScore()
        print(self.player1.playerColor + " had " + str(player1Score) + " points, " + \
            self.player2.playerColor + " had " + str(player2Score) +" points.")
        if player1Score == player2Score:
            print("Tie")
        elif player1Score > player2Score:
            print(self.player1.playerColor + " wins")
        else:
            print(self.player2.playerColor + " wins")
        quit()

    def hostGame(self):
        HOST = input("Please enter your local IP:\n")
        PORT = 65432
        print("You are blue")
        print("Waiting for other player to join...")

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen()
            connection, address = s.accept()
            print("Connection established")
            with connection:
                while not self.gameIsOver():
                    if self.currentPlayer.isHost:
                        decision = self.currentPlayer.takeTurn()
                        if decision is None:
                            connection.send(bytes("None", "utf-8"))
                        else:
                            connection.send(bytes(decision, "utf-8"))
                    else:
                        print("Waiting for " + self.currentPlayer.playerColor + " to take their turn")
                        clientDecision = connection.recv(1024)
                        clientDecision = clientDecision.decode("utf-8")
                        if clientDecision == "None":
                            print(self.currentPlayer.playerColor + " had to pass")
                        else:
                            self.currentPlayer.takeTurn(clientDecision)
                            print(self.currentPlayer.playerColor + " has placed a piece at " + clientDecision)
                    self.nextPlayer()
                self.finalScoring()
                    
    def connectToGame(self):
        HOST_IP = input("Please enter the local IP of the host: \n")
        HOST_PORT = 65432

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST_IP, HOST_PORT))
            print("You are red")
            while not self.gameIsOver():
                if not self.currentPlayer.isHost:
                    decision = self.currentPlayer.takeTurn()
                    if decision is None:
                        s.send(bytes("None", "utf-8"))
                    else:
                        s.send(bytes(decision, "utf-8"))
                else:
                    print("Waiting for " + self.currentPlayer.playerColor + " to take their turn")
                    hostDecision = s.recv(1024)
                    hostDecision = hostDecision.decode("utf-8")
                    if hostDecision == "None":
                        print(self.currentPlayer.playerColor + "had to pass ")
                    else:
                        self.currentPlayer.takeTurn(hostDecision)
                        print(self.currentPlayer.playerColor + " has placed a piece at " \
                        + hostDecision)
                self.nextPlayer()
            self.finalScoring()


            



def main():

    title = """\u001b[32m      ___           ___           ___           ___           ___           ___                 
     /\  \         /\  \         /\__\         /\  \         /\  \         /\  \          ___   
    /::\  \       /::\  \       /:/  /        /::\  \       /::\  \       /::\  \        /\  \  
   /:/\:\  \     /:/\:\  \     /:/  /        /:/\:\  \     /:/\:\  \     /:/\ \  \       \:\  \ 
  /::\~\:\  \   /::\~\:\  \   /:/__/  ___   /::\~\:\  \   /::\~\:\  \   _\:\~\ \  \      /::\__\ 
 /:/\:\ \:\__\ /:/\:\ \:\__\  |:|  | /\__\ /:/\:\ \:\__\ /:/\:\ \:\__\ /\ \:\ \ \__\  __/:/\/__/
 \/_|::\/:/  / \:\~\:\ \/__/  |:|  |/:/  / \:\~\:\ \/__/ \/_|::\/:/  / \:\ \:\ \/__/ /\/:/  /   
    |:|::/  /   \:\ \:\__\    |:|__/:/  /   \:\ \:\__\      |:|::/  /   \:\ \:\__\   \::/__/    
    |:|\/__/     \:\ \/__/     \::::/__/     \:\ \/__/      |:|\/__/     \:\/:/  /    \:\__\    
    |:|  |        \:\__\        ~~~~          \:\__\        |:|  |        \::/  /      \/__/    
     \|__|         \/__/                       \/__/         \|__|         \/__/                

    \u001b[0m"""       
    print(title)

    decision = input("Press [f] to play with a friend, press [b] to play against a bot\n")
    while decision != "f" and decision != "b":
        decision = input("Invalid input. Please try again.\n")
    
    board = Board()
    if decision == "f":
        decision2 = None
        while decision2 != "s" and decision2 != "h" and decision2 != "c":
            decision2 = input("Press [s] for playing on the same computer, [h] to host a game, " \
                +" or [c] to connect to a game \n")
            player1 = Person("blue", board)
            player2 = Person("red", board)
            game = Game(player1, player2, board)
        if decision2 == "h":
            game.player1.isHost = True
            game.player2.isHost = False
            game.hostGame()
        elif decision2 == "c":
            game.player1.isHost = True
            game.player2.isHost = False
            game.connectToGame()
        else:
            pass
    else:
        player1 = Person("blue", board)
        player2 = Bot("red", board)

    game = Game(player1, player2, board)
    game.playGame()
    


if __name__ == "__main__":
    main()
