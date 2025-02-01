from piece_data import piece_representation, get_square_location_from_coordinates
import numpy as np


def knight_vision_bitboard(self,square_notation:str):
        """ returns a vision board of a knight on a specific square"""
        square_index = get_square_location_from_coordinates(square_notation)
        print(square_index)
        row, col = self.row_col_from_square_notation(square_notation)
        vision_board = np.uint64(0)
        knight_moves = [(2,1),(2,-1),(-2,1),(-2,-1),(1,2),(1,-2),(-1,2),(-1,-2)] #possible knight moves in row column changes
        for move_row, move_col in knight_moves:
            row_change = move_row + row
            col_change = move_col + col
            if 0 <= row_change < 8 and 0 <= col_change < 8:
                offset = move_row * 8 + move_col
                vision_board = np.uint64(vision_board | 1 << (square_index + offset))

        return vision_board, "WN", square_index

def north_ray_empty(self, square_notation:str):
    """ returns north ray vision bitboard from given square"""
    square_index = get_square_location_from_coordinates(square_notation)
    vision_board = np.uint64(0)
    for i in range(0,8):
        if square_index + i*8 + 8> 64:
            break
        vision_board = np.uint64(vision_board | 1 << np.uint64(square_index+i*8+8))
    return vision_board, "WN", square_index

def south_ray_empty(self, square_notation:str):
    """ returns south ray vision bitboard from given square"""
    square_index = get_square_location_from_coordinates(square_notation)
    vision_board = np.uint64(0)
    for i in range(0,8):
        if square_index - i*8 - 8 < 0:
            break
        vision_board = np.uint64(vision_board | 1 << np.uint64(square_index - i*8 - 8))
    return vision_board, "WN", square_index

def west_ray_empty(self,square_notation:str):
    """ returns west ray vision bitboard from given square"""
    square_index = get_square_location_from_coordinates(square_notation)
    col = self.row_col_from_square_notation(square_notation)[1]
    vision_board = np.uint64(0)
    for i in range(col):
        vision_board = np.uint64(vision_board | 1 << np.uint64(square_index-i-1))
    return vision_board, "WN", square_index

def east_ray_empty(self,square_notation:str):
    """ returns east ray vision bitboard from given square"""
    square_index = get_square_location_from_coordinates(square_notation)
    col = self.row_col_from_square_notation(square_notation)[1]
    vision_board = np.uint64(0)
    for i in range(7-col):
        vision_board = np.uint64(vision_board | 1 << np.uint64(square_index+i+1))
    return vision_board, "WN", square_index

def north_west_ray_empty(self,square_notation:str):
    """ returns north-west diagonal ray vision bitboard from given square"""
    square_index = get_square_location_from_coordinates(square_notation)
    row, col = self.row_col_from_square_notation(square_notation)
    vision_board = np.uint64(0)
    
