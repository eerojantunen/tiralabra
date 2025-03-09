import sys
import pytest
from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))
import pytest
from board import Board
from tests.setup_board_for_test import *
from evaluation import *

def test_evaluation_equal_at_beginning():
    """ Test if engine finds mate in two """
    current_board = Board()
    current_board.setup()
    evaluation = evaluate(current_board)
    assert evaluation == 0

def test_piece_position_evaluation():
    current_board = Board()
    current_board.setup()
    evaluation = evaluate(current_board)
    