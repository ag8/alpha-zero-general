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

        self.pieces = list()

        # Set up the initial board position
        for i in range(8):
            self.pieces.append(Piece(self._PAWN, 1, i, 1))
            self.pieces.append(Piece(self._PAWN, 6, i, -1))

        for i in [0, 7]:
            self.pieces.append(Piece(self._ROOK, i, 0, 1 if i is 0 else -1))
            self.pieces.append(Piece(self._KNIGHT, i, 1, 1 if i is 0 else -1))
            self.pieces.append(Piece(self._BISHOP, i, 2, 1 if i is 0 else -1))
            self.pieces.append(Piece(self._KING, i, 3, 1 if i is 0 else -1))
            self.pieces.append(Piece(self._QUEEN, i, 4, 1 if i is 0 else -1))
            self.pieces.append(Piece(self._BISHOP, i, 5, 1 if i is 0 else -1))
            self.pieces.append(Piece(self._KING, i, 6, 1 if i is 0 else -1))
            self.pieces.append(Piece(self._ROOK, i, 7, 1 if i is 0 else -1))

    # add [][] indexer syntax to the Board
    # def __getitem__(self, index):
    #     return self.pieces[index]

    def get_piece_on(self, row, col):
        for piece in self.pieces:
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
                    if row is not 6:
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
                    if row is not 1:
                        moves.append([row + 1, col])

                if row == 6:
                    if self.get_piece_on(row - 1, col) is None and self.get_piece_on(row - 2, col) is None:
                        moves.append([row - 2, col])

                if self.get_piece_on(row - 1, col + 1) is not None or (
                        row - 1 == self.en_passant_target_row and col + 1 == self.en_passant_target_col and self.en_passant_allowed):
                    if self.get_piece_on(row - 1, col + 1) is None:  # en passant
                        moves.append([row - 1, col + 1])
                    elif self.get_piece_on(row - 1, col + 1).color == -1:
                        moves.append([row - 1, col + 1])

                if self.get_piece_on(row - 1, col - 1) is not None or (
                        row - 1 == self.en_passant_target_row and col - 1 == self.en_passant_target_col and self.en_passant_allowed):
                    if self.get_piece_on(row - 1, col - 1) is None:  # en passant
                        moves.append([row - 1, col - 1])
                    elif self.get_piece_on(row - 1, col - 1).color == -1:
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
                        row, col + 3) is None and self.long_casting_allowed:
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
        for piece in self.pieces:
            if piece.color == color:  # if it's the right color
                for move in self.get_moves(piece):
                    moves.add([piece.row, piece.col, move[0], move[1]])

        return moves

    def execute_move(self, move, color):
        """Perform the given move on the board
        """
        start_row, start_col, target_row, target_col = move

        # Get the piece
        current_piece = self.get_piece_on(start_row, start_col)

        # See if there's a capture
        captured_piece = self.get_piece_on(target_row, target_col)

        if captured_piece is not None:
            self.pieces.remove(captured_piece)

        # Check for the french move
        if self.en_passant_allowed and target_row is self.en_passant_target_row and target_col is self.en_passant_target_col and current_piece.type is self._PAWN:
            frenched_pawn = self.get_piece_on(self.en_passant_target_row, self.en_passant_target_col)
            self.pieces.remove(frenched_pawn)

        if current_piece.type is self._KING:
            self.short_castling_allowed = False
            self.long_castling_allowed = False
        if current_piece.type is self._ROOK:
            if current_piece.col is 0:
                self.short_castling_allowed = False
            elif current_piece.col is 7:
                self.long_castling_allowed = False

        # Move piece
        current_piece.row = target_row
        current_piece.col = target_col

        # Check for castling
        # Long
        if current_piece.type is self._KING and target_col - start_col == 2:
            corresponding_rook = self.get_piece_on(7, 0)
            corresponding_rook.row = 0
            corresponding_rook.col = 4
        # Short
        if current_piece.type is self._KING and target_col - start_col == -2:
            corresponding_rook = self.get_piece_on(0, 0)
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

    def get_winner(self):
        white_lost = True
        black_lost = True

        for piece in self.pieces:
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
