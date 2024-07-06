import numpy as np

# python -m venv venv
# source venv/bin/activate

class ChessEngine:
    def __init__(self):
        self.board = self.initalize_board()

    def initalize_board(self):
        # Initalize 8x8 chess board
        # 0 represents empty squares
        # Positive numbers for white pieces, negative for black
        # 1: Pawn, 2: Knight, 3: Bishop, 4: Rook, 5: Queen, 6:King
        board = np.zeros((8,8), dtype=int)

        # Set up pawns
        board[1, :] = 1 # White pawns
        board[6, :] = -1 # Black pawns

        # Set up other pieces
        pieces = [4, 2, 3, 5, 6, 3, 2, 4]
        board[0, :] = pieces # White pieces
        board[7, :] = [-p for p in pieces] # Black pieces 

        return board
    
    def print_board(self):
        # Display current board state
        piece_symbols = {
            0: '.',
            1: '♙', -1: '♟',
            2: '♘', -2: '♞',
            3: '♗', -3: '♝',
            4: '♖', -4: '♜',
            5: '♕', -5: '♛',
            6: '♔', -6: '♚'
        }
        for row in self.board:
            print(' '.join(piece_symbols[piece] for piece in row))
    

    def is_valid_position(self, row, col):
        # Helper to check if a given position is on board
        return 0 <= row < 8 and 0 <= col < 8

# Printing of inital board test
if __name__ == "__main__":
    engine = ChessEngine()
    engine.print_board()

    