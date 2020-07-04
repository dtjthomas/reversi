# Reversi
## Installation: 
1. Clone the repository \
        `git clone https://github.com/dtjthomas/reversi.git`
2. Run the script \
    `python3 reversi.py`

## How to play:
### Overview:
Reversi is played with two colors (in this case, blue and red). 
### Objective:
The object of the game is to have to most amount of your color pieces on the board when the game ends.
### Taking Turns
Each player will take their turn placing one of their given pieces on the board. The piece must be placed such that it sandwiches at least one opposing colored piece in at least one of eight directions (up,left,right, down, diagonals). When an opposing piece (or pieces) is sandwiched between the newly placed piece and another piece of the current player's color, flip all opposing piece in that given color such that they are now the color of the current player.
### Ending
The game ends when the board is filled or both players have no valid moves. Add the amount of pieces for both players and compare.


For more information, check out: https://www.youtube.com/watch?v=Ol3Id7xYsY4