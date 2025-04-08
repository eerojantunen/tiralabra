import sys
import pytest
from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))
import pytest
from board import Board
from tests.setup_board_for_test import *
from time import time
from evaluation import evaluate

def test_mate_in_two():
    """ Test if engine finds mate in two """
    current_board = Board()
    setup_mate_in_two_board(current_board)
    result = current_board.run_engine(99999999999,5)

    assert result[0][1][0] == (57,59, "WQ")
    current_board.make_move_board(result[0][1][0][0],result[0][1][0][1],result[0][1][0][2]) #make move for white
    current_board.make_move_board(result[0][1][1][0],result[0][1][1][1],result[0][1][1][2]) #make move for black
    result = current_board.run_engine(99999999999,5)

    assert result[0][1][0] == (13,29, "W")
    current_board.make_move_board(result[0][1][0][0],result[0][1][0][1],result[0][1][0][2]) #make move for white
    current_board.make_move_board(result[0][1][1][0],result[0][1][1][1],result[0][1][1][2]) #make move for black
    result = current_board.run_engine(99999999999,5)
    
    assert result[0][1][0] == (29,36, "W")
    current_board.make_move_board(result[0][1][0][0],result[0][1][0][1],result[0][1][0][2]) #make move for white

    assert evaluate(current_board) > 99000

def test_depth_five_time():
    """ Test if depth of 5 is reached in under 100 seconds - Performance test"""
    current_board = Board()
    setup_mate_in_two_board(current_board)
    start_time = time()
    result = current_board.run_engine(99999999999,5)
    total_time = time()-start_time
    assert total_time < 90

def test_pruning_amount():
    """ Test if amount of pruned moves reach benchmark amount - Performance test"""
    current_board = Board()
    setup_mate_in_two_board(current_board)
    result = current_board.run_engine(99999999999,5)
    prunes = result[1]
    assert (prunes > 12000)

def test_move_ordering_amount():
    """ Test if amount of move orders made reach benchmark amount - Performance test"""
    current_board = Board()
    setup_mate_in_two_board(current_board)
    result = current_board.run_engine(99999999999,4)
    assert result[2] > 470

def test_mate_in_two_with_sacrafice():
    """ Test if engine finds mate in two that involves a sacrifice"""
    current_board = Board()
    setup_mate_in_two_board_v2(current_board)
    result = current_board.run_engine(99999999999,5)
    
    assert result[0][1][0] == (4,36, "WR")
    current_board.make_move_board(result[0][1][0][0],result[0][1][0][1],result[0][1][0][2]) #make move for white
    current_board.final_print_board()
    current_board.make_move_board(51,36,"BN") #make move for black
    result = current_board.run_engine(99999999999,5)

    assert result[0][1][0] == (43,59, "WQ")
    current_board.make_move_board(result[0][1][0][0],result[0][1][0][1],result[0][1][0][2]) #make move for white
    current_board.make_move_board(60,59,"BK") #make move for black ("eats" queen but gets eaten ending game)
    result = current_board.run_engine(99999999999,5)

    assert result[0][1][0] == (3,59, "WR")
    current_board.make_move_board(result[0][1][0][0],result[0][1][0][1],result[0][1][0][2]) #make move for white
    current_board.final_print_board()
    assert evaluate(current_board) > 90000


