from piece_data import piece_representation, get_square_location_from_coordinates
import numpy as np
from annotation_data import alg_notation_to_index, index_to_alg_notation


#TODO
#why are rays returning "WN" ??? :DDD
#+ is square index returning necessary
def north_ray_empty(self, square_notation:str):
    """ returns north ray vision bitboard from given square"""
    square_index = alg_notation_to_index[square_notation]
    vision_board = np.uint64(0)
    for i in range(0,8):
        if square_index + i*8 + 8> 64:
            break
        vision_board = np.uint64(vision_board | 1 << np.uint64(square_index+i*8+8))
    return np.uint64(vision_board), "WN", square_index

def south_ray_empty(self, square_notation:str):
    """ returns south ray vision bitboard from given square"""
    square_index = alg_notation_to_index[square_notation]
    vision_board = np.uint64(0)
    for i in range(0,8):
        if square_index - i*8 - 8 < 0:
            break
        vision_board = np.uint64(vision_board | 1 << np.uint64(square_index - i*8 - 8))
    return np.uint64(vision_board), "WN", square_index

def west_ray_empty(self,square_notation:str):
    """ returns west ray vision bitboard from given square"""
    square_index = alg_notation_to_index[square_notation]
    col = self.row_col_from_square_notation(square_notation)[1]
    vision_board = np.uint64(0)
    for i in range(col):
        vision_board = np.uint64(vision_board | 1 << np.uint64(square_index-i-1))
    return np.uint64(vision_board), "WN", square_index

def east_ray_empty(self,square_notation:str):
    """ returns east ray vision bitboard from given square"""
    square_index = alg_notation_to_index[square_notation]
    col = self.row_col_from_square_notation(square_notation)[1]
    vision_board = np.uint64(0)
    for i in range(7-col):
        vision_board = np.uint64(vision_board | 1 << np.uint64(square_index+i+1))
    return np.uint64(vision_board), "WN", square_index

def south_west_ray_empty(self,square_notation:str):
    """ returns south-west diagonal ray vision bitboard from given square"""
    square_index = alg_notation_to_index[square_notation]
    row, col = self.row_col_from_square_notation(square_notation)
    vision_board = np.uint64(0)
    for i in range(min(row,col)):
        vision_board = np.uint64(vision_board | 1 << np.uint(square_index -9 * (i+1)))
    return np.uint64(vision_board), "WN", square_index

def south_east_ray_empty(self,square_notation:str):
    """ returns south-west diagonal ray vision bitboard from given square"""
    square_index = alg_notation_to_index[square_notation]
    row, col = self.row_col_from_square_notation(square_notation)
    vision_board = np.uint64(0)
    for i in range(min(row,7-col)):
        vision_board = np.uint64(vision_board | 1 << np.uint(square_index - 7 * (i+1)))
    return np.uint64(vision_board), "WN", square_index

def north_west_ray_empty(self,square_notation:str):
    """ returns north-west diagonal ray vision bitboard from given square"""
    square_index = alg_notation_to_index[square_notation]
    row, col = self.row_col_from_square_notation(square_notation)
    vision_board = np.uint64(0)
    for i in range(min(7-row,col)):
        vision_board = np.uint64(vision_board | 1 << np.uint(square_index + 7 * (i+1)))
    return np.uint64(vision_board), "WN", square_index

def north_east_ray_empty(self,square_notation:str):
    """ returns north-east diagonal ray vision bitboard from given square"""
    square_index = alg_notation_to_index[square_notation]
    row, col = self.row_col_from_square_notation(square_notation)
    vision_board = np.uint64(0)
    for i in range(min(7-row,7-col)):
        vision_board = np.uint64(vision_board | 1 << np.uint(square_index +9 * (i+1)))
    return np.uint64(vision_board), "WN", square_index


def king_vision_board_empty(self,square_notation):
    square_index = alg_notation_to_index[square_notation]
    king_moves = [-9,-8,-7,-1,1,7,8,9]
    king_vision_board_empty = np.uint64(0)
    col = square_index % 8

    for move in king_moves:
        target = square_index+move
        if  0 <= target <= 63:
            target_col = (square_index+move) % 8
            if abs(target_col - col) <= 1:
                king_vision_board_empty = np.uint64(king_vision_board_empty | 1 << np.uint64(square_index + move))
    return king_vision_board_empty

def black_pawn_vision_board_empty(self,square_notation): # EI TOIMI TEE SAMA KU WHITE PAWN FIX ASAP
    square_index = alg_notation_to_index[square_notation]
    pawn_moves = [-8]
    pawn_vision_board_empty = np.uint64(0)
    two_move_vision_ray = np.uint64(0)

    if int(square_notation[1]) == 1:
        #todo promote queen
        return np.uint64(0) #placeholder 
    if int(square_notation[1]) == 7:
        two_move_vision_ray = np.uint64(two_move_vision_ray | 1 << np.uint64(square_index-16))
    for move in pawn_moves:
        pawn_vision_board_empty = np.uint64(pawn_vision_board_empty | 1 << np.uint64(square_index+move))
    return pawn_vision_board_empty, two_move_vision_ray

def black_pawn_attack(self, square_notation):
    square_index = alg_notation_to_index[square_notation]
    pawn_attack_board_empty = np.uint64(0)
    if int(square_notation[1]) > 1:
        if square_notation[0] != "h":
            pawn_attack_board_empty = np.uint64(pawn_attack_board_empty | 1 << np.uint64(square_index-7))
        if square_notation[0] != "a":
            pawn_attack_board_empty = np.uint64(pawn_attack_board_empty | 1 << np.uint64(square_index-9))
        return pawn_attack_board_empty
    return np.uint64(0)

def white_pawn_vision_board_empty(self,square_notation):
    #TARKISTA
    square_index = alg_notation_to_index[square_notation]
    pawn_moves = [8]
    pawn_vision_board_empty = np.uint64(0)
    two_move_vision_ray = np.uint64(0)
    if int(square_notation[1]) == 8:
        #todo promote queen
        return np.uint64(0) #placeholder 
    if int(square_notation[1]) == 2: # tarkasta onko oikei :)
        two_move_vision_ray = np.uint64(two_move_vision_ray | 1 << np.uint64(square_index+16))
    for move in pawn_moves:
        pawn_vision_board_empty = np.uint64(pawn_vision_board_empty | 1 << np.uint64(square_index+move))
    return pawn_vision_board_empty, two_move_vision_ray


def white_pawn_attack(self,square_notation):
    square_index = alg_notation_to_index[square_notation]
    pawn_attack_board_empty = np.uint64(0)
    if int(square_notation[1]) < 8:
        if square_notation[0] != "a":
            pawn_attack_board_empty = np.uint64(pawn_attack_board_empty | 1 << np.uint64(square_index+7))
        if square_notation[0] != "h":
            pawn_attack_board_empty = np.uint64(pawn_attack_board_empty | 1 << np.uint64(square_index+9))
        return pawn_attack_board_empty
    return np.uint64(0)