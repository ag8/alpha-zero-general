'''
Author: Eric P. Nichols
Date: Feb 8, 2008.
Board class.
Board data:
  1=white, -1=black, 0=empty
  first dim is column , 2nd is row:
     pieces[1][7] is the square in column 2,
     at the opposite end of the board in row 8.
Squares are stored and manipulated as (x,y) tuples.
x is the column, y is the row.
'''
import numpy as np


class Board():
    # list of all 8 directions on the board, as (x,y) offsets
    __directions = [(1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1)]

    def __init__(self, rows, cols):
        "Set up initial board configuration."

        self.cols = cols
        self.rows = rows

        # Create the empty board array.
        self.pieces = np.zeros([self.rows + 2, self.cols])  # Two extra rows for storing information

        # Set up the initial location of the football.
        self.pieces[int(self.rows / 2)][int(self.cols / 2)] = 2

    # add [][] indexer syntax to the Board
    def __getitem__(self, index):
        return self.pieces[index]

    def get_legal_moves(self, color):
        """Returns all the legal moves for the given color.
        (1 for white, -1 for black
        """
        moves = set()  # stores the legal moves.

        # First, all empty spots are valid moves to place a player.
        for row in range(self.rows):
            for col in range(self.cols):
                if col == 0 or col == self.cols - 1:
                    continue

                if self[row][col] == 0:
                    moves.add((row, col))

        # Next, all hops are valid moves.
        hops = self.get_hops()

        # Finally, "skipping" is only allowed if the player has already hopped.
        player_already_hopped = self[self.rows][0] == 1
        others = [(2 * self.rows, 0)] if player_already_hopped else []

        return moves, hops, others

    def get_hops(self):
        """
        Returns all the possible (one-step) hops the football can take.
        """
        x, y = self.get_football_location()

        hops = []

        for direction in self.__directions:
            # First, there must be a player to jump over.
            xp = x + direction[0]
            yp = y + direction[1]

            if yp == 0 or yp == self.cols - 1:  # winning move
                if self.in_bounds(xp, yp):
                    hops.append((xp, yp))
                continue

            if self.in_bounds(xp, yp):
                if self[xp][yp] == 1:
                    # If there is, figure out how far we can jump in that direction.
                    jump_result = self.get_jump(xp, yp, direction)

                    if jump_result is not None:
                        hops.append(jump_result)

        return hops

    def get_jump(self, xp, yp, direction):
        while self[xp][yp] == 1:
            xp += direction[0]
            yp += direction[1]

            if not self.in_bounds(xp, yp):
                return None

            if yp == 0 or yp == self.cols - 1:  # winning move
                if self[xp][yp] == 0:
                    return (xp, yp)
                else:
                    return None

        return (xp, yp) if self.in_bounds(xp, yp) and self[xp][yp] == 0 else None

    def in_bounds(self, row, col):
        return 0 <= row < self.rows

    def get_football_location(self):
        for row in range(self.rows):
            for col in range(self.cols):
                if self[row][col] == 2:
                    return row, col

        raise Exception("Where'd the football go?")

    def has_legal_moves(self, color):
        # Assumes the player has not already placed a player.
        # (But execute_move logic should take care of this).

        for row in range(self.rows):
            for col in range(self.cols):
                if col == 0 or col == self.cols - 1:
                    continue

                if self[row][col] == 0:
                    return True

        # If there's no empty spots left, can't hop anywhere, either
        return False

    def execute_move(self, move, color):
        """Perform the given move on the board; removes hopped-over players if necessary.
        """
        row, col, is_hop = move

        if not is_hop:
            # Placing a player.
            self[row][col] = 1

            # Say it's the other player's move now.
            self.pieces[self.rows + 1] = [-color] * self.cols

            # Reset hops
            self.pieces[self.rows] = [0] * self.cols

            return

        # If we're here, then we're hopping.
        cur_row, cur_col = self.get_football_location()

        # If the target column is out of bounds, game is already over.
        if col >= self.cols:
            self[0][self.cols - 1] = 2  # Just force the ball in the goal
            self[cur_row][cur_col] = 0
            return
        if col < 0:
            self[0][0] = 2
            self[cur_row][cur_col] = 0
            return

        # Otherwise, do a normal hop computation
        rdir = 1 if row > cur_row + 1 else -1
        cdir = 1 if col > cur_col + 1 else -1

        for r in range(cur_row + 1, row, rdir):
            for c in range(cur_col + 1, col, cdir):
                self[r][c] = 0  # Remove players in the way

        self[row][col] = 2  # Move the football
        self[cur_row][cur_col] = 0  # Remove it from the old place

        self.pieces[self.rows] = [1] * self.cols  # Record a hop

    def get_winner(self):
        row, col = self.get_football_location()

        if col == 0:
            return -1
        elif col == self.cols - 1:
            return 1
        else:
            return 0
