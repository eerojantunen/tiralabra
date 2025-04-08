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
    """ Test if evaluation is equal on board setup """
    current_board = Board()
    current_board.setup()
    evaluation = evaluate(current_board)
    assert evaluation == 0

def test_evaluation_empty_board():
    """ Test if evaluation is even with no material """
    current_board = Board()
    evaluation = evaluate(current_board)
    assert evaluation == 0


def test_evaluation_on_mate_two_board():
    """ Test if evaluation is calculated correctly on mate two board """
    current_board = Board()
    setup_mate_in_two_board(current_board)
    evaluation = evaluate(current_board)
    assert evaluation == -70
    
def test_evaluation_on_earlygame_board():
    """ Test if evaluation is calculated correctly on earlygame board """
    current_board = Board()
    setup_earlygame_board(current_board)
    evaluation = evaluate(current_board)
    print(evaluation)
    current_board.final_print_board()
    assert evaluation == 50

def test_evaluation_on_midgame_board():
    """ Test if evaluation is calculated correctly on midgame board """
    current_board = Board()
    setup_midgame_board(current_board)
    evaluation = evaluate(current_board)
    print(evaluation)
    current_board.final_print_board()
    assert evaluation == 370

