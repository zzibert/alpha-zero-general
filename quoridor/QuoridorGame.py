from __future__ import print_function
import sys
sys.path.append('..')
from Game import Game
from .QuoridorLogic import Board, DirectionType
import numpy as np

class QuoridorGame(Game):

    def getInitBoard(self):
        # return initial board (numpy board)
        b = Board()
        return b
    
    def getNextState(self, board, player, action):
        nextBoard = board.make_action(player, action)

        return (nextBoard, -player)
    
    def getValidMoves(self, board, player):
        return board.getValidMoves(player)
    
    def getActionSize(self):
        # return all possible moves and tile placements
        return len(DirectionType)

    
    def getGameEnded(self, board, player):
        if board.is_game_completed():
            result = board.get_game_result()
            if result == 0.5:
                return result
            elif player == result:
                return 1
            else:
                return -1

        else:
            return 0

    # TODO:
    def stringRepresentation(self, board):
        pass


    



