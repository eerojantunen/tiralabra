import sys
import pytest
from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))
import pytest
from board import Board
from vision_boards import *
from tests.setup_board_for_test import *
from annotation_data import *
from moves import *
def test_adding_material():
    board = Board()
    board.add_material("WBg3")
    board.add_material("Bh6")
    board.add_material("Wa3")
    board.add_material("WNb1")
    board.add_material("WQh5")
    board.add_material("WKf8")
    board.add_material("BBd4")
    board.add_material("BNh1")
    board.add_material("BQh8")
    board.add_material("BKe2")
    board.add_material("BRe1")
    board.add_material("WRe3")
    assert board.piece_board == {'W': {16}, 'WR': {20}, 'WN': {1}, 'WB': {22},
                                'WQ': {39}, 'WK': {61}, 'B': {47}, 'BR': {4},
                                'BN': {7}, 'BB': {27}, 'BQ': {63}, 'BK': {12}}
    
def test_white_rook_legal_moves():
    """ Test if white rook legal move generation is correct """
    current_board = Board()
    setup_vision_ray_test_board(current_board)
    current_board.add_material("WRd4")
    legal_move_bitboard = get_legal_moves_rook(current_board,"W","d4")
    assert legal_move_bitboard == 8831359256576


def test_black_rook_legal_moves():
    """ Test if black rook legal move generation is correct """
    current_board = Board()
    setup_vision_ray_test_board(current_board)
    current_board.add_material("BRd4")
    legal_move_bitboard = get_legal_moves_rook(current_board,"B","d4")
    assert legal_move_bitboard == 36306419712

def test_white_queen_legal_moves():
    """ Test if white queen legal move generation is correct """
    current_board = Board()
    setup_vision_ray_test_board(current_board)
    current_board.add_material("WQd4")
    legal_move_bitboard = get_legal_moves_queen(current_board,"W","d4")
    assert legal_move_bitboard == 292591259887616

def test_black_queen_legal_moves():
    """ Test if black queen legal move generation is correct """
    current_board = Board()
    setup_vision_ray_test_board(current_board)
    current_board.add_material("BQd4")
    legal_move_bitboard = get_legal_moves_queen(current_board,"B","d4")
    assert legal_move_bitboard == 37505602158592

def test_white_king_legal_moves():
    """ Test if white king legal move generation is correct """
    current_board = Board()
    setup_vision_ray_test_board(current_board)
    current_board.add_material("WKc1")
    legal_move_bitboard = get_legal_moves_king(current_board,"W","c1")
    assert legal_move_bitboard == 2562

def test_black_king_legal_moves():
    """ Test if black king legal move generation is correct """
    current_board = Board()
    setup_vision_ray_test_board(current_board)
    current_board.add_material("BKc1")
    legal_move_bitboard = get_legal_moves_king(current_board,"B","c1")
    assert legal_move_bitboard == 1546

def test_white_bishop_legal_moves():
    """ Test if white bishop legal move generation is correct """
    current_board = Board()
    setup_vision_ray_test_board(current_board)
    current_board.add_material("WBd4")
    legal_move_bitboard = get_legal_moves_bishop(current_board,"W","d4")
    assert legal_move_bitboard == 283759900631040

def test_black_bishop_legal_moves():
    """ Test if black bishop legal move generation is correct """
    current_board = Board()
    setup_vision_ray_test_board(current_board)
    current_board.add_material("BBd4")
    legal_move_bitboard = get_legal_moves_bishop(current_board,"B","d4")
    assert legal_move_bitboard == 37469295738880

def test_white_knight_legal_moves():
    """ Test if white knight legal move generation is correct """
    current_board = Board()
    setup_vision_ray_test_board(current_board)
    current_board.add_material("WNd4")
    legal_move_bitboard = get_legal_moves_knight(current_board,"W","d4")
    assert legal_move_bitboard == 22136261574656

def test_black_knight_legal_moves():
    """ Test if black knight legal move generation is correct """
    current_board = Board()
    setup_vision_ray_test_board(current_board)
    current_board.add_material("BNd4")
    legal_move_bitboard = get_legal_moves_knight(current_board,"B","d4")
    assert legal_move_bitboard == 17600778212352

def test_black_pawn_legal_moves():
    """ Test if black pawns legal move generation is correct """
    current_board = Board()
    setup_vision_ray_test_board(current_board)
    current_board.add_material("Be4")
    legal_move_bitboard = get_legal_black_pawn_moves(current_board,"B","e4")
    assert legal_move_bitboard == 3145728

def test_white_pawn_legal_moves():
    """ Test if white pawns legal move generation is correct """
    current_board = Board()
    setup_vision_ray_test_board(current_board)
    current_board.add_material("We4")
    legal_move_bitboard = get_legal_white_pawn_moves(current_board,"W","e4")
    assert legal_move_bitboard == 206158430208

def test_all_moves_white():
    """ Test if all moves for white returns all legal moves for white"""
    current_board = Board()
    setup_vision_ray_test_board(current_board)
    current_board.add_material("WKa1")
    current_board.add_material("BKa8")
    all_legal = all_moves(current_board,"W")
    assert all_legal == [(12, 20, 'W'), (12, 28, 'W'), (45, 53, 'W'), (45, 54, 'W'), (21, 29, 'W'),
                        (30, 37, 'W'), (30, 38, 'W'), (0, 1, 'WK'), (0, 8, 'WK'), (0, 9, 'WK')]

def test_all_moves_black():
    """ Test if all moves for black returns all legal moves for black"""
    current_board = Board()
    setup_vision_ray_test_board(current_board)
    current_board.add_material("WKa1")
    current_board.add_material("BKa8")
    all_legal = all_moves(current_board,"B")
    assert all_legal == [(37, 29, 'B'), (37, 30, 'B'), (42, 34, 'B'), (43, 35, 'B'), (13, 5, 'B'),
                         (48, 32, 'B'), (48, 40, 'B'), (54, 38, 'B'), (54, 45, 'B'), (54, 46, 'B'),
                         (25, 17, 'B'), (31, 23, 'B'), (56, 49, 'BK'), (56, 57, 'BK')]

def test_moving():
    """ Test if making a move works as intended """
    current_board = Board()
    setup_vision_ray_test_board(current_board)
    current_board.make_move_board(45,53,"W")
    current_board.make_move_board(48,40,"B")
    board_state = current_board.get_board_state_hash()
    assert board_state == 603496784414915592

def test_taking():
    """ Test if making a move that is a take is registered correctly"""
    current_board = Board()
    setup_vision_ray_test_board(current_board)
    current_board.make_move_board(45,54,"W")
    current_board.make_move_board(37,30,"B")
    current_board.make_move_board(54,62,"W")
    board_state = current_board.get_board_state_hash()
    assert board_state == 5188441443104209928

def test_illegal_move():
    current_board = Board()
    setup_vision_ray_test_board(current_board)
    #x=make_move(current_board,45,54,"W")
    move_1 = is_legal(current_board,45,54,"W")
    move_2 = is_legal(current_board,45,52,"W")
    move_3 = is_legal(current_board,2,3,"WR")
    assert move_1 == True
    assert move_2 == False
    assert move_3 == False

test_illegal_move()