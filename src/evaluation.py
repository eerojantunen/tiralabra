from piece_data import *

piece_position_value_dict = {"W":white_pawn_weights,"WB":white_bishop_weights,"WN":white_knight_weights,
                             "WR":white_rook_weights, "WQ":white_queen_weights, "WK":white_king_weights,
                             "B":black_pawn_weights,"BB":black_bishop_weights,"BN":black_knight_weights,
                             "BR":black_rook_weights, "BQ":black_queen_weights, "BK":black_king_weights,}

def evaluate_piece_positions(self): #add all lists
    """ sums and returns positional value of all pieces by using pre-assigned weights"""
    evaluation = 0
    for key in self.piece_board:
        weight_dict = piece_position_value_dict[key]
        if len(self.piece_board[key]) > 0:
            for value in self.piece_board[key]:
                evaluation += weight_dict[value]
    return evaluation


def material_count(self):
    material_diff = 0
    for piece in self.piece_board:
        material_diff += piece_value[piece] * len(self.piece_board[piece])
    return material_diff

def evaluate(self):
    full_evaluation = 0
    full_evaluation += material_count(self)
    full_evaluation += evaluate_piece_positions(self)
    return full_evaluation