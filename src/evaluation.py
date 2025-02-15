from piece_data import *


def evaluate_position(self):
    pass


def material_count(self):
    material_diff = 0
    for piece in self.piece_board: #tarkista self.piece_board
        material_diff += piece_value[piece] * len(self.piece_board[piece])
    return material_diff

def evaluate(self):
    full_evaluation = 0
    full_evaluation += material_count(self)
    return full_evaluation