import numpy as np
from piece_data import piece_representation, get_square_location_from_coordinates
from annotation_data import alg_notation_to_index, index_to_alg_notation
from evaluation import material_count
from moves import *
from engine import *
from evaluation import *
import time

class Board():
    def __init__(self):
        """ initializes all pieces as np.uint64(0) (empty chessboard)"""
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
        self.move_history = []

    @property
    def full_board(self):
        """ returns bitboard of all occupied squares """
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
        """ returns a dict of piece notation to correct piece bitboard"""
        return {"W":self.white_pawns, "WR":self.white_rooks, "WN":self.white_knights, "WB":self.white_bishops,
                "WQ":self.white_queens, "WK":self.white_king, "B":self.black_pawns, "BR":self.black_rooks,
                "BN":self.black_knights, "BB":self.black_bishops, "BQ":self.black_queens, "BK":self.black_king}

    def setup(self):
        """ initializes bitboards of all pieces to be in standard inital chess position """
        self.setup_standard_board()


    def setup_standard_board(self):
        """ initializes bitboards of all pieces to be in standard inital chess position """
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

    def index_from_bitboard(self, bitboard):
        """ Returns list friendly indexes from bitboard """
        indexes = set()
        for index in range(64):
            if bitboard & (1 << index):
                indexes.add(index)
        return indexes

    def refresh_piece_board(self):
        """ Refreshes piece_board dictionary to match bitboards """

        for piece_type, bitboard in self.bitboard_dict.items():
            indexes = self.index_from_bitboard(bitboard)
            self.piece_board[piece_type] = indexes

    def final_print_board(self):
        """Prints current board using chess symbols"""
        self.refresh_piece_board()
        board = [0]*64
        for piece_type, piece_locations in self.piece_board.items():
            for piece in piece_locations:
                board[piece] = piece_representation[piece_type]
        board = np.reshape(board,(8,8))
        board = board[::-1,:]   
        print(board, "\n")

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
        """ Adds a given piece to board given the notation
            Parameters:
                notation: Piece notation + square algeabratic notation eg.(WNe5 - white knight e5) """

        correct_bitboard, square_location = self.notation_decoder(notation)
        current_value = getattr(self, correct_bitboard)
        new_value = np.uint64(current_value | 1 << square_location)
        setattr(self, correct_bitboard, new_value)
        self.refresh_piece_board()

    
    def row_col_from_square_notation(self,square_location_as_notation):
        """ returns board row and column from algeabric notation (0-7)"""
        square_location = get_square_location_from_coordinates(square_location_as_notation)
        row = square_location // 8
        col = square_location-((square_location // 8) * 8)
        return row, col


    def run_engine(self,max_time_parameter):
        """ Runs minimax engine to find white (computer) move
            Parameters: 
                max_time_parameter: maximum time engine is allowed to run
            Returns:
                Tuple of (int evaluation, list move history)"""
        legal_moves = all_moves(self,"W")
        move_data = run_engine_local(self,legal_moves,True,max_time_parameter=max_time_parameter)
        return move_data

    def make_move_board(self, from_square, to_square, piece):
        """ Makes a move on the board
            Parameters:
                from_square: int index of from square
                to_square: int index of to square
                piece: str moving piece notation """
        move_data = make_move(self,from_square,to_square,piece)
        self.move_history.append(move_data)

    def undo_move_board(self):
        """ Undos most recent move on board """
        if not self.move_history:
            return False 
        last_move = self.move_history.pop()
        piece = last_move['piece']
        from_square = last_move['from_square']
        to_square = last_move['to_square']
        captured_piece = last_move.get('captured_piece', None)

        bitboard_name = self.piece_annotation_to_bitboard_name(piece)
        current_value = getattr(self, bitboard_name)
        new_value = current_value ^ (np.uint64(1) << to_square)
        new_value = np.uint64(new_value | (1 << from_square))
        setattr(self, bitboard_name, new_value)
        
        if captured_piece:
            captured_bitboard_name = self.piece_annotation_to_bitboard_name(captured_piece)
            captured_value = getattr(self, captured_bitboard_name)
            restored_value = np.uint64(captured_value | (1 << to_square))
            setattr(self, captured_bitboard_name, restored_value)
        self.refresh_piece_board()

    def get_board_state_hash(self):
        """ Generates and returns unique int representing board state """
        hash_key = 0
        for i in self.all_bitboards:
            hash_key ^= i
        return hash_key