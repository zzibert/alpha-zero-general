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

from enum import Enum

class Position():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def isWithinBounds(self):
        self.x >= 0 & self.x < 17 & self.y >= 0 & self.y < 17

class RelativePosition():
    def __init__(self, dx, dy):
        self.dx = dx
        self.dy = dy

    def transform(self, position):
        return Position(
            x=position.x + self.dx,
            y=position.y + self.dy
        )
    
class DirectionCondition():
    def __init__(self, occupied, not_occupied, blocked, not_blocked):
        self.occupied = occupied
        self.not_occupied = not_occupied
        self.blocked = blocked
        self.not_blocked = not_blocked

    def is_condition_met(self, player_position, opponent_position, occupancy):
        raise NotImplementedError("Subclasses must implement move()")
    
    def is_direction_blocked(self, relative, player_position, occupancy):
        
        

        

class Direction():
    def __init__(self, name, relative_position):
        self.name = name
        self.relative_position = relative_position

    def 




class Player():
    def __init__(self, position, tiles):
        self.position = position
        self.tiles = tiles

    def update_position(self, position):
        self.position = position

    def decrement_tiles(self):
        self.tiles = self.tiles - 1



class Board():

    # All possible directions
    _moves = [
            "Right",
            "Right-Jump",
            "Right-Jump-Up",
            "Right-Jump-Down",

            "Down",
            "Down-Jump",
            "Down-Jump-Left",
            "Down-Jump-Right",

            "Left",
            "Left-Jump",
            "Left-Jump-Up",
            "Left-Jump-Down",

            "Up",
            "Up-Jump",
            "Up-Jump-Left",
            "Up-Jump-Right",
        ]

    # map direction to (x,y) offsets
    _directionToOffset = {
        "Right": (0, 2),
        "Right-Jump": (0, 4),
        "Right-Jump-Up": (-2, 2), 
        "Right-Jump-Down": (2, 2),

        "Down": (2, 0),
        "Down-Jump": (4, 0),
        "Down-Jump-Left": (2, -2),   
        "Down-Jump-Right": (2, 2),

        "Left": (0, -2),
        "Left-Jump": (0, -4),
        "Left-Jump-Up": (-2, -2),
        "Left-Jump-Down": (2, -2),

        "Up": (-2, 0),
        "Up-Jump": (-4, 0),
        "Up-Jump-Left":  (-2, -2),
        "Up-Jump-Right": (-2, 2),
    }

    def __init__(self):
        "Set up initial board configuration."
        # 0 - white, 1 - back
        self.turn = 0

        # white player starting position
        self.white_player = [16, 8]
        self.white_tiles = 10

        # black player starting position
        self.black_player = [0, 8]
        self.black_tiles = 10

        # State of tile placement
        self.occupancy = {}


    def get_valid_moves(self):
        """Returns all the valid moves for the given color.
        (1 for white, -1 for black)     
        """
        moves = Set()

    def isWithinBounds(self, x, y):
        x >= 0 & x < 17 & y >= 0 & y < 17




    
        