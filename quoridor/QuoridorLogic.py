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

class PlayerId(Enum):
    WHITE = 0
    BLACK = 1

class Position():
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __eq__(self, other) -> bool:
        if not isinstance(other, Position):
            return NotImplemented
        
        return self.x == other.x and self.y == other.y
    
    def __hash__(self) -> int:
        return hash({self.x, self.y})

    def is_within_bounds(self) -> bool:
        return self.x >= 0 and self.x < 17 and self.y >= 0 and self.y < 17

white_starting_position = Position(16, 8)
black_starting_position = Position(0, 8)

def get_starting_position(player_id) -> Position:
    if (player_id == PlayerId.WHITE):
        return white_starting_position
    else: 
        return black_starting_position

class RelativePosition():
    def __init__(self, dx: int, dy: int):
        self.dx = dx
        self.dy = dy

    def transform(self, position: Position) -> Position:
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

    # all(x > 0 for x in numbers)
    def is_condition_met(self, player_position: Position, opponent_position: Position, occupancy) -> bool:
        return (
            all(relative.transform(player_position) == opponent_position for relative in self.occupied) and
            all(relative.transform(player_position) != opponent_position for relative in self.not_occupied) and
            all(self.is_direction_blocked(relative, player_position, occupancy) for relative in self.blocked) and
            all(relative.transform(player_position) not in occupancy for relative in self.not_blocked)
        )

    
    def is_direction_blocked(self, relative: RelativePosition, player_position: Position, occupancy) -> bool:
        potential_position = relative.transform(player_position)
        return potential_position in occupancy or not potential_position.is_within_bounds()

class Direction():
    def __init__(self, name, relative_position: RelativePosition, occupied=[], not_occupied=[], blocked=[], not_blocked=[]):
        self.name = name
        self.relative_position = relative_position
        self.condition = DirectionCondition(occupied=occupied, not_occupied=not_occupied, blocked=blocked, not_blocked=not_blocked)

class DirectionType(Enum):
    LEFT = Direction(
        name="Left", 
        relative_position=RelativePosition(0, -2),
        not_occupied=[RelativePosition(0, -2)],
        not_blocked=[RelativePosition(0, -1)]
    )
    
    LEFT_JUMP = Direction(
        name="Left-Jump",
        relative_position=RelativePosition(0, -4),
        occupied=[RelativePosition(0, -2)],
        not_blocked=[RelativePosition(0, -1),RelativePosition(0, -3)]
    )
    
    LEFT_JUMP_UP = Direction(
        name="Left-Jump-Up",
        relative_position=RelativePosition(-2, -2),
        occupied=[RelativePosition(0, -2)],
        not_blocked=[RelativePosition(0, -1), RelativePosition(-1, -2)],
        blocked=[RelativePosition(0, -3)]
    )

    LEFT_JUMP_DOWN = Direction(
        name="Left-Jump-Down",
        relative_position=RelativePosition(2, -2),
        occupied=[RelativePosition(0, -2)],
        not_blocked=[RelativePosition(0, -1), RelativePosition(1, -2)],
        blocked=[RelativePosition(0, -3)]
    )

    RIGHT = Direction(
        name="Right",
        relative_position=RelativePosition(0, 2),
        not_occupied=[RelativePosition(0, 2)],
        not_blocked=[RelativePosition(0, 1)]
    )

    RIGHT_JUMP = Direction(
        name="Right-Jump",
        relative_position=RelativePosition(0, 4),
        occupied=[RelativePosition(0, 2)],
        not_blocked=[RelativePosition(0, 1), RelativePosition(0, 3)]
    )

    RIGHT_JUMP_UP = Direction(
        name="Right-Jump-Up",
        relative_position=RelativePosition(-2, 2),
        occupied=[RelativePosition(0, 2)],
        blocked=[RelativePosition(0, 3)],
        not_blocked=[RelativePosition(0, 1), RelativePosition(-1, 2)]
    )

    RIGHT_JUMP_DOWN = Direction(
        name="Right-Jump-Down",
        relative_position=RelativePosition(2, 2),
        occupied=[RelativePosition(0, 2)],
        blocked=[RelativePosition(0, 3)],
        not_blocked=[RelativePosition(0, 1), RelativePosition(1, 2)]
    )

    UP = Direction(
        name="Up",
        relative_position=RelativePosition(-2, 0),
        not_occupied=[RelativePosition(-2, 0)],
        not_blocked=[RelativePosition(-1, 0)]
    )

    UP_JUMP = Direction(
        name="Up-Jump",
        relative_position=RelativePosition(-4, 0),
        occupied=[RelativePosition(-2, 0)],
        not_blocked=[RelativePosition(-1, 0), RelativePosition(-3, 0)]
    )

    UP_JUMP_LEFT = Direction(
        name="Up-Jump-Left",
        relative_position=RelativePosition(-2, -2),
        occupied=[RelativePosition(-2, 0)],
        blocked=[RelativePosition(-3, 0)],
        not_blocked=[RelativePosition(-1, 0), RelativePosition(-2, -1)]
    )

    UP_JUMP_RIGHT = Direction(
        name="Up-Jump-Right",
        relative_position=RelativePosition(-2, 2),
        occupied=[RelativePosition(-2, 0)],
        blocked=[RelativePosition(-3, 0)],
        not_blocked=[RelativePosition(-1, 0), RelativePosition(-2, 1)]
    )

    DOWN = Direction(
        name="Down",
        relative_position=RelativePosition(2, 0),
        not_occupied=[RelativePosition(2, 0)],
        not_blocked=[RelativePosition(1, 0)]
    )

    DOWN_JUMP = Direction(
        name="Down-Jump",
        relative_position=RelativePosition(4, 0),
        occupied=[RelativePosition(2, 0)],
        not_blocked=[RelativePosition(1, 0), RelativePosition(3, 0)]
    )

    DOWN_JUMP_LEFT = Direction(
        name="Down-Jump-Left",
        relative_position=RelativePosition(2, -2),
        occupied=[RelativePosition(2, 0)],
        blocked=[RelativePosition(3, 0)],
        not_blocked=[RelativePosition(1, 0), RelativePosition(2, -1)]
    )

    DOWN_JUMP_RIGHT = Direction(
        name="Down-Jump-Right",
        relative_position=RelativePosition(2, 2),
        occupied=[RelativePosition(2, 0)],
        blocked=[RelativePosition(3, 0)],
        not_blocked=[RelativePosition(1, 0), RelativePosition(2, 1)]
    )

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
    _moves = {
            "Right": DirectionType.RIGHT,
            "Right-Jump": DirectionType.RIGHT_JUMP,
            "Right-Jump-Up": DirectionType.RIGHT_JUMP_UP,
            "Right-Jump-Down": DirectionType.RIGHT_JUMP_DOWN,

            "Down": DirectionType.DOWN,
            "Down-Jump": DirectionType.DOWN_JUMP,
            "Down-Jump-Left": DirectionType.DOWN_JUMP_LEFT,
            "Down-Jump-Right": DirectionType.DOWN_JUMP_RIGHT,

            "Left": DirectionType.LEFT,
            "Left-Jump": DirectionType.LEFT_JUMP,
            "Left-Jump-Up": DirectionType.LEFT_JUMP_UP,
            "Left-Jump-Down": DirectionType.LEFT_JUMP_DOWN,

            "Up": DirectionType.UP,
            "Up-Jump": DirectionType.UP_JUMP,
            "Up-Jump-Left": DirectionType.UP_JUMP_LEFT,
            "Up-Jump-Right": DirectionType.UP_JUMP_RIGHT,
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




    
        