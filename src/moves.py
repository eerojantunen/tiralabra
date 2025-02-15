import numpy as np
from vision_boards import *
from piece_data import *
from annotation_data import *

def update_full_board(self,from_square:int, to_square:int, piece):
    """ updates move to full_board """
    self.full_board &= ~(np.uint(1) << from_square)
    self.full_board |= np.uint(1) << to_square


def update_piece_board(self,from_square:int, to_square:int, piece):
    """ updates move to piece_board """

    self.piece_board[piece].add(to_square)
    self.piece_board[piece].remove(from_square)



def update_bitboard_of_moving(self,from_square:int, to_square:int, piece):
    """ updates the bitboard of the moving piece """
    #to_move_bitboard = self.piece_annotation_to_bitboard(piece)
    target_bitboard_name = self.piece_annotation_to_bitboard_name(piece)
    to_move_bitboard = getattr(self, target_bitboard_name)
    to_move_bitboard &= ~(np.uint(1) << from_square) #set bit at index from_square to 0 (maybe do seperate function to clear?)
    to_move_bitboard |= np.uint(1) << to_square 
    setattr(self, target_bitboard_name, to_move_bitboard)
    #XD

def get_piece_by_index(self,index):
    for key, value in self.piece_board.items():
        if index in value:
            return key
    return None

def identify_takes(self,to_square, piece): #verify that works lolz
    if self.full_board & (np.uint(1) << to_square) == np.uint64(0):
        return
    attacked_piece = get_piece_by_index(self, to_square)
    self.piece_board[attacked_piece].remove(to_square) #get piece on said index

    target_bitboard_name = self.piece_annotation_to_bitboard_name(attacked_piece)
    taken_bitboard = getattr(self, target_bitboard_name)
    taken_bitboard &= ~(np.uint(1) << to_square)
    setattr(self, target_bitboard_name, taken_bitboard)
    

def make_move(self,from_square:int, to_square:int, piece):
    """ FORCE UPDATES move according to from square and to square
        from_square - as index 0-63
        to_square - index 0-63
        """
    identify_takes(self,to_square, piece)
    update_bitboard_of_moving(self, from_square, to_square, piece)
    update_piece_board(self, from_square, to_square, piece)
    #update_full_board(self, from_square, to_square, piece)

def make_move_takes(self,from_square, to_square, piece, taken_piece):
    """ FORCE UPDATES take move according to from square and to square
        make move updated to include functionality of this function
    """
    make_move(self, from_square, to_square, piece)
    self.full_board &= ~(np.uint(1) << to_square)
    self.piece_board[piece].remove(to_square)

def all_moves(self,only_color=None): #probably not working correctly fix lolz
    """ returns all possible moves, or all moves of wanted color
        returns as (from_square, to_square, piece)"""
    all_move_list = []
    for key, value in self.piece_board.items():
        if only_color is None or key[0] == only_color:
            if value:
                color = key[0]
                legal_move_function = piece_to_legal_moves_function(key)

                for square in value:
                    legal_move_bitboard = legal_move_function(self, color, index_to_alg_notation[square])
                    all_index = all_index_from_bitboard(legal_move_bitboard)
                    for index in all_index:
                        all_move_list.append((square, index, key)) 
    return all_move_list