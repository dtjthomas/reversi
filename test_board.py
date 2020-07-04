import unittest
from board import *


class TestTile(unittest.TestCase):
    def test_tile_empty(self):
        emptyTile = Tile(0, 0)
        self.assertEqual(emptyTile.color, "empty")
        self.assertEqual(emptyTile.oppositeColor(), None)

        with self.assertRaises(pieceError):
            emptyTile.flip()

        #self.assertEqual("*", str(emptyTile))

    def test_tile_player_colors(self):
        blue = Tile(4,5, "blue")
        blue.flip()
        self.assertEqual(blue.color, "red")

# creates a starter board
class TestBoardSimple(unittest.TestCase):
    def setUp(self):
        self.board = Board()

    def test_getTile(self):
        tile = self.board.getTile("D4")
        self.assertEqual(tile.color, "blue")


    def test_indexToPosition(self):
        self.assertEqual(self.board.indexToPosition(3, 4), "D5")

    def test_up(self):
        self.assertEqual(self.board.up(4,3), self.board.getTile("E5"))
        self.assertEqual(self.board.up(7,4), self.board.getTile("H6"))

        with self.assertRaises(offBoardError):
            self.board.up(4,7)

    def test_down(self):
        self.assertEqual(self.board.down(4,3), self.board.getTile("E3"))
        self.assertEqual(self.board.down(7,4), self.board.getTile("H4"))

        with self.assertRaises(offBoardError):
            self.board.down(5,0)

    def test_left(self):
        self.assertEqual(self.board.left(4,3), self.board.getTile("D4"))
        self.assertEqual(self.board.left(7,4), self.board.getTile("G5"))

        with self.assertRaises(offBoardError):
            self.board.left(0,2)

    def test_right(self):
        self.assertEqual(self.board.right(3,3), self.board.getTile("E4"))
        self.assertEqual(self.board.right(5,1), self.board.getTile("G2"))

        with self.assertRaises(offBoardError):
            self.board.right(7,5)

    def test_diagUpLeft(self):
        self.assertEqual(self.board.diagUpLeft(4,3), self.board.getTile("D5"))
        self.assertEqual(self.board.diagUpLeft(7,6), self.board.getTile("G8"))

        with self.assertRaises(offBoardError):
            self.board.diagUpLeft(0,0)

    def test_diagUpRight(self):
        self.assertEqual(self.board.diagUpRight(0,0), self.board.getTile("B2"))
        self.assertEqual(self.board.diagUpRight(3,6), self.board.getTile("E8"))

        with self.assertRaises(offBoardError):
            self.board.diagUpRight(0,7)

    def test_diagDownLeft(self):
        self.assertEqual(self.board.diagDownLeft(4,4), self.board.getTile("D4"))
        self.assertEqual(self.board.diagDownLeft(7,7), self.board.getTile("G7"))

        with self.assertRaises(offBoardError):
            self.board.diagDownLeft(0,0)

    def test_diagDownRight(self):
        self.assertEqual(self.board.diagDownRight(3,4), self.board.getTile("E4"))
        self.assertEqual(self.board.diagDownRight(0,7), self.board.getTile("B7"))

        with self.assertRaises(offBoardError):
            self.board.diagDownRight(7,0)

    def test_flankingDirections(self):
        directions = self.board.flankingDirections(3,2, "red")
        self.assertEqual(len(directions),1)
        self.assertEqual(directions[0], Board.up)

        directions = self.board.flankingDirections(6,5, "blue")
        self.assertEqual(directions, [])

        directions = self.board.flankingDirections(3, 5, "blue")
        self.assertEqual(directions, [Board.down])

    def test_getValidMoves(self):
        redValidMoves = self.board.getValidMoves("red")
        self.assertEqual(sorted(redValidMoves), sorted(["C4", "D3", "F5", "E6"]))

        blueValidMoves = self.board.getValidMoves("blue")
        self.assertEqual(sorted(blueValidMoves), sorted(["E3", "F4", "D6", "C5"]))
    
    def test_currentScore(self):
        self.assertEqual(self.board.currentScore("blue"), 2)

    def test_placePiece(self):
        self.board.placePiece("F5", "red")
        self.assertEqual(self.board.getTile("E5").color, "red")
        self.assertEqual(self.board.currentScore("red"), 4)
        self.assertEqual(self.board.currentScore("blue"), 1)




# creates a board that is several moves into the game
class TestBoardComplex(unittest.TestCase):
    def setUp(self):
        self.board = Board()
        #self.board.output()
        self.board.placePiece("E3", "blue")
        #self.board.output()
        self.board.placePiece("F3", "red")
        #self.board.output()
        self.board.placePiece("F4", "blue")
        #self.board.output()
        self.board.placePiece("F5", "red")
        #self.board.output()
        self.board.placePiece("G4", "blue")
        #self.board.output()
        self.board.placePiece("H5", "red")
        #self.board.output()

    def test_getTile(self):
        tile = self.board.getTile("F5")
        self.assertEqual(tile.color, "red")


    def test_flankingDirections(self):
        directions = self.board.flankingDirections(3, 2, "red")
        self.assertEqual(directions, [Board.up, Board.right, Board.diagUpRight])
        
        directions = self.board.flankingDirections(3, 2, "blue")
        self.assertEqual(directions, [])

    def test_getValidMoves(self):
        redValidMoves = self.board.getValidMoves("red")
        self.assertEqual(sorted(redValidMoves), sorted(["G3", "E2", "D3", "C4", "C3"]))

        blueValidMoves = self.board.getValidMoves("blue")
        self.assertEqual(sorted(blueValidMoves), \
        sorted(["C6", "D6", "E6", "F6", "G6", "H4", "G2", "F2", "G3"]))


    def test_getBestMove(self):
        # just used so that one has a majority (technically an illegal move)
        # when the bot uses getBestMove and there is a tie,
        # it won't really matter which the bot chooses
        self.board.getTile("C4").color = "blue"
        self.assertEqual(self.board.getBestMove("red"), "B4")
    
    def test_currentScore(self):
        self.assertEqual(self.board.currentScore("red"), 6)
        self.assertEqual(self.board.currentScore("blue"), 4)

    def test_placePiece(self):
        # technically illegal move, just using to determine 
        # if placepiece goes farther than 1 in either direction
        self.board.getTile("C4").color = "blue"
        self.board.placePiece("B4", "red")
        self.assertEqual(self.board.currentScore("blue"), 1)
        self.assertEqual(self.board.currentScore("red"), 11)
        self.assertEqual(self.board.getTile("E4").color, "red")

        with self.assertRaises(invalidPlacementError):
            self.board.placePiece("F6", "red")





if __name__ == "__main__":
    unittest.main()