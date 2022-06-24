from __future__ import print_function

import copy
import sys

sys.path.append('..')
from Game import Game
from .PhilosophersFootballLogic import Board
import numpy as np


class PhilosophersFootballGame(Game):
    def __init__(self, rows, cols):
        super().__init__()
        self.rows = rows
        self.cols = cols

    def getInitBoard(self):
        # return initial board (numpy board)
        b = Board(self.rows, self.cols)
        return np.array(b.pieces)

    def getBoardSize(self):
        # (a,b) tuple
        return self.rows + 2, self.cols

    def getActionSize(self):
        # return number of actions
        return 2 * self.rows * self.cols + 1

    def getNextState(self, board, player, action):
        # if player takes action on board, return next (board,player)
        # action must be a valid move
        if action == 2 * self.rows * self.cols:
            bq = Board(self.rows, self.cols)
            bq.pieces = np.copy(board)
            bq.pieces[self.rows] = [0] * self.cols  # reset hops
            return bq.pieces, -player

        b = Board(self.rows, self.cols)
        b.pieces = np.copy(board)

        is_hop = not (action % (self.rows * self.cols) == action)

        move = (int((action % (self.rows * self.cols)) / self.cols),  # row
                action % self.cols,  # col
                is_hop)  # is_hop

        b.execute_move(move, player)

        return b.pieces, player if is_hop else -player

    def getValidMoves(self, board, player):
        # return a fixed size binary vector
        valids = [0] * self.getActionSize()
        b = Board(self.rows, self.cols)
        b.pieces = np.copy(board)

        moves, hops, others = b.get_legal_moves(player)

        if len(moves) == 0:
            valids[-1] = 1
            return np.array(valids)

        for x, y in moves:
            valids[self.cols * x + y] = 1

        for x, y in hops:
            valids[self.rows * self.cols + self.cols * x + y] = 1

        for x, y in others:
            valids[-1] = 1

        return np.array(valids)

    def getGameEnded(self, board, player):
        # return 0 if not ended, 1 if player 1 won, -1 if player 1 lost
        # player = 1
        b = Board(self.rows, self.cols)
        b.pieces = np.copy(board)

        if not b.has_legal_moves(1):
            return 1e-4  # No more moves --> tie

        return b.get_winner()

    def getCanonicalForm(self, board, player):
        b = copy.deepcopy(board)
        b[self.rows + 1] = [player] * self.cols
        return b

    def getSymmetries(self, board, pi):
        # Vertical mirroring; omit for now
        l = []
        l += [(board, pi)]
        return l

    def stringRepresentation(self, board):
        return board.tostring()

    def getScore(self, board, player):
        b = Board(self.rows, self.cols)
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
                if board[row][col] == 0:
                    print(". ", end='')
                elif board[row][col] == 1:
                    print("⬤ ", end='')
                elif board[row][col] == 2:
                    print("◯ ", end='')

            print()

        print("-----------------------------", end='')
        print("    already hopped: " + str(board[rows][0] == 1), end='')
        print("    turn player: " + str(board[rows + 1][0]))
