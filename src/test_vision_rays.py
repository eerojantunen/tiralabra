import pytest
import numpy as np
from vision_boards import *
from temp import Board

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
    
def test_white_rook_vision_board():
    board = Board()
    