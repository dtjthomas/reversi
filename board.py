# board.py

# represents the assets needed to play Reversi

class pieceError(Exception):
    def __init__(self, column, row):
        self.column = column
        self.row = row

class Tile:
    """Represents a given tile in the game, with the ability to place tiles and 
    flip them. Columns = characters A-H, rows = integers 1-8"""

    def __init__(self, col, row, color="empty"):
        if col > 7 or col < 0 or row > 7 or row < 0:
            raise pieceError
        self.color = color
        self.col = col
        self.row = row

        
    def oppositeColor(self):
        if self.color == "red":
            return "blue"
        elif self.color == "blue":
            return "red"
        else:
            return None

    def flip(self):
        """Throws a pieceError exception if the tile doesn't have a piece"""
        if self.color != "empty":
            self.color = self.oppositeColor()
        else:
            raise pieceError(self.col, self.row)

    def output(self, width):
        if self.color == "empty":
            print("\u001b[42m \u001b[0m", end = width)
        elif self.color == "blue":
            print("\u001b[44m \u001b[0m", end = width)
        else:
            print("\u001b[41m \u001b[0m", end = width)


class offBoardError(Exception):
    pass

class invalidPlacementError(Exception):
    def __init__(self, col, row):
        self.position = str(col) + str(row)

class Board:    
    """Represents the 8 by 8 grid of tiles. With Outside array = column, inside
    nested array = row
    
    E = empty tile
    W = white piece
    B = black piece
    """
    
    def __init__(self):
        """Initializes the board where the first four tokens have been played."""

        self._length = 8
        self.board = []
        self.columns = "ABCDEFGH"
        for colNum in range(0, self._length):
            self.board.append([])
            for rowNum in range(0, self._length):
                self.board[colNum].append(Tile(colNum, rowNum))

        self.board[3][3].color = "blue"
        self.board[3][4].color = "red"
        self.board[4][3].color = "red"
        self.board[4][4].color = "blue"


    # not sure if I could package this into a large string and use __str__ instead
    def output(self):
        """Returns the current board and location of pieces"""
        width = "      " # 6 spaces formatting
        print("\n\n")
        for row in range(self._length, -1, -1):
            if row != 0:
                print(row, end = width)
                for col in range(0, self._length):
                    #print(self.board[col][row - 1], end = width)
                    self.board[col][row-1].output(width)
                print("\n\n")
            else:
                print(width, end=" ")
                for col in self.columns:
                    print(col, end = width)
        print("\n\n")

    # used for testing
    def getTile(self, position):
        """Returns a refernece to the tile at position. Requires the 
        form [Column letter][Row num]"""
        columns = "ABCDEFGH"
        if not position[0] in columns or not position[1].isdigit():
            raise invalidPlacementError
        return self.board[columns.find(position[0])][int(position[1]) - 1]

    def indexToPosition(self, col, row):
        """Returns a string in the user format from the set of indices used to traverse the board
        Ex: indexToPosition(2, 5) -> \"C6\"
        """
        columns = "ABCDEFGH"
        return columns[col] + str(row + 1)

    def up(self, col, row):
        if row == self._length - 1:
            raise offBoardError
        else:
            return self.board[col][row + 1]


    def down(self, col, row):
        if row == 0:
            raise offBoardError
        else:
            return self.board[col][row - 1]

    def left(self, col, row):
        if col == 0:
            raise offBoardError
        else:
            return self.board[col - 1][row]

    def right(self, col, row):
        if col == self._length - 1:
            raise offBoardError
        else:
            return self.board[col + 1][row]

    def diagUpLeft(self, col, row):
        if col == 0 or row == self._length - 1:
            raise offBoardError
        else:
            return self.board[col - 1][row + 1]

    def diagUpRight(self, col, row):
        if col == self._length - 1 or row == self._length - 1:
            raise offBoardError
        else:
            return self.board[col + 1][row + 1]

    def diagDownLeft(self, col, row):
        if col == 0 or row == 0:
            raise offBoardError
        else:
            return self.board[col - 1][row - 1]

    def diagDownRight(self, col, row):
        if col == self._length - 1 or row == 0:
            raise offBoardError
        else:
            return self.board[col + 1][row - 1]



    directions = [up, down, left, right, diagUpLeft, diagUpRight, \
        diagDownLeft, diagDownRight]


    def flankingDirections(self, col, row, playerColor):
        """Returns a list of directions in which a given piece outflanks/sandwiches opposing color pieces"""
        flankingDirections = []
        for direction in self.directions:
            try:
                adjacent = direction(self, col, row)
                if adjacent.color != playerColor and adjacent.color != "empty":
                    while True:
                        colNext = adjacent.col
                        rowNext = adjacent.row
                        adjacent = direction(self, colNext, rowNext)
                        if adjacent.color == playerColor:   # successfully flanked opposing piece
                            flankingDirections.append(direction)
                            break
                        if adjacent.color == "empty":
                            break
                else:
                    continue
            except offBoardError:
                continue
        return flankingDirections

    def getValidMoves(self, playerColor):
        """Returns a list of all valid moves for a given color"""
        validMoves = []
        for col in range(0, 8):
            for row in range(0, 8):
                if self.board[col][row].color != "empty":
                    continue
                if len(self.flankingDirections(col, row, playerColor)):
                    validMoves.append(self.indexToPosition(col,row))
        return validMoves

    def getBestMove(self, playerColor):
        """Returns the \"best\" placement by locally maximizing the number of opposing pieces flipped.
        In the case of a tie, it will return the piece closest in order of left to right bottom to top."""
        moves = self.getValidMoves(playerColor)
        movesAndFlips = {}
        columns = "ABCDEFGH"

        for move in moves:
            # initialize dictionary, python dictionaries don't value initialize like c++ maps
            movesAndFlips[move] = 0
            originalCol = columns.index(move[0])
            originalRow = int(move[1]) - 1
            placementDirections = self.flankingDirections(originalCol, originalRow, playerColor)
            for direction in placementDirections:
                col = originalCol
                row = originalRow
                while True:
                    try:
                        adjacent = direction(self, col, row)
                        if adjacent.color != "empty" and adjacent.color != playerColor:
                            movesAndFlips[move] += 1
                            col = adjacent.col
                            row = adjacent.row
                        else:
                            break
                    except offBoardError:
                        continue
                

        maxFlips = 0
        bestMove = None
        for possibleMove in moves:
            if movesAndFlips[possibleMove] > maxFlips:
                bestMove = possibleMove
                maxFlips = movesAndFlips[possibleMove]

        return bestMove


    def currentScore(self, playerColor):
        """Returns the number of pieces a player of a given color has on the board"""
        total = 0
        for col in range(0, 8):
            for row in range(0, 8):
                if self.board[col][row].color == playerColor:
                    total+=1
        return total


    def placePiece(self, position, playerColor):
        """Places a piece at [col][row] according to the player's color and performs all necessary 
        flips in all 8 directions"""

        columns = "ABCDEFGH"
        originalCol = columns.find(position[0])
        originalRow = int(position[1]) - 1

        if (len(self.flankingDirections(originalCol, originalRow, playerColor))) and \
            (position in self.getValidMoves(playerColor)):
            col = originalCol
            row = originalRow
            self.board[col][row].color = playerColor
            for direction in self.flankingDirections(col, row, playerColor):
                # need to reset col & row or iterating to the next direction
                # will result in starting in a tile that was not the original position
                col = originalCol
                row = originalRow
                while True:
                    try:
                        adjacent = direction(self, col, row)
                        if adjacent.color == "empty" or adjacent.color == \
                        playerColor:
                            break
                        else:
                            adjacent.flip()
                            col = adjacent.col
                            row = adjacent.row
                    except offBoardError:
                        break

        else:
            raise invalidPlacementError(originalCol, originalRow)

