import numpy as np
from piece_data import piece_representation, get_square_location_from_coordinates
from vision_boards import get_legal_moves_king, get_legal_white_pawn_moves, get_enemy_pieces, get_friendly_pieces, get_legal_moves_knight, get_legal_moves_queen, get_legal_moves_rook, bishop_vision_board_empty, legal_moves_of_piece, occupied_bitboard, knight_vision_bitboard, get_blocked_rays_bishop, get_legal_moves_bishop
from Pieces import queen_vision_board_empty
from annotation_data import alg_notation_to_index, index_to_alg_notation
from vision_rays import north_ray_empty, south_ray_empty, west_ray_empty, east_ray_empty, south_west_ray_empty,south_east_ray_empty, north_west_ray_empty, north_east_ray_empty
from evaluation import material_count
import time
from moves import *
from engine import *
from evaluation import *

#TODO Remove essentially >50% of methods out of board class into appropriate file
#np -> pythonin oma
#muuta self.white yms numero listaan
class Board():
    def __init__(self):
        self.white_rooks = np.uint64(0)
        self.white_bishops = np.uint64(0)
        self.white_knights = np.uint64(0)
        self.white_queens = np.uint64(0)
        self.white_king = np.uint64(0)
        self.white_pawns = np.uint64(0)

        self.black_rooks = np.uint64(0)
        self.black_bishops = np.uint64(0)
        self.black_knights = np.uint64(0)
        self.black_queens = np.uint64(0)
        self.black_king = np.uint64(0)
        self.black_pawns = np.uint64(0)

        self.piece_board = {}

    @property
    def full_board(self):
        return occupied_bitboard(self.all_bitboards)

    @property
    def all_bitboards(self):
        """ returns list of all piece bitboards """
        return [self.white_rooks, self.white_bishops, self.white_knights, self.white_queens,
                self.white_king, self.white_pawns, self.black_rooks, self.black_bishops,
                self.black_knights, self.black_king, self.black_pawns, self.black_queens]

    @property
    def white_bitboards(self):
        """ returns list of all white piece bitboards 
            Order: P, N, B, R, Q, K"""
        
        return [self.white_pawns,self.white_knights, self.white_bishops, self.white_rooks, self.white_queens,
                self.white_king]
    
    @property
    def black_bitboards(self):
        """ returns list of all black piece bitboards 
            Order: P, N, B, R, Q, K"""
        return [self.black_pawns,self.black_knights, self.black_bishops, self.black_rooks, self.black_queens,
                self.black_king]


    @property
    def bitboard_dict(self):
        return {"W":self.white_pawns, "WR":self.white_rooks, "WN":self.white_knights, "WB":self.white_bishops,
                "WQ":self.white_queens, "WK":self.white_king, "B":self.black_pawns, "BR":self.black_rooks,
                "BN":self.black_knights, "BB":self.black_bishops, "BQ":self.black_queens, "BK":self.black_king}

    def setup(self):
        self.setup_standard_board()


    def setup_standard_board(self):
        """ setup initial bitboard positions for pieces """
        self.white_rooks = np.uint64(self.white_rooks | 1 << 0 | 1 << 7)
        self.white_knights = np.uint64(self.white_knights | 1 << 1 | 1 << 6)
        self.white_bishops = np.uint64(self.white_bishops | 1 << 2 | 1 << 5)
        self.white_queens = np.uint64(self.white_queens | 1 << 3)
        self.white_king = np.uint64(self.white_king | 1 << 4)
        for i in range(8):
            self.white_pawns = np.uint64(self.white_pawns | 1 << 8+i)
            self.black_pawns = np.uint64(self.black_pawns | 1 << 48+i)
        self.black_rooks = np.uint64(self.black_rooks | 1 << 56 | 1 << 63)
        self.black_knights = np.uint64(self.black_knights | 1 << 57 | 1 << 62)
        self.black_bishops = np.uint64(self.black_bishops | 1 << 58 | 1 << 61)
        self.black_queens = np.uint64(self.black_queens | 1 << 59)
        self.black_king = np.uint64(self.black_king | 1 << 60)
        self.refresh_piece_board()

    def index_from_bitboard(self, bitboard): #compare speeds to other index from bitbarobd
        """ Returns list friendly indexes from bitboard """

        indexes = set()
        for index in range(64):
            if bitboard & (1 << index):
                indexes.add(index)
        return indexes

    def refresh_piece_board(self):
        """ Refreshes displayable board to match bitboards """

        for piece_type, bitboard in self.bitboard_dict.items():
            indexes = self.index_from_bitboard(bitboard)
            self.piece_board[piece_type] = indexes

    def final_print_board(self):
        """function printing board with chess symbols"""
        self.refresh_piece_board()
        board = [0]*64
        for piece_type, piece_locations in self.piece_board.items():
            for piece in piece_locations:
                board[piece] = piece_representation[piece_type]
        board = np.reshape(board,(8,8))
        board = board[::-1,:]   
        print(board, "\n")

    def print_square_vision_board(self, vision_board, piece:str, square_index:int, color="x"):
        """ print a given vision board ---- debugging tool
         🟥-enemy,   🟩-friendly 🟪-self"""
        board = ["⚪"]*64
        x = self.index_from_bitboard(vision_board)
        if color != "x":
            y = self.index_from_bitboard(occupied_bitboard(get_enemy_pieces(self, color))) #:)
            for i in y:
                board[i] = "🟥"
        board[square_index] = "🟪"#piece_representation[piece] optional
        for i in x:
            board[i] = "❌"
        if color != "x":
            y = self.index_from_bitboard(occupied_bitboard(get_friendly_pieces(self, color))) #:)
            for i in y:
                board[i] = "🟩"
        board = np.reshape(board,(8,8))
        board = board[::-1,:]   
        print(board, "\n")

    def print_board_occupancy(self):
        """prints occupied squares"""
        print(bin(self.full_board))

    def piece_annotation_to_bitboard(self, color_and_piece):
        """ returns correct bitboard from given color and piece """
        bitboard_dict = {"W":self.white_pawns, "WR":self.white_rooks, "WN":self.white_knights, "WB":self.white_bishops,
                         "WQ":self.white_queens, "WK":self.white_king, "B":self.black_pawns, "BR":self.black_rooks,
                        "BN":self.black_knights, "BB":self.black_bishops, "BQ":self.black_queens, "BK":self.black_king}   
        correct_bitboard = bitboard_dict[color_and_piece]
        return correct_bitboard

    def piece_annotation_to_bitboard_name(self, color_and_piece):
        """ returns correct bitboard name from given color and piece """
        bitboard_dict = {"W":"white_pawns", "WR":"white_rooks", "WN":"white_knights", "WB":"white_bishops",
                         "WQ":"white_queens", "WK":"white_king", "B":"black_pawns", "BR":"black_rooks",
                        "BN":"black_knights", "BB":"black_bishops", "BQ":"black_queens", "BK":"black_king"}   
        correct_bitboard_name = bitboard_dict[color_and_piece]
        return correct_bitboard_name
    
    def notation_decoder(self, notation:str):
        """ takes algeabric notation, returns correct bitboard, square_location """
        correct_bitboard = self.piece_annotation_to_bitboard_name(notation[:-2])
        square_location = get_square_location_from_coordinates(notation[-2:])
        return correct_bitboard, square_location

    def add_material(self, notation:str):
        """ adds chosen material to on board """

        correct_bitboard, square_location = self.notation_decoder(notation)
        current_value = getattr(self, correct_bitboard)
        new_value = np.uint64(current_value | 1 << square_location)
        setattr(self, correct_bitboard, new_value)
        self.refresh_piece_board()

    
    #### temporary methods, to be moved

    def get_knight_vision_bitboard(self,square_notation:str):
        """ temp """
        return knight_vision_bitboard(self, square_notation)

    def get_north_ray_empty(self,square_notation:str):
        return north_ray_empty(self,square_notation)

    def get_south_ray_empty(self,square_notation:str):
        return south_ray_empty(self,square_notation)

    def get_west_ray_empty(self,square_notation:str):
        return west_ray_empty(self,square_notation)

    def get_east_ray_empty(self,square_notation:str):
        return east_ray_empty(self,square_notation)
    
    def get_south_west_ray_empty(self, square_notation:str):
        return south_west_ray_empty(self, square_notation)
    
    def get_south_east_ray_empty(self,square_notation:str):
        return south_east_ray_empty(self, square_notation)

    def get_north_west_ray_empty(self, square_notation:str):
        return north_west_ray_empty(self, square_notation)
    
    def get_north_east_ray_empty(self,square_notation:str):
        return north_east_ray_empty(self, square_notation)

    def get_legal_moves_of_piece(self,vision_board,color:str):
        return legal_moves_of_piece(self, vision_board,color)

    def get_bishop_vision_board_empty(self,square_notation):
        return bishop_vision_board_empty(self,square_notation)

    def get_queen_vision_board_empty(self,square_notation):
        return queen_vision_board_empty(self,square_notation)

    def blocked_rays_bishop(self,square_notation):
        return get_blocked_rays_bishop(self,square_notation)

    def row_col_from_square_notation(self,square_location_as_notation):
        """ returns board row and column from algeabric notation (0-7)"""
        square_location = get_square_location_from_coordinates(square_location_as_notation)
        row = square_location // 8
        col = square_location-((square_location // 8) * 8)
        return row, col

    def copy_board(self): #mulla on syvä viha tätä metodia kohtaan. 90% varma että turha
        board_copy = Board()
        for key, value in self.__dict__.items():
            if isinstance(value, np.uint64):
                setattr(board_copy, key, np.uint64(value))
            elif isinstance(value, dict):
                setattr(board_copy, key, value.copy())
        return board_copy

    """ debugu tool :)""" 
    def print_bb(self, vision_board, piece:str, square_index:int, color="x"):
        """ print a given vision board ---- debugging tool
         🟥-enemy,   🟩-friendly 🟪-self"""
        board = ["⚪"]*64
        x = self.index_from_bitboard(vision_board)
        board[square_index] = "🟪"#piece_representation[piece] optional
        for i in x:
            board[i] = "❌"
        board = np.reshape(board,(8,8))
        board = board[::-1,:]   
        print(board, "\n")

    #turha
    def eval(self):
        return evaluate(self)


    def run_engine(self):
        legal_moves = all_moves(self,"W")
        alku = time.time()
        move_data = run_engine_local(self,legal_moves,4,True)
        print(time.time()-alku)
        return move_data

    def make_move_board(self, from_square, to_square, piece):
        """ as index from and to"""
        make_move(self,from_square,to_square,piece)
    
    def make_move_board_alg(self,from_square,to_square,piece):
        from_square = alg_notation_to_index[from_square]
        to_square = alg_notation_to_index[to_square]
        make_move(self,from_square,to_square,piece)

    def get_board_state_hash(self):
        hash_key = 0
        for i in self.all_bitboards:
            hash_key*=18446744073709551616
            hash_key+=i