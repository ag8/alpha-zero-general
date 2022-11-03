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
        return b.board_rep

    def getBoardSize(self):
        # (a,b) tuple
        return 8, 10

    def getActionSize(self):
        # return number of actions
        return 8 * 8 * 8 * 8

    def getNextState(self, board, player, action):
        # if player takes action on board, return next (board,player)
        # action must be a valid move
        b = Board()
        b.load_info(board)  # todo might also need to custom load player??

        target_col = int(action % 8)
        action -= target_col
        action /= 8
        target_row = int(action % 8)
        action -= target_row
        action /= 8
        source_col = int(action % 8)
        action -= source_col
        action /= 8
        source_row = int(action)

        move = (source_row, source_col, target_row, target_col)

        b.execute_move(move, player)

        return b.board_rep, -player

    def getValidMoves(self, board, player):
        # return a fixed size binary vector
        valids = [0] * self.getActionSize()
        b = Board()
        b.load_info(board)  # todo same

        moves = b.get_legal_moves(b.player_turn)

        for a, b, c, d in moves:
            valids[int(512 * a + 64 * b + 8 * c + d)] = 1

        return np.array(valids)

    def getGameEnded(self, board, player):
        # return 0 if not ended, 1 if player 1 won, -1 if player 1 lost
        # player = 1
        b = Board()
        # if isinstance(board[0], np.ndarray):
        #     b.pieces = copy.deepcopy(pieces_from_canonical(board))
        #     b.player_turn = board[8][0]
        # else:
        b.load_info(board)

        if b.is_tie():
            return 1e-4

        return b.get_winner()

    def getCanonicalForm(self, board, player):
        b = copy.deepcopy(board)
        return b

    def getSymmetries(self, board, pi):
        # Vertical mirroring; omit for now
        l = []
        l += [(board, pi)]
        return l

    def stringRepresentation(self, board):
        return board.tostring()

    def getScore(self, board, player):
        b = Board()
        b.load_info(board)
        return b.get_winner()

    @staticmethod
    def display(board):
        if isinstance(board, np.ndarray):
            rows = 8
            cols = 8
            print("   ", end="")
            for y in range(cols):
                # print(chr(ord('H') - y), end=" ")
                print(str(y), end=" ")
            print("")
            print("-----------------------------")
            for row in range(rows):
                # print(str(row + 1), "|", end="")  # print the row name
                print(str(row), "|", end="")  # print the row name
                for col in range(cols):
                    if abs(board[row][col]) == 0:
                        print(". ", end='')
                    elif abs(board[row][col]) == 1:
                        if (1 if board[row][col] > 0 else -1) == 1:
                            print("P ", end='')
                        else:
                            print("p ", end='')
                    elif abs(board[row][col]) == 2:
                        if (1 if (board[row][col]) > 0 else -1) == 1:
                            print("N ", end='')
                        else:
                            print("n ", end='')
                    elif abs(board[row][col]) == 3:
                        if (1 if (board[row][col]) > 0 else -1) == 1:
                            print("B ", end='')
                        else:
                            print("b ", end='')
                    elif abs(board[row][col]) == 4:
                        if (1 if (board[row][col]) > 0 else -1) == 1:
                            print("R ", end='')
                        else:
                            print("r ", end='')
                    elif abs(board[row][col]) == 5:
                        if (1 if (board[row][col]) > 0 else -1) == 1:
                            print("Q ", end='')
                        else:
                            print("q ", end='')
                    elif abs(board[row][col]) == 6:
                        if (1 if (board[row][col]) > 0 else -1) == 1:
                            print("K ", end='')
                        else:
                            print("k ", end='')

                print()

            print()
            print("Current turn: " + str(int(board[8][0])))
            print("Turns: " + str(int(board[9][7])))
            print("-----------------------------", end='')
            print()
            print()
