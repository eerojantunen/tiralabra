import numpy as np
from piece_data import piece_representation, get_square_location_from_coordinates
from vision_boards import get_legal_white_pawn_moves, get_enemy_pieces, get_friendly_pieces, get_legal_moves_knight, get_legal_moves_queen, get_legal_moves_rook, bishop_vision_board_empty, legal_moves_of_piece, occupied_bitboard, knight_vision_bitboard, get_blocked_rays_bishop, get_legal_moves_bishop
from Pieces import queen_vision_board_empty
from annotation_data import alg_notation_to_index, index_to_alg_notation
from vision_rays import north_ray_empty, south_ray_empty, west_ray_empty, east_ray_empty, south_west_ray_empty,south_east_ray_empty, north_west_ray_empty, north_east_ray_empty
import time

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

        self.full_board = np.uint64(0)
        self.piece_board = {}                      


    @property
    def all_bitboards(self):
        """ returns list of all piece bitboards """
        return [self.white_rooks, self.white_bishops, self.white_knights, self.white_queens,
                self.white_king, self.white_pawns, self.black_rooks, self.black_bishops,
                self.black_knights, self.black_king, self.black_pawns, self.black_queens]

    @property
    def white_bitboards(self):
        """ returns list of all white piece bitboards """
        return [self.white_rooks, self.white_bishops, self.white_knights, self.white_queens,
                self.white_king, self.white_pawns]
    
    @property
    def black_bitboards(self):
        """ returns list of all black piece bitboards """
        return [self.black_rooks, self.black_bishops,self.black_knights, self.black_king,
                self.black_pawns, self.black_queens]


    @property
    def bitboard_dict(self):
        return {"W":self.white_pawns, "WR":self.white_rooks, "WN":self.white_knights, "WB":self.white_bishops,
                "WQ":self.white_queens, "WK":self.white_king, "B":self.black_pawns, "BR":self.black_rooks,
                "BN":self.black_knights, "BB":self.black_bishops, "BQ":self.black_queens, "BK":self.black_king}

    def setup(self):
        self.setup_standard_board()

    def create_board(self):
        full_board = np.uint64(0)
        for board in self.all_bitboards:
            full_board = np.uint64(full_board | board)
        self.full_board = full_board

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
            print(bin(self.white_pawns))
        self.black_rooks = np.uint64(self.black_rooks | 1 << 56 | 1 << 63)
        self.black_knights = np.uint64(self.black_knights | 1 << 57 | 1 << 62)
        self.black_bishops = np.uint64(self.black_bishops | 1 << 58 | 1 << 61)
        self.black_queens = np.uint64(self.black_queens | 1 << 59)
        self.black_king = np.uint64(self.black_king | 1 << 60)
        self.create_board()


    def index_from_bitboard(self, bitboard):
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
        bitboard_dict = {"W":"white_pawns", "WR":"white_rooks", "WN":"white_knights", "WB":"white_bishops",
                         "WQ":"white_queens", "WK":"white_king", "B":"black_pawns", "BR":"black_rooks",
                        "BN":"black_knights", "BB":"black_bishops", "BQ":"black_queens", "BK":"black_king"}   
        correct_bitboard = bitboard_dict[color_and_piece]
        return correct_bitboard

    def notation_decoder(self, notation:str):
        """ takes algeabric notation, returns correct bitboard, square_location """
        correct_bitboard = self.piece_annotation_to_bitboard(notation[:-2])
        square_location = get_square_location_from_coordinates(notation[-2:])
        return correct_bitboard, square_location

    def add_material(self, notation:str):
        """ adds chosen material to on board """

        correct_bitboard, square_location = self.notation_decoder(notation)
        current_value = getattr(self, correct_bitboard)
        new_value = np.uint64(current_value | 1 << square_location)
        setattr(self, correct_bitboard, new_value)


    
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

    def legal_moves_bishop(self,color,square_notation):
        return get_legal_moves_bishop(self, color, square_notation)

    def legal_moves_rook(self, color, square_notation):
        return get_legal_moves_rook(self, color, square_notation)

    def legal_moves_queen(self,color,square_notation):
        return get_legal_moves_queen(self,color,square_notation)

    def legal_moves_knight(self, color, square_notation):
        return get_legal_moves_knight(self, color, square_notation)

    def legal_white_pawn_moves(self,color,square_notation): #remove color parameter
        return get_legal_white_pawn_moves(self,color,square_notation)

C = Board()
C.create_board()
C.add_material("Bb2")
C.add_material("Ba5")
C.add_material("Bc4")
C.add_material("Bh7")
C.add_material("Bd7")
C.add_material("Bc5")
C.add_material("Bd5")
C.add_material("Bh6")

C.add_material("Bd8")

C.add_material("Wh4")



#z = alg_notation_to_index["d3"]
#x = C.get_rook_vision_board_empty("f5")
#C.print_square_vision_board(x,"BR", z)
C.final_print_board()
alku = time.time()
#y = C.legal_moves_queen("B","f5")
loppu = time.time()
print(loppu-alku)
z = C.legal_white_pawn_moves("W","d8")
d = C.print_board_occupancy
#z = C.legal_moves_rook("W","b3")
C.print_square_vision_board(z,"W",alg_notation_to_index["d8"],"W")
