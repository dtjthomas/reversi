# reversi.py

# reversi board game with modified rules

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


    def playGame(self):
        while self.player1.canMove() or self.player2.canMove():
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
        decision = input("Invalid input. Please try again.")
    
    board = Board()
    if decision == "f":
        player1 = Person("blue", board)
        player2 = Person("red", board)
    else:
        player1 = Person("blue", board)
        player2 = Bot("red", board)

    game = Game(player1, player2, board)
    game.playGame()
    


if __name__ == "__main__":
    main()
