# player.py

# represents the actions the player has available

from board import *

class Player:
    def __init__(self, color, board):
        self.playerColor = color
        self.board = board # reference to the shared board

    def takeTurn(self):
        pass

    def getValidMoves(self):
        return self.board.getValidMoves(self.playerColor)

    def placePiece(self, position):
        self.board.placePiece(position, self.playerColor)

    def canMove(self):
        if len(self.board.getValidMoves(self.playerColor)) != 0:
            return True
        else:
            return False
        
    def getScore(self):
        return self.board.currentScore(self.playerColor)



class Bot(Player):
    """Bot strategy is implemented using a greedy algorithm by always placing a tile
    that will locally maximize the amount of tiles flipped for a given turn.


    Note: This bot would have "easy" difficulty as it doesn't calculate the importance
    of corners into its strategy or set up for future (better) moves.
    
    """
    def __init__(self, color, board):
        self.playerColor = color
        self.board = board 

    def takeTurn(self):
        bestMove = self.board.getBestMove(self.playerColor)
        if bestMove == None:
            print(self.playerColor + " had to pass. No valid moves.")
        else:
            self.placePiece(bestMove)
            print(self.playerColor + " placed a tile at " + bestMove)

class Person(Player):
    def __init__(self, color, board):
        self.playerColor = color
        self.board = board
    
    """Represents human players"""
    def takeTurn(self, validMove=None):

        # used for updated players board for online play
        if validMove != None:
            self.placePiece(validMove)
            return

        self.board.output()
        columns = "ABCDEFGH"
        validMoves = self.getValidMoves()
        if len(validMoves) == 0:
            print("Your turn is skipped. You have no possible moves")
            return None
        else:
            while True:
                try:
                    decision = input(self.playerColor + "'s turn. Please enter a position [Col, Row], see [v]alid positions," \
                    + " or [q]uit.\n")
                    if decision == "q":
                        quit()
                    elif decision == "v":
                        print(validMoves)
                    elif len(decision) == 2 and decision[0] in columns and int(decision[1]) > 0 and \
                        int(decision[1]) < 9:
                        self.placePiece(decision)
                        self.board.output()
                        return decision
                    else:
                        print("Your input is not a position [Col, Row], see [v]alid moves or" + \
                        "[q]uit\n")
                except invalidPlacementError:
                    print("Invalid move.\n")
                    continue

    