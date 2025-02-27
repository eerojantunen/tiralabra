from temp import *
from engine import *
class Game:
    def __init__(self):
        self.main_board = Board()
        
    def print_piece_names(self):
        print("White pawn: W\nWhite knight: WN\nWhite bishop: WB\nWhite rook: WR")
        print("White queen: WQ\nWhite king: WK\nBlack pawn: B\nBlack knight: BN\nBlack bishop: BB")
        print("Black rook: BR\nBlack queen: BQ\nBlack king: BK")


    def run_game(self): #add mate
        self.main_board.final_print_board()
        while True:
            print("Thinking...")
            move = self.main_board.run_engine()
            self.main_board.make_move_board(move[1][0][0],move[1][0][1],move[1][0][2])
            self.main_board.final_print_board()
            print(f"{move[1][0][2]} moves from {index_to_alg_notation[move[1][0][0]]} to {index_to_alg_notation[move[1][0][1]]}!\n")
            while True:
                print("Your move")
                from_square_notation = input("from_square_notation: ")
                to_square_notation = input("to square notation: ")
                piece = input("piece notation: ")
                try:
                    if not is_legal(self.main_board, alg_notation_to_index[from_square_notation], alg_notation_to_index[to_square_notation],piece):
                        print("Not a legal move, try again")
                        continue
                    break
                except:
                    print("Not a legal move, try again")
                    continue
            self.main_board.make_move_board(alg_notation_to_index[from_square_notation],alg_notation_to_index[to_square_notation],piece)
            self.main_board.final_print_board()

    def new_game(self):
        self.main_board.setup_standard_board()
        self.run_game()
    
    def load_ready_position(self):
        self.main_board.add_material("Wa2")
        self.main_board.add_material("Wb2")
        self.main_board.add_material("Wc3")
        self.main_board.add_material("Wd3")
        self.main_board.add_material("We4")
        self.main_board.add_material("Wh2")
        self.main_board.add_material("WRa1")
        self.main_board.add_material("WNb1")
        self.main_board.add_material("WKg1")
        self.main_board.add_material("WQh5")
        self.main_board.add_material("WBh6")
        self.main_board.add_material("WRf7")

        self.main_board.add_material("Ba7")
        self.main_board.add_material("Bb7")
        self.main_board.add_material("Bc7")
        self.main_board.add_material("Bd6")
        self.main_board.add_material("Bh7")
        self.main_board.add_material("BRa8")
        self.main_board.add_material("BQd8")
        self.main_board.add_material("BRg8")
        self.main_board.add_material("BKh8")
        self.main_board.add_material("BNc6")
        self.main_board.add_material("BBe6")
        self.main_board.add_material("BBg3")
        self.run_game()

    def instructions(self):
        print("\nComputer plays white, you play black")
        print("The computer will make a move and will let you know what piece it moved from which square into what square")
        print("You will be prompted to input the inital square of the piece you want to move, the square it moves to and the piece type")
        print("These squares are to be communicated in coordinate notation for example: a2, h5, d8")
        print("\nThe piece types are:")
        self.print_piece_names()

    def game_selection(self):
        """ select game type (new, loaded position)"""
        while True:
            selection = int(input("1. Setup standard board \n2. Load position from memory\n3. Instructions \nInput: "))
            if selection == 1:
                self.new_game()
                break
            elif selection == 2:
                self.load_ready_position()
                break
            elif selection ==3:
                self.instructions()
            print("Invalid selection \n")
    

game = Game()
game.game_selection()