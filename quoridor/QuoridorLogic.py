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
from typing import List, Set

class PlayerId(Enum):
    WHITE = 1
    BLACK = -1

class Position():
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __eq__(self, other) -> bool:
        if not isinstance(other, Position):
            return NotImplemented
        
        return self.x == other.x and self.y == other.y
    
    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def is_within_bounds(self) -> bool:
        return self.x >= 0 and self.x < 17 and self.y >= 0 and self.y < 17

white_starting_position = Position(16, 8)
black_starting_position = Position(0, 8)

def get_starting_position(player_id) -> Position:
    if (player_id == PlayerId.WHITE.value):
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

class Player ():
    def __init__(self, position: Position, tiles):
        self.position = position
        self.tiles = tiles

    def update_position(self, position):
        return Player(position=position, tiles=self.tiles)
        

    def decrement_tiles(self):
        return Player(position=self.position,tiles=self.tiles-1)
        


class Action ():
    def __init__(self, isMove: bool, position, isHorizontal=None):
        self.isMove = isMove
        self.position = position
        self.isHorizontal = isHorizontal

class Tile ():
    def __init__(self, isHorizontal: bool, position: Position):
        self.isHorizontal = isHorizontal
        self.position = position

    def blocks(self) -> List[Position]:
        if self.isHorizontal:
            return [Position(x=self.x, y=self.y+i) for i in range(3)]
        else:
            return [Position(x=self.x+i, y=self.y) for i in range(3)]
        
    
    def occupancy(self) -> Set[Position]:
        block_list = self.blocks()
        return set(block_list)





class Board ():
    def __init__(self, white_player, black_player, occupancy):
        self.white_player=white_player
        self.black_player=black_player
        self.occupancy=occupancy

    def get_player(self, player_id: int) -> Player:
        if player_id == PlayerId.WHITE.value:
            return self.white_player
        else:
            return self.black_player
        
    def place_tile(self, player_id, tile: Tile):
        new_occupancy = self.occupancy.copy()
        new_occupancy.update(tile.occupancy())

        if player_id == PlayerId.WHITE.value:
            return Board(
                white_player=self.white_player.decrement_tiles(),
                black_player=self.black_player,
                occupancy=new_occupancy
            )
        else:
            return Board(
                white_player=self.white_player,
                black_player=self.black_player.decrement_tiles(),
                occupancy=new_occupancy
            )
        

        
    def make_move(self, player_id: int, position: Position):
        if (player_id == PlayerId.WHITE.value):
            white_player = Player(position=position, tiles=self.white_player.tiles)
            return Board(
                white_player=white_player,
                black_player=self.black_player,
                occupancy=self.occupancy
            )
        else:
            black_player = Player(position=position, tiles=self.black_player.tiles)
            return Board(
                white_player=self.white_player,
                black_player=black_player,
                occupancy=self.occupancy
            )
    
    def make_action(self, player_id, action):
        if action.isMove:
            return self.make_move(player_id, action.position)
        else:
            return self.place_tile(player_id, Tile(isHorizontal=action.isHorizontal, position=action.position))
        
    def is_game_completed(self) -> bool:
        return self.white_player.position.x == 0 or self.black_player.position.x == 16
    
    # First call is_game_completed
    # result 1 : white won
    # result -1 : black won
    # result 0/5 : draw
    def get_game_result(self) -> float:
        if self.white_player.position.x == 0 and self.black_player.position.x == 16:
            return 0.5
        elif self.white_player.position == 0:
            return 1
        else:
            return -1
            
    
        




        



    def get_valid_moves(self):
        """Returns all the valid moves for the given color.
        (1 for white, -1 for black)     
        """
        moves = Set()




    
        