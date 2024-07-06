import numpy as np

# python -m venv venv
# source venv/bin/activate

class ChessEngine:
    def __init__(self):
        self.board = self.initalize_board()
        self.white_king_moved = False
        self.black_king_moved = False
        self.white_rooks_moved = [False, False]  # [queenside, kingside]
        self.black_rooks_moved = [False, False]  # [queenside, kingside]

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
        print('  a b c d e f g h')
        for y in range(7, -1, -1):
            print(f"{y+1} {' '.join(piece_symbols[self.board[y, x]] for x in range(8))} {y+1}")
        print('  a b c d e f g h')

    def is_valid_position(self, x, y):
        return 'a' <= x <= 'h' and 1 <= y <= 8

    def get_pawn_moves(self, x, y, color):
        moves = []
        x_idx = ord(x) - ord('a')
        y_idx = y - 1
        direction = 1 if color == 'white' else -1
        
        # Move forward
        if self.is_valid_position(x, y + direction) and self.board[y_idx + direction, x_idx] == 0:
            moves.append((x, y + direction))
            
            # Double move from starting position
            if (color == 'white' and y == 2) or (color == 'black' and y == 7):
                if self.board[y_idx + 2*direction, x_idx] == 0:
                    moves.append((x, y + 2*direction))
        
        # Capture diagonally
        for dx in [-1, 1]:
            new_x = chr(ord(x) + dx)
            if self.is_valid_position(new_x, y + direction):
                if color == 'white' and self.board[y_idx + direction, x_idx + dx] < 0:
                    moves.append((new_x, y + direction))
                elif color == 'black' and self.board[y_idx + direction, x_idx + dx] > 0:
                    moves.append((new_x, y + direction))
        
        return moves
    
    def get_knight_moves(self, x, y):
        moves = []
        knight_moves = [
            (2, 1), (1, 2), (-1, 2), (-2, 1),
            (-2, -1), (-1, -2), (1, -2), (2, -1)
        ]
        for dx, dy in knight_moves:
            new_x = chr(ord(x) + dx)
            new_y = y + dy
            if self.is_valid_position(new_x, new_y):
                x_idx, y_idx = ord(new_x) - ord('a'), new_y - 1
                if self.board[y_idx, x_idx] * self.board[y - 1, ord(x) - ord('a')] <= 0:  # Empty or opponent's piece
                    moves.append((new_x, new_y))
        return moves

    def get_bishop_moves(self, x, y):
        return self.get_diagonal_moves(x, y)

    def get_rook_moves(self, x, y):
        return self.get_straight_moves(x, y)

    def get_queen_moves(self, x, y):
        return self.get_diagonal_moves(x, y) + self.get_straight_moves(x, y)

    def get_diagonal_moves(self, x, y):
        moves = []
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        for dx, dy in directions:
            for i in range(1, 8):
                new_x = chr(ord(x) + i*dx)
                new_y = y + i*dy
                if not self.is_valid_position(new_x, new_y):
                    break
                x_idx, y_idx = ord(new_x) - ord('a'), new_y - 1
                if self.board[y_idx, x_idx] == 0:
                    moves.append((new_x, new_y))
                elif self.board[y_idx, x_idx] * self.board[y - 1, ord(x) - ord('a')] < 0:  # Opponent's piece
                    moves.append((new_x, new_y))
                    break
                else:
                    break
        return moves

    def get_straight_moves(self, x, y):
        moves = []
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for dx, dy in directions:
            for i in range(1, 8):
                new_x = chr(ord(x) + i*dx)
                new_y = y + i*dy
                if not self.is_valid_position(new_x, new_y):
                    break
                x_idx, y_idx = ord(new_x) - ord('a'), new_y - 1
                if self.board[y_idx, x_idx] == 0:
                    moves.append((new_x, new_y))
                elif self.board[y_idx, x_idx] * self.board[y - 1, ord(x) - ord('a')] < 0:  # Opponent's piece
                    moves.append((new_x, new_y))
                    break
                else:
                    break
        return moves

    def get_basic_king_moves(self, x, y):
        moves = []
        king_moves = [
            (1, 0), (1, 1), (0, 1), (-1, 1),
            (-1, 0), (-1, -1), (0, -1), (1, -1)
        ]
        for dx, dy in king_moves:
            new_x = chr(ord(x) + dx)
            new_y = y + dy
            if self.is_valid_position(new_x, new_y):
                x_idx, y_idx = ord(new_x) - ord('a'), new_y - 1
                if self.board[y_idx, x_idx] * self.board[y - 1, ord(x) - ord('a')] <= 0:  # Empty or opponent's piece
                    moves.append((new_x, new_y))
        return moves
    
    def is_square_attacked(self, x, y, attacking_color):
        for i in range(8):
            for j in range(8):
                piece = self.board[i, j]
                if (piece > 0 and attacking_color == 'black') or (piece < 0 and attacking_color == 'white'):
                    moves = self.get_basic_moves(chr(ord('a') + j), i + 1)
                    if (x, y) in moves:
                        return True
        return False
    
    def can_castle(self, color, side):
        y = 1 if color == 'white' else 8
        king_x = 'e'
        
        # Check if king or rook has moved
        if color == 'white':
            if self.white_king_moved or self.white_rooks_moved[0 if side == 'queenside' else 1]:
                return False
        else:
            if self.black_king_moved or self.black_rooks_moved[0 if side == 'queenside' else 1]:
                return False

        # Check if squares between king and rook are empty
        if side == 'queenside':
            empty_squares = ['d', 'c', 'b']
            rook_x = 'a'
        else:  # kingside
            empty_squares = ['f', 'g']
            rook_x = 'h'

        for x in empty_squares:
            if self.board[y-1, ord(x)-ord('a')] != 0:
                return False

        # Check if king is in check or passes through attacked squares
        enemy_color = 'black' if color == 'white' else 'white'
        check_squares = [king_x] + empty_squares[:2]  # King's current square and the two it passes through
        for x in check_squares:
            if self.is_square_attacked(x, y, enemy_color):
                return False

        return True
    
    def get_basic_moves(self, x, y):
        x_idx = ord(x) - ord('a')
        y_idx = y - 1
        piece = self.board[y_idx, x_idx]
        color = 'white' if piece > 0 else 'black'
        
        if abs(piece) == 1:  # Pawn
            return self.get_pawn_moves(x, y, color)
        elif abs(piece) == 2:  # Knight
            return self.get_knight_moves(x, y)
        elif abs(piece) == 3:  # Bishop
            return self.get_bishop_moves(x, y)
        elif abs(piece) == 4:  # Rook
            return self.get_rook_moves(x, y)
        elif abs(piece) == 5:  # Queen
            return self.get_queen_moves(x, y)
        elif abs(piece) == 6:  # King
            return self.get_basic_king_moves(x, y)
        else:
            return []
        
    def get_moves(self, x, y):
        moves = self.get_basic_moves(x, y)
        if abs(self.board[y-1, ord(x)-ord('a')]) == 6:  # If it's a king
            color = 'white' if self.board[y-1, ord(x)-ord('a')] > 0 else 'black'
            # Check castling
            if self.can_castle(color, 'kingside'):
                moves.append(('g', y))
            if self.can_castle(color, 'queenside'):
                moves.append(('c', y))
        return moves

    def make_move(self, from_x, from_y, to_x, to_y):
        piece = self.board[from_y-1, ord(from_x)-ord('a')]
        self.board[to_y-1, ord(to_x)-ord('a')] = piece
        self.board[from_y-1, ord(from_x)-ord('a')] = 0

        # Update king and rook move flags
        if abs(piece) == 6:  # King
            if piece > 0:
                self.white_king_moved = True
            else:
                self.black_king_moved = True

            # Handle castling
            if abs(ord(to_x) - ord(from_x)) == 2:
                if to_x == 'g':  # Kingside
                    rook_from, rook_to = ('h', 'f')
                else:  # Queenside
                    rook_from, rook_to = ('a', 'd')
                self.make_move(rook_from, from_y, rook_to, to_y)

        elif abs(piece) == 4:  # Rook
            if from_x == 'a':  # Queenside
                if piece > 0:
                    self.white_rooks_moved[0] = True
                else:
                    self.black_rooks_moved[0] = True
            elif from_x == 'h':  # Kingside
                if piece > 0:
                    self.white_rooks_moved[1] = True
                else:
                    self.black_rooks_moved[1] = True