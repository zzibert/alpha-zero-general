from __future__ import print_function
import sys
sys.path.append('..')
from Game import Game
from .OthelloLogic import Board
import numpy as np

class QuoridorGame(Game):

    def getInitBoard(self):
        # return initial board (numpy board)
        b = Board()
        return b
    
    def getNextState(self, board, player, action):
        nextBoard = board.makeAction(player, action)

        return (nextBoard, -player)
    
    def getValidMoves(self, board, player):
        return board.getValidMoves(player)

    
    def getGameEnded(self, board, player):
        # return 0 if not ended, 1 if player 1 won, -1 if player 1 lost
        # player = 1
        if board.isGameCompleted():
            return board.getGameResult(player)
        else:
            return 0

    # TODO:
    def stringRepresentation(self, board):
        pass


    



