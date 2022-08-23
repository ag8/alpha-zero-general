import numpy as np


class RandomPlayer():
    def __init__(self, game):
        self.game = game

    def play(self, board):
        a = np.random.randint(self.game.getActionSize())
        valids = self.game.getValidMoves(board, 1)
        while valids[a] != 1:
            a = np.random.randint(self.game.getActionSize())
        return a


class HumanPhilosphersFootballPlayer():
    def __init__(self, game):
        self.game = game

    def play(self, board):
        # display(board)
        valid = self.game.getValidMoves(board, 1)
        for i in range(len(valid)):
            if valid[i]:
                if i == 2 * self.game.rows * self.game.cols:
                    print("[", 2 * self.game.rows, 0, "1 (end hopping)", end="] ")
                else:
                    print("[", int((i % (self.game.rows * self.game.cols)) / self.game.cols), i % self.game.cols,
                      "2 (hop)" if not (i % (self.game.rows * self.game.cols) == i) else "1 (place)", end="] ")
        while True:
            input_move = input()
            input_a = input_move.split(" ")
            if len(input_a) == 3:
                try:
                    x, y, z = [int(i) for i in input_a]
                    a = self.game.cols * x + y if z == 1 else (self.game.rows * self.game.cols) + (
                                self.game.cols * x + y)
                    if valid[a]:
                        break
                except ValueError:
                    # Input needs to be an integer
                    'Invalid integer'
            print('Invalid move')
        return a


class GreedyPhilosphersFootballPlayer():
    def __init__(self, game):
        self.game = game

    def play(self, board):
        valids = self.game.getValidMoves(board, 1)
        candidates = []
        for a in range(self.game.getActionSize()):
            if valids[a] == 0:
                continue
            nextBoard, _ = self.game.getNextState(board, 1, a)
            score = self.game.getScore(nextBoard, 1)
            candidates += [(-score, a)]
        candidates.sort()
        return candidates[0][1]
