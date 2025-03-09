import sys
import pytest
from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))
import pytest
from board import Board
from tests.setup_board_for_test import *
from time import time

def test_mate_in_two():
    """ Test if engine finds mate in two """
    current_board = Board()
    setup_mate_in_two_board(current_board)
    result = current_board.run_engine(99999999999,5)
    assert result[0][0] == 99599

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
    assert (prunes > 21000)

def test_move_ordering_amount():
    """ Test if amount of move orders made reach benchmark amount - Performance test"""
    current_board = Board()
    setup_mate_in_two_board(current_board)
    result = current_board.run_engine(99999999999,4)
    assert result[2] > 470

