from __future__ import print_function

import copy
import sys

sys.path.append('..')
from Game import Game
from .GravityChessLogic import Board
import numpy as np


class GravityChessGame(Game):
    def __init__(self):
        super().__init__()

    def getInitBoard(self):
        # return initial board (numpy board)
        b = Board()
        return np.array(b.pieces)

    def getBoardSize(self):
        # (a,b) tuple
        return 8, 8

    def getActionSize(self):
        # return number of actions
        return 8 * 8 * 8 * 8

    def getNextState(self, board, player, action):
        # if player takes action on board, return next (board,player)
        # action must be a valid move
        b = Board()
        b.pieces = np.copy(board)

        target_col = action % 8
        action -= target_col
        action /= 8
        target_row = action % 8
        action -= target_row
        action /= 8
        source_col = action % 8
        action -= source_col
        action /= 8
        source_row = action

        move = (source_row, source_col, target_row, target_col, player)

        b.execute_move(move, player)

        return b.pieces, -player

    def getValidMoves(self, board, player):
        # return a fixed size binary vector
        valids = [0] * self.getActionSize()
        b = Board()
        b.pieces = np.copy(board)

        moves = b.get_legal_moves(player)

        for a, b, c, d in moves:
            valids[512 * a + 64 * b + 8 * c + d] = 1

        return np.array(valids)

    def getGameEnded(self, board, player):
        # return 0 if not ended, 1 if player 1 won, -1 if player 1 lost
        # player = 1
        b = Board()
        b.pieces = np.copy(board)

        if not b.is_tie():
            return 1e-4

        return b.get_winner()

    def getCanonicalForm(self, board, player):
        b = copy.deepcopy(board)
        return b * player

    def getSymmetries(self, board, pi):
        # Vertical mirroring; omit for now
        l = []
        l += [(board, pi)]
        return l

    def stringRepresentation(self, board):
        return board.tostring()

    def getScore(self, board, player):
        b = Board()
        b.pieces = np.copy(board)
        return b.get_winner()

    @staticmethod
    def display(board):
        rows = len(board) - 2
        cols = len(board[0])
        print("   ", end="")
        for y in range(cols):
            print(y, end=" ")
        print("")
        print("-----------------------------")
        for row in range(rows):
            print(chr(ord('A') + row), "|", end="")  # print the row name
            for col in range(cols):
                if board[row][col] is None:
                    print(". ", end='')
                elif board[row][col].type == 1:
                    if board[row][col].color == 1:
                        print("♙ ", end='')
                    else:
                        print("♟ ", end='')
                elif board[row][col].type == 2:
                    if board[row][col].color == 1:
                        print("♘ ", end='')
                    else:
                        print("♞ ", end='')
                elif board[row][col].type == 3:
                    if board[row][col].color == 1:
                        print("♗ ", end='')
                    else:
                        print("♝ ", end='')
                elif board[row][col].type == 4:
                    if board[row][col].color == 1:
                        print("♖ ", end='')
                    else:
                        print("♜ ", end='')
                elif board[row][col].type == 5:
                    if board[row][col].color == 1:
                        print("♕ ", end='')
                    else:
                        print("♛ ", end='')
                elif board[row][col].type == 6:
                    if board[row][col].color == 1:
                        print("♔ ", end='')
                    else:
                        print("♚ ", end='')

            print()

        print("-----------------------------", end='')
        print("    already hopped: " + str(board[rows][0] == 1), end='')
        print("    turn player: " + str(board[rows + 1][0]))
