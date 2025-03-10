from piece_data import piece_representation, get_square_location_from_coordinates
from vision_rays import *
from annotation_data import alg_notation_to_index, index_to_alg_notation
import numpy as np
#add magic bitboards (?)

def occupied_bitboard(bitboards):
    """ Returns bitboard of all sqaures """
    #should be obselete when automatic occupancy updating done  ---- if deleted update board.full_board --- should improve speed
    occupied_bitboard = np.uint64(0)
    for i in bitboards:
        occupied_bitboard = occupied_bitboard | i
    return occupied_bitboard

def get_enemy_pieces(self,color:str):
    """ Returns enemy bitboards according to given color in string from W / B """
    color_to_board_dict = {"W":self.black_bitboards,"B":self.white_bitboards}
    return color_to_board_dict[color]

def get_friendly_pieces(self,color:str):
    """ Returns friendly bitboards according to given color in string from W / B """
    color_to_board_dict = {"B":self.black_bitboards,"W":self.white_bitboards}
    return color_to_board_dict[color]

    
def knight_vision_bitboard(self,square_notation:str):
        """ Returns a vision board of a knight on a specific square"""
        square_index = get_square_location_from_coordinates(square_notation)
        row, col = self.row_col_from_square_notation(square_notation)
        vision_board = np.uint64(0)
        knight_moves = [(2,1),(2,-1),(-2,1),(-2,-1),(1,2),(1,-2),(-1,2),(-1,-2)] #possible knight moves in row column changes
        for move_row, move_col in knight_moves:
            row_change = move_row + row
            col_change = move_col + col
            if 0 <= row_change < 8 and 0 <= col_change < 8:
                offset = move_row * 8 + move_col
                vision_board = np.uint64(vision_board | 1 << (square_index + offset))

        return np.uint64(vision_board), "WN", square_index

def lsb_forward(bitboard):
    """ Returns least significant bit as index"""
    if bitboard == 0:
        return -1  
    return (int(bitboard) & - int(bitboard)).bit_length() - 1

def msb_backward(bitboard):
    """ Returns most significant bit as index"""
    if bitboard == 0:
        return -1
    return int(bitboard).bit_length() - 1

def get_blocked_rays_bishop(self, square_notation):
    """ Returns vision bitboard of bishop with blocks accounted for """
    blockers = np.uint64(0)
    intersection_board = occupied_bitboard(self.all_bitboards) #improve

    """ Get south west ray with blocks """
    south_west_ray = south_west_ray_empty(self,square_notation)[0]
    intersections = south_west_ray & intersection_board
    if intersections != -1:
        first_block = msb_backward(intersections)
        if first_block != -1:
            blockers |= np.uint64(1) << first_block
            reflex_ray = north_east_ray_empty(self,index_to_alg_notation[first_block])[0]
            south_west_ray &= reflex_ray

    """ Get south east ray with blocks """
    south_east_ray = south_east_ray_empty(self,square_notation)[0]
    intersections = south_east_ray & intersection_board
    if intersections != -1:
        first_block = msb_backward(intersections)
        if first_block != -1:
            blockers |= np.uint64(1) << first_block
            reflex_ray = north_west_ray_empty(self,index_to_alg_notation[first_block])[0]
            south_east_ray &= reflex_ray

    """ Get north west ray with blocks """
    north_west_ray = north_west_ray_empty(self,square_notation)[0]
    intersections = north_west_ray & intersection_board
    if intersections != -1:
        first_block = lsb_forward(intersections)
        if first_block != -1:
            blockers |= np.uint64(1) << first_block
            reflex_ray = south_east_ray_empty(self,index_to_alg_notation[first_block])[0]
            north_west_ray &= reflex_ray

    """  Get north east ray with blocks """
    north_east_ray = north_east_ray_empty(self,square_notation)[0]
    intersections = north_east_ray & intersection_board
    if intersections != -1:
        first_block = lsb_forward(intersections)
        if first_block != -1:
            blockers |= np.uint64(1) << first_block
            reflex_ray = south_west_ray_empty(self,index_to_alg_notation[first_block])[0]
            north_east_ray &= reflex_ray

    vision_bitboard = north_east_ray | north_west_ray | south_east_ray | south_west_ray
    return vision_bitboard, np.uint64(blockers)

def get_blocked_rays_rook(self, square_notation):
    """ Returns rook vision board with blocks from a given square notation
        and a bitboard of all blockers """
    blockers = np.uint64(0)
    intersection_board = occupied_bitboard(self.all_bitboards) 
   
    """ Get north ray with blocks """
    north_ray = north_ray_empty(self,square_notation)[0]
    intersections = north_ray & intersection_board
    if intersections != -1:
        first_block = lsb_forward(intersections)
        if first_block != -1:
            blockers |= np.uint64(1) << first_block
            reflex_ray = south_ray_empty(self,index_to_alg_notation[first_block])[0]
            north_ray &= reflex_ray

           
    """ Get east ray with blocks """
    east_ray = east_ray_empty(self,square_notation)[0]
    intersections = east_ray & intersection_board
    if intersections != -1:
        first_block = lsb_forward(intersections)
        if first_block != -1:
            blockers |= np.uint64(1) << first_block
            reflex_ray = west_ray_empty(self,index_to_alg_notation[first_block])[0]
            east_ray &= reflex_ray

    """ Get south ray with blocks """
    south_ray = south_ray_empty(self,square_notation)[0]
    intersections = south_ray & intersection_board
    if intersections != -1:
        first_block = msb_backward(intersections)
        if first_block != -1:
            blockers |= np.uint64(1) << first_block
            reflex_ray = north_ray_empty(self,index_to_alg_notation[first_block])[0]
            south_ray &= reflex_ray

    """ Get west ray with blocks """
    west_ray = west_ray_empty(self,square_notation)[0]
    intersections = west_ray & intersection_board
    if intersections != -1:
        first_block = msb_backward(intersections)
        if first_block != -1:
            blockers |= np.uint64(1) << first_block
            reflex_ray = east_ray_empty(self,index_to_alg_notation[first_block])[0]
            west_ray &= reflex_ray

    vision_bitboard = north_ray | west_ray | south_ray | east_ray

    return vision_bitboard, np.uint64(blockers)


def get_legal_moves_bishop(self,color:str, square_notation:str):
    """ returns normal moves and takes moves bitboards of a bishop from square"""
    vision_board_blocked, blockers = get_blocked_rays_bishop(self, square_notation)
    enemy_bitboard = get_enemy_pieces(self,color)
    enemy_bitboard = occupied_bitboard(enemy_bitboard)
    vision_board_attacked = blockers & enemy_bitboard
    full_vision_bitboard = vision_board_blocked | vision_board_attacked
    return full_vision_bitboard
    

def get_legal_moves_rook(self,color:str,square_notation:str): 
    """ returns normal moves and takes moves bitboards of a rook from square"""
    vision_board_blocked, blockers = get_blocked_rays_rook(self, square_notation)
    enemy_bitboard = get_enemy_pieces(self,color)
    enemy_bitboard = occupied_bitboard(enemy_bitboard)
    vision_board_attacked = blockers & enemy_bitboard
    full_vision_bitboard = vision_board_blocked | vision_board_attacked

    return full_vision_bitboard

def get_legal_moves_queen(self,color:str,square_notation:str):
    """ Returns all legal moves of a queen of a given color from a given square"""
    diagonal_vision_bitboard = get_legal_moves_bishop(self,color,square_notation)
    cardinal_vision_bitboard = get_legal_moves_rook(self,color,square_notation)
    return diagonal_vision_bitboard | cardinal_vision_bitboard


def get_legal_moves_knight(self, color:str, square_notation:str):
    """ Returns all legal moves of a knight of a given color from a given square """
    knight_vision_board = knight_vision_bitboard(self,square_notation)[0]
    friendly_bitboard = get_friendly_pieces(self,color)
    friendly_bitboard = occupied_bitboard(friendly_bitboard)
    full_vision_bitboard = knight_vision_board & ~friendly_bitboard
    return full_vision_bitboard

def get_legal_moves_king(self,color:str,square_notation:str):
    """ Returns all legal moves of a king of a given color from a given square """
    king_vision_board = king_vision_board_empty(self, square_notation)
    friendly_bitboard = get_friendly_pieces(self,color)
    friendly_bitboard = occupied_bitboard(friendly_bitboard)
    full_vision_bitboard = king_vision_board & ~friendly_bitboard
    return full_vision_bitboard

def get_legal_white_pawn_moves(self,color:str,square_notation:str): 
    """returns all legal moves of a white pawn in a given square notation"""
    pawn_vision_board, two_move = white_pawn_vision_board_empty(self, square_notation)
    all_bitboards = occupied_bitboard(self.all_bitboards)
    enemy_bitboard = occupied_bitboard(get_enemy_pieces(self,color))
    
    if pawn_vision_board & all_bitboards == 0:
        pawn_vision_board |= two_move

    attack_board = white_pawn_attack(self, square_notation)
    full_vision_bitboard = (pawn_vision_board & ~all_bitboards) | (attack_board & enemy_bitboard)
    return full_vision_bitboard

def get_legal_black_pawn_moves(self,color:str,square_notation:str): 
    """ Returns all legal moves of a black pawn from a given square """
    pawn_vision_board, two_move = black_pawn_vision_board_empty(self, square_notation)
    all_bitboards = occupied_bitboard(self.all_bitboards)
    enemy_bitboard = occupied_bitboard(get_enemy_pieces(self,color))

    if pawn_vision_board & all_bitboards == 0:
        pawn_vision_board |= two_move

    attack_board = black_pawn_attack(self, square_notation)
    full_vision_bitboard = (pawn_vision_board & ~all_bitboards) | (attack_board & enemy_bitboard) 
    return full_vision_bitboard

def piece_to_legal_moves_function(piece):
    """ translates given piece to correct function and returns said function"""
    get_legal_moves = {"W":get_legal_white_pawn_moves, "WN":get_legal_moves_knight, "WB":get_legal_moves_bishop,
             "WR":get_legal_moves_rook, "WQ":get_legal_moves_queen, "WK":get_legal_moves_king,
             "B":get_legal_black_pawn_moves, "BN":get_legal_moves_knight, "BB":get_legal_moves_bishop, 
             "BR":get_legal_moves_rook, "BQ":get_legal_moves_queen, "BK":get_legal_moves_king}
    correct_function = get_legal_moves[piece]
    return correct_function

def all_index_from_bitboard(bitboard):
    """ returns index of all 1 bits of a given bitboard """
    all_index = []
    bitboard = int(bitboard)
    while bitboard:
        index = (bitboard & -bitboard).bit_length() -1
        all_index.append(index)
        bitboard &= bitboard -1
    return all_index