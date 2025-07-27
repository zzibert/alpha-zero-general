'''
Author: Žan Žibert
Date: July 27, 2025.
Board class.
Board data:
  1=white, -1=black, 0=empty
  first dim is column , 2nd is row:
     pieces[1][7] is the square in column 2,
     at the opposite end of the board in row 8.
Squares are stored and manipulated as (x,y) tuples.
x is the column, y is the row.
'''

class Board():

    _white_starting_position = [16, 8]
    _black_starting_position = [0, 8]

    # list of all directions on the board, as (x,y) offsets
    _directions = [
        (0, 2),     # Right
        (0, 4),     # Right-Jump
        (-2, 2),    # Right-Jump-Up
        (2, 2)      # Right-Jump-Down

        (2, 0),      # Down
        (4, 0),     # Down-Jump
        (2, -2),    # Down-Jump-Left
        (2, 2),     # Down-Jump-Right

        (0, -2)     # Left
        (0, -4),    # Left-Jump
        (-2, -2),   # Left-Jump-Up
        (2, -2),    # Left-Jump-Down

        (-2, 0),    # Up
        (-4, 0),    # Up-Jump
        (-2, -2),   # Up-Jump-Left
        (-2, 2),    # Up-Jump-Right
    ]

    def __init__(self, n):
        "Set up initial board configuration."

        self.n = n
        # Create the empty board array
        self.pieces = [None]*self.n
        for i in range(self.n):
            self.pieces[i] = [0]*self.n

        # Set up the initial black and white piece
        