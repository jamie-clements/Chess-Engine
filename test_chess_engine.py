# test_chess_engine.py

from chess_engine import ChessEngine

def test_initial_board():
    engine = ChessEngine()
    print("Initial board:")
    engine.print_board()

def test_pawn_moves():
    engine = ChessEngine()
    print("\nPossible moves for white pawn at e2:")
    print(engine.get_moves('e', 2))
    print("\nPossible moves for black pawn at e7:")
    print(engine.get_moves('e', 7))

def test_knight_moves():
    engine = ChessEngine()
    print("\nPossible moves for white knight at b1:")
    print(engine.get_moves('b', 1))

def test_bishop_moves():
    engine = ChessEngine()
    # Clear some spaces for the bishop
    engine.board[1, 3] = 0  # Remove pawn at d2
    print("\nPossible moves for white bishop at c1:")
    print(engine.get_moves('c', 1))

def test_rook_moves():
    engine = ChessEngine()
    # Clear some spaces for the rook
    engine.board[1, 0] = 0  # Remove pawn at a2
    print("\nPossible moves for white rook at a1:")
    print(engine.get_moves('a', 1))

def test_queen_moves():
    engine = ChessEngine()
    # Clear some spaces for the queen
    engine.board[1, 3] = 0  # Remove pawn at d2
    print("\nPossible moves for white queen at d1:")
    print(engine.get_moves('d', 1))

def test_king_moves():
    engine = ChessEngine()
    print("\nPossible moves for white king at e1:")
    print(engine.get_moves('e', 1))

def test_castling():
    engine = ChessEngine()
    print("\nPossible moves for white king at e1 (should include castling):")
    print(engine.get_moves('e', 1))

    # Clear the path for castling
    engine.board[0, 5] = 0  # Remove bishop at f1
    engine.board[0, 6] = 0  # Remove knight at g1

    print("\nPossible moves for white king at e1 (should now include kingside castling):")
    print(engine.get_moves('e', 1))

    # Make the castling move
    engine.make_move('e', 1, 'g', 1)
    print("\nBoard after white kingside castle:")
    engine.print_board()

def run_all_tests():
    test_initial_board()
    test_pawn_moves()
    test_knight_moves()
    test_bishop_moves()
    test_rook_moves()
    test_queen_moves()
    test_king_moves()
    test_castling()

if __name__ == "__main__":
    run_all_tests()