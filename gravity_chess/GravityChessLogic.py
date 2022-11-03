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


class Piece():
    def __init__(self, type, row, col, color):
        self.type = type
        self.row = row
        self.col = col
        self.color = color


class Board():
    _PAWN = 1
    _KNIGHT = 2
    _BISHOP = 3
    _ROOK = 4
    _QUEEN = 5
    _KING = 6

    def __init__(self):
        "Set up initial board configuration."
        self.board_size = 8
        self.s = self.board_size  # short alias

        self.internal_pieces = list()

        # Set up the initial board position
        for i in range(8):
            self.internal_pieces.append(Piece(self._PAWN, 1, i, 1))
            self.internal_pieces.append(Piece(self._PAWN, 6, i, -1))

        for i in [0, 7]:
            self.internal_pieces.append(Piece(self._ROOK, i, 0, 1 if i == 0 else -1))
            self.internal_pieces.append(Piece(self._KNIGHT, i, 1, 1 if i == 0 else -1))
            self.internal_pieces.append(Piece(self._BISHOP, i, 2, 1 if i == 0 else -1))
            self.internal_pieces.append(Piece(self._KING, i, 3, 1 if i == 0 else -1))
            self.internal_pieces.append(Piece(self._QUEEN, i, 4, 1 if i == 0 else -1))
            self.internal_pieces.append(Piece(self._BISHOP, i, 5, 1 if i == 0 else -1))
            self.internal_pieces.append(Piece(self._KNIGHT, i, 6, 1 if i == 0 else -1))
            self.internal_pieces.append(Piece(self._ROOK, i, 7, 1 if i == 0 else -1))

        # Other game state variables
        # TODO: These game state variables currently:
        # 1. don't get displayed canonically, and thus are unknown for the players
        # 2. are not carried over during lookahad.
        # both of these issues should be fixed.
        self.short_castling_allowed = True
        self.long_castling_allowed = True
        self.en_passant_allowed = True
        self.en_passant_target_col = -1
        self.en_passant_target_row = -1
        self.en_passant_victim_col = -1
        self.en_passant_victim_row = -1

        self.player_turn = 1

        self.stupid_moves = 0

        self.board_rep = np.zeros([10, 8])

        for piece in self.internal_pieces:
            self.board_rep[piece.row][piece.col] = piece.type if piece.color == 1 else -piece.type

        self.board_rep[8] = [self.player_turn] * 8
        self.board_rep[9][0] = self.short_castling_allowed
        self.board_rep[9][1] = self.long_castling_allowed
        self.board_rep[9][2] = self.en_passant_allowed
        self.board_rep[9][3] = self.en_passant_target_row
        self.board_rep[9][4] = self.en_passant_target_col
        self.board_rep[9][5] = self.en_passant_victim_row
        self.board_rep[9][6] = self.en_passant_victim_col
        self.board_rep[9][7] = self.stupid_moves

    # add [][] indexer syntax to the Board
    # def __getitem__(self, tup):
    #     y, x = tup
    #     return self.get_piece_on(x, y)

    def load_info(self, board, player=None):
        self.internal_pieces = list()

        for row in range(8):
            for col in range(8):
                if abs((board[row][col])) > 0:
                    self.internal_pieces.append(Piece(int(abs(board[row][col])), row, col, 1 if board[row][col] > 0 else -1))

        if player is None:
            self.player_turn = board[8][0]
        else:
            self.player_turn = player

        self.short_castling_allowed = board[9][0]
        self.long_castling_allowed = board[9][1]
        self.en_passant_allowed = board[9][2]
        self.en_passant_target_row = board[9][3]
        self.en_passant_target_col = board[9][4]
        self.en_passant_victim_row = board[9][5]
        self.en_passant_victim_col = board[9][6]
        self.stupid_moves = board[9][7]

        self.update_board_representation()

    def update_board_representation(self):
        self.board_rep = np.zeros([10, 8])

        for piece in self.internal_pieces:
            self.board_rep[piece.row][piece.col] = piece.type if piece.color == 1 else -piece.type

        self.board_rep[8] = [self.player_turn] * 8
        self.board_rep[9][0] = self.short_castling_allowed
        self.board_rep[9][1] = self.long_castling_allowed
        self.board_rep[9][2] = self.en_passant_allowed
        self.board_rep[9][3] = self.en_passant_target_col
        self.board_rep[9][4] = self.en_passant_target_row
        self.board_rep[9][5] = self.en_passant_victim_col
        self.board_rep[9][6] = self.en_passant_victim_row
        self.board_rep[9][7] = self.stupid_moves

    def get_piece_on(self, row, col):
        for piece in self.internal_pieces:
            if piece.row == row and piece.col == col:
                return piece

        return None

    def on_board(self, row, col):
        return 0 <= row < self.s and 0 <= col < self.s

    def get_moves(self, piece):
        """Returns a list of all the moves a piece can do (does not check for legality cause w/e)."""
        moves = list()

        row = piece.row
        col = piece.col

        if piece.type == self._PAWN:
            if piece.color == 1:
                if self.get_piece_on(row + 1, col) is None:
                    if row != 6:
                        moves.append([row + 1, col])

                if row == 1:
                    if self.get_piece_on(row + 1, col) is None and self.get_piece_on(row + 2, col) is None:
                        moves.append([row + 2, col])

                if self.get_piece_on(row + 1, col + 1) is not None or (
                        row + 1 == self.en_passant_target_row and col + 1 == self.en_passant_target_col and self.en_passant_allowed):
                    if self.get_piece_on(row + 1, col + 1) is None:  # en passant
                        moves.append([row + 1, col + 1])
                    elif self.get_piece_on(row + 1, col + 1).color == -1:
                        moves.append([row + 1, col + 1])

                if self.get_piece_on(row + 1, col - 1) is not None or (
                        row + 1 == self.en_passant_target_row and col - 1 == self.en_passant_target_col and self.en_passant_allowed):
                    if self.get_piece_on(row + 1, col - 1) is None:  # en passant
                        moves.append([row + 1, col - 1])
                    elif self.get_piece_on(row + 1, col - 1).color == -1:
                        moves.append([row + 1, col - 1])
            else:
                if self.get_piece_on(row - 1, col) is None:
                    if row != 1:
                        moves.append([row - 1, col])

                if row == 6:
                    if self.get_piece_on(row - 1, col) is None and self.get_piece_on(row - 2, col) is None:
                        moves.append([row - 2, col])

                if self.get_piece_on(row - 1, col + 1) is not None or (
                        row - 1 == self.en_passant_target_row and col + 1 == self.en_passant_target_col and self.en_passant_allowed):
                    if self.get_piece_on(row - 1, col + 1) is None:  # en passant
                        moves.append([row - 1, col + 1])
                    elif self.get_piece_on(row - 1, col + 1).color == 1:
                        moves.append([row - 1, col + 1])

                if self.get_piece_on(row - 1, col - 1) is not None or (
                        row - 1 == self.en_passant_target_row and col - 1 == self.en_passant_target_col and self.en_passant_allowed):
                    if self.get_piece_on(row - 1, col - 1) is None:  # en passant
                        moves.append([row - 1, col - 1])
                    elif self.get_piece_on(row - 1, col - 1).color == 1:
                        moves.append([row - 1, col - 1])

        if piece.type == self._ROOK:
            for i in range(row + 1, 8):
                if self.get_piece_on(i, col) is not None:
                    if self.get_piece_on(i, col).color == piece.color:
                        break

                    moves.append([i, col])
                    break
                else:
                    moves.append([i, col])

            for i in range(row - 1, -1, -1):
                if self.get_piece_on(i, col) is not None:
                    if self.get_piece_on(i, col).color == piece.color:
                        break

                    moves.append([i, col])
                    break
                else:
                    moves.append([i, col])

            for i in range(col + 1, 8):
                if self.get_piece_on(row, i) is not None:
                    if self.get_piece_on(row, i).color == piece.color:
                        break

                    moves.append([row, i])
                    break
                else:
                    moves.append([row, i])

            for i in range(col - 1, -1, -1):
                if self.get_piece_on(row, i) is not None:
                    if self.get_piece_on(row, i).color == piece.color:
                        break

                    moves.append([row, i])
                    break
                else:
                    moves.append([row, i])

        if piece.type == self._KNIGHT:
            if self.get_piece_on(row + 2, col + 1) is not None:
                if self.get_piece_on(row + 2, col + 1).color is not piece.color:
                    moves.append([row + 2, col + 1])
            else:
                if self.on_board(row + 2, col + 1):
                    moves.append([row + 2, col + 1])

            if self.get_piece_on(row + 2, col - 1) is not None:
                if self.get_piece_on(row + 2, col - 1).color is not piece.color:
                    moves.append([row + 2, col - 1])
            else:
                if self.on_board(row + 2, col - 1):
                    moves.append([row + 2, col - 1])

            if self.get_piece_on(row - 2, col + 1) is not None:
                if self.get_piece_on(row - 2, col + 1).color is not piece.color:
                    moves.append([row - 2, col + 1])
            else:
                if self.on_board(row - 2, col + 1):
                    moves.append([row - 2, col + 1])

            if self.get_piece_on(row - 2, col - 1) is not None:
                if self.get_piece_on(row - 2, col - 1).color is not piece.color:
                    moves.append([row - 2, col - 1])
            else:
                if self.on_board(row - 2, col - 1):
                    moves.append([row - 2, col - 1])

            if self.get_piece_on(row + 1, col + 2) is not None:
                if self.get_piece_on(row + 1, col + 2).color is not piece.color:
                    moves.append([row + 1, col + 2])
            else:
                if self.on_board(row + 1, col + 2):
                    moves.append([row + 1, col + 2])

            if self.get_piece_on(row - 1, col + 2) is not None:
                if self.get_piece_on(row - 1, col + 2).color is not piece.color:
                    moves.append([row - 1, col + 2])
            else:
                if self.on_board(row - 1, col + 2):
                    moves.append([row - 1, col + 2])

            if self.get_piece_on(row + 1, col - 2) is not None:
                if self.get_piece_on(row + 1, col - 2).color is not piece.color:
                    moves.append([row + 1, col - 2])
            else:
                if self.on_board(row + 1, col - 2):
                    moves.append([row + 1, col - 2])

            if self.get_piece_on(row - 1, col - 2) is not None:
                if self.get_piece_on(row - 1, col - 2).color is not piece.color:
                    moves.append([row - 1, col - 2])
            else:
                if self.on_board(row - 1, col - 2):
                    moves.append([row - 1, col - 2])

        if piece.type == self._BISHOP:
            for i in range(1, 10):
                new_row = row + i
                new_col = col + i

                if not self.on_board(new_row, new_col):
                    break

                if self.get_piece_on(new_row, new_col) is not None:
                    if self.get_piece_on(new_row, new_col).color is piece.color:
                        break

                    moves.append([new_row, new_col])
                    break
                else:
                    moves.append([new_row, new_col])

            for i in range(1, 10):
                new_row = row + i
                new_col = col - i

                if not self.on_board(new_row, new_col):
                    break

                if self.get_piece_on(new_row, new_col) is not None:
                    if self.get_piece_on(new_row, new_col).color is piece.color:
                        break

                    moves.append([new_row, new_col])
                    break
                else:
                    moves.append([new_row, new_col])

            for i in range(1, 10):
                new_row = row - i
                new_col = col + i

                if not self.on_board(new_row, new_col):
                    break

                if self.get_piece_on(new_row, new_col) is not None:
                    if self.get_piece_on(new_row, new_col).color is piece.color:
                        break

                    moves.append([new_row, new_col])
                    break
                else:
                    moves.append([new_row, new_col])

            for i in range(1, 10):
                new_row = row - i
                new_col = col - i

                if not self.on_board(new_row, new_col):
                    break

                if self.get_piece_on(new_row, new_col) is not None:
                    if self.get_piece_on(new_row, new_col).color is piece.color:
                        break

                    moves.append([new_row, new_col])
                    break
                else:
                    moves.append([new_row, new_col])

        if piece.type == self._QUEEN:
            for i in range(row + 1, 8):
                if self.get_piece_on(i, col) is not None:
                    if self.get_piece_on(i, col).color == piece.color:
                        break

                    moves.append([i, col])
                    break
                else:
                    moves.append([i, col])

            for i in range(row - 1, -1, -1):
                if self.get_piece_on(i, col) is not None:
                    if self.get_piece_on(i, col).color == piece.color:
                        break

                    moves.append([i, col])
                    break
                else:
                    moves.append([i, col])

            for i in range(col + 1, 8):
                if self.get_piece_on(row, i) is not None:
                    if self.get_piece_on(row, i).color == piece.color:
                        break

                    moves.append([row, i])
                    break
                else:
                    moves.append([row, i])

            for i in range(col - 1, -1, -1):
                if self.get_piece_on(row, i) is not None:
                    if self.get_piece_on(row, i).color == piece.color:
                        break

                    moves.append([row, i])
                    break
                else:
                    moves.append([row, i])

            for i in range(1, 10):
                new_row = row + i
                new_col = col + i

                if not self.on_board(new_row, new_col):
                    break

                if self.get_piece_on(new_row, new_col) is not None:
                    if self.get_piece_on(new_row, new_col).color is piece.color:
                        break

                    moves.append([new_row, new_col])
                    break
                else:
                    moves.append([new_row, new_col])

            for i in range(1, 10):
                new_row = row + i
                new_col = col - i

                if not self.on_board(new_row, new_col):
                    break

                if self.get_piece_on(new_row, new_col) is not None:
                    if self.get_piece_on(new_row, new_col).color is piece.color:
                        break

                    moves.append([new_row, new_col])
                    break
                else:
                    moves.append([new_row, new_col])

            for i in range(1, 10):
                new_row = row - i
                new_col = col + i

                if not self.on_board(new_row, new_col):
                    break

                if self.get_piece_on(new_row, new_col) is not None:
                    if self.get_piece_on(new_row, new_col).color is piece.color:
                        break

                    moves.append([new_row, new_col])
                    break
                else:
                    moves.append([new_row, new_col])

            for i in range(1, 10):
                new_row = row - i
                new_col = col - i

                if not self.on_board(new_row, new_col):
                    break

                if self.get_piece_on(new_row, new_col) is not None:
                    if self.get_piece_on(new_row, new_col).color is piece.color:
                        break

                    moves.append([new_row, new_col])
                    break
                else:
                    moves.append([new_row, new_col])

        if piece.type == self._KING:
            if self.get_piece_on(row + 1, col + 1) is not None:
                if self.get_piece_on(row + 1, col + 1).color is not piece.color:
                    moves.append([row + 1, col + 1])
            else:
                if self.on_board(row + 1, col + 1):
                    moves.append([row + 1, col + 1])

            if self.get_piece_on(row + 1, col - 1) is not None:
                if self.get_piece_on(row + 1, col - 1).color is not piece.color:
                    moves.append([row + 1, col - 1])
            else:
                if self.on_board(row + 1, col - 1):
                    moves.append([row + 1, col - 1])

            if self.get_piece_on(row - 1, col + 1) is not None:
                if self.get_piece_on(row - 1, col + 1).color is not piece.color:
                    moves.append([row - 1, col + 1])
            else:
                if self.on_board(row - 1, col + 1):
                    moves.append([row - 1, col + 1])

            if self.get_piece_on(row - 1, col - 1) is not None:
                if self.get_piece_on(row - 1, col - 1).color is not piece.color:
                    moves.append([row - 1, col - 1])
            else:
                if self.on_board(row - 1, col - 1):
                    moves.append([row - 1, col - 1])

            if self.get_piece_on(row, col + 1) is not None:
                if self.get_piece_on(row, col + 1).color is not piece.color:
                    moves.append([row, col + 1])
            else:
                if self.on_board(row, col + 1):
                    moves.append([row, col + 1])

            if self.get_piece_on(row, col - 1) is not None:
                if self.get_piece_on(row, col - 1).color is not piece.color:
                    moves.append([row, col - 1])
            else:
                if self.on_board(row, col - 1):
                    moves.append([row, col - 1])

            if self.get_piece_on(row - 1, col) is not None:
                if self.get_piece_on(row - 1, col).color is not piece.color:
                    moves.append([row - 1, col])
            else:
                if self.on_board(row - 1, col):
                    moves.append([row - 1, col])

            if self.get_piece_on(row + 1, col) is not None:
                if self.get_piece_on(row + 1, col).color is not piece.color:
                    moves.append([row + 1, col])
            else:
                if self.on_board(row + 1, col):
                    moves.append([row + 1, col])

            if piece.color == 1:
                # Long castling
                if self.get_piece_on(row, col + 1) is None and self.get_piece_on(row,
                                                                                 col + 2) is None and self.get_piece_on(
                    row, col + 3) is None and self.long_castling_allowed:
                    moves.append([row, col + 2])

                # Short castling
                if self.get_piece_on(row, col - 1) is None and self.get_piece_on(row,
                                                                                 col - 2) is None and self.short_castling_allowed:
                    moves.append([row, col - 2])

        return moves

    def get_legal_moves(self, color):
        """Returns all the legal moves for the given color.
        (1 for white, -1 for black
        """
        moves = set()  # stores the legal moves.

        # Iterate through all the pieces
        for piece in self.internal_pieces:
            if piece.color == color:  # if it's the right color
                for move in self.get_moves(piece):
                    moves.add((piece.row, piece.col, move[0], move[1]))

        return moves

    def execute_move(self, move, color):
        """Perform the given move on the board
        """
        start_row, start_col, target_row, target_col = move

        # Get the piece
        current_piece = self.get_piece_on(start_row, start_col)

        if current_piece is None:
            print("current piece is none!")
            print("Game state is this:")
            print(self.board_rep)
            print()
            print("Attempted action was:")
            print(start_row, start_col, target_row, target_col)
            print("Making it a draw for now, but this should be figured out and fixed.")
            current_piece = self.internal_pieces[0]
            self.stupid_moves = 100000
            # return

        # See if there's a capture
        captured_piece = self.get_piece_on(target_row, target_col)

        if captured_piece is not None:
            self.internal_pieces = np.delete(self.internal_pieces, np.where(self.internal_pieces == captured_piece))
            # self.stupid_moves = 0

        # Check for the french move
        if self.en_passant_allowed and target_row is self.en_passant_target_row and target_col is self.en_passant_target_col and current_piece.type is self._PAWN:
            frenched_pawn = self.get_piece_on(self.en_passant_target_row, self.en_passant_target_col)
            self.internal_pieces = np.delete(self.internal_pieces, np.where(self.internal_pieces == frenched_pawn))

        if current_piece.type is self._KING and current_piece.color == 1:
            self.short_castling_allowed = False
            self.long_castling_allowed = False
        if current_piece.type is self._ROOK and current_piece.color == 1:
            if current_piece.col == 0:
                self.short_castling_allowed = False
            elif current_piece.col == 7:
                self.long_castling_allowed = False

        # Move piece
        current_piece.row = target_row
        current_piece.col = target_col

        # Check for castling
        # Long
        if current_piece.type is self._KING and target_col - start_col == 2 and current_piece.color == 1:
            corresponding_rook = self.get_piece_on(7, 0)
            if corresponding_rook is not None:
                corresponding_rook.row = 0
                corresponding_rook.col = 4
        # Short
        if current_piece.type is self._KING and target_col - start_col == -2 and current_piece.color == 1:
            corresponding_rook = self.get_piece_on(0, 0)
            if corresponding_rook is not None:
                corresponding_rook.row = 0
                corresponding_rook.col = 2

        # Check if the piece is a pawn that went two squares
        if current_piece.type is self._PAWN and abs(target_row - start_row) == 2:
            self.en_passant_allowed = True
            self.en_passant_target_col = target_col
            self.en_passant_target_row = int((target_row + start_row) / 2)
            self.en_passant_victim_col = target_col
            self.en_passant_victim_row = target_row
        else:
            self.en_passant_allowed = False

        # Check if the piece is a promoted pawn
        if current_piece.color == 1 and current_piece.row == 7 and current_piece.type == self._PAWN or current_piece.color == -1 and current_piece.row == 0 and current_piece.type == self._PAWN:
            current_piece.type = self._QUEEN  # for simplicity
            # self.stupid_moves = 0

        # Add gravity!!!!!!!
        for i in range(8):
            for piece in self.internal_pieces[:32]:
                if piece.type == self._PAWN:
                    continue

                below_row = piece.row + 1
                col = piece.col

                if self.get_piece_on(below_row, col) is None:
                    if self.on_board(below_row, col):
                        piece.row = below_row
                        piece.col = col

        # Next move time
        self.player_turn = -color

        self.stupid_moves += 0.1

        # Update board representation
        self.update_board_representation()

        return

    def is_tie(self):
        return self.stupid_moves > 10

    def get_winner(self):
        white_lost = True
        black_lost = True

        for piece in self.internal_pieces:
            if piece.type == self._KING and piece.color == 1:
                white_lost = False
            if piece.type == self._KING and piece.color == -1:
                black_lost = False

        if black_lost:
            return 1
        elif white_lost:
            return -1
        else:
            return 0
