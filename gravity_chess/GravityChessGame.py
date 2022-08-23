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

        new_board = np.zeros([8, 8])

        for piece in b:
            new_board[piece.row][piece.col] = piece.type if piece.color == 1 else -piece.type

        return new_board * player

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
        rows = 8
        cols = 8
        print("   ", end="")
        for y in range(cols):
            print(chr(ord('H') - y), end=" ")
        print("")
        print("-----------------------------")
        for row in range(rows):
            print(str(row + 1), "|", end="")  # print the row name
            for col in range(cols):
                current_piece = None

                for piece in board:
                    if piece.row == row and piece.col == col:
                        current_piece = piece

                if current_piece is None:
                    print(". ", end='')
                elif current_piece.type == 1:
                    if current_piece.color == 1:
                        print("♙ ", end='')
                    else:
                        print("♟ ", end='')
                elif current_piece.type == 2:
                    if current_piece.color == 1:
                        print("♘ ", end='')
                    else:
                        print("♞ ", end='')
                elif current_piece.type == 3:
                    if current_piece.color == 1:
                        print("♗ ", end='')
                    else:
                        print("♝ ", end='')
                elif current_piece.type == 4:
                    if current_piece.color == 1:
                        print("♖ ", end='')
                    else:
                        print("♜ ", end='')
                elif current_piece.type == 5:
                    if current_piece.color == 1:
                        print("♕ ", end='')
                    else:
                        print("♛ ", end='')
                elif current_piece.type == 6:
                    if current_piece.color == 1:
                        print("♔ ", end='')
                    else:
                        print("♚ ", end='')

            print()

        print("-----------------------------", end='')
