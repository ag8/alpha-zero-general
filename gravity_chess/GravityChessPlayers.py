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
        valid = self.game.getValidMoves(board, -1)
        for i in range(len(valid)):
            if valid[i]:
                action = i + 3 - 3

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

                print("[", str(source_row), str(source_col), str(target_row), str(target_col), end="] ")
        while True:
            input_move = input()
            input_a = input_move.split(" ")
            if len(input_a) == 4:
                try:
                    w, x, y, z = [int(i) for i in input_a]
                    a = 512 * w + 64 * x + 8 * y + z
                    if valid[a]:
                        break
                    else:
                        print('Invalid move')
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
