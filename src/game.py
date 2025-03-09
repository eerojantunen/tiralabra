from board import *
class Game:
    
    def __init__(self):
        """ initalizes board and default parameters """
        self.main_board = Board()
        self.max_move_time = 20

    def run_game(self): 
        """ Runs a loop through which user can play against the chess engine"""
        self.main_board.final_print_board()
        while True:
            alku = time.time()
            print("Thinking...")
            move = self.main_board.run_engine(self.max_move_time)
            self.main_board.make_move_board(move[1][0][0],move[1][0][1],move[1][0][2])
            self.main_board.final_print_board()
            if len(self.main_board.piece_board["BK"]) == 0:
                print("Computer wins!")
                break
            print(f"{move[1][0][2]} moves from {index_to_alg_notation[move[1][0][0]]} to {index_to_alg_notation[move[1][0][1]]}!\n")
            print(time.time()-alku)
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

            if len(self.main_board.piece_board["WK"]) == 0:
                print("You win!")
                break
            self.main_board.final_print_board()

    def new_game(self):
        """ Initializes standard board and starts game loop"""
        self.main_board.setup_standard_board()
        self.run_game()
    


    def load_ready_position(self):
        """ Initializes board with a given set of piece positions """
        self.main_board.add_material("BKg8")
        self.main_board.add_material("Bg7")
        self.main_board.add_material("Bh7")
        self.main_board.add_material("Bc5")
        self.main_board.add_material("Ba6")
        self.main_board.add_material("Bb7")
        self.main_board.add_material("BRa8")
        self.main_board.add_material("BNb8")
        self.main_board.add_material("BBc8")
        self.main_board.add_material("BQd8")
        self.main_board.add_material("BRf8")
        self.main_board.add_material("BBd6")
        self.main_board.add_material("Be6")
        self.main_board.add_material("BNf6")
        self.main_board.add_material("Bf7")

        self.main_board.add_material("Wa2")
        self.main_board.add_material("Wb2")
        self.main_board.add_material("Wf2")
        self.main_board.add_material("Wg2")
        self.main_board.add_material("Wh2")
        self.main_board.add_material("WKg1")
        self.main_board.add_material("WRf1")
        self.main_board.add_material("WQd1")
        self.main_board.add_material("WRa1")
        self.main_board.add_material("WNf3")
        self.main_board.add_material("WNc3")
        self.main_board.add_material("WBc4")
        self.main_board.add_material("WBf4")
        self.main_board.add_material("Wd4")
        self.main_board.add_material("We3")        
        self.run_game()

    def instructions(self):
        """ Prints instructions """

        print("\nComputer plays white, you play black")
        print("The computer will make a move and will let you know what piece it moved from which square into what square")
        print("You will be prompted to input the inital square of the piece you want to move, the square it moves to and the piece type")
        print("These squares are to be communicated in coordinate notation for example: a2, h5, d8")
        print("\nThe piece types are:")
        self.print_piece_names()

    def print_piece_names(self):
        """ Prints piece names and their notation"""

        print("White pawn: W\nWhite knight: WN\nWhite bishop: WB\nWhite rook: WR")
        print("White queen: WQ\nWhite king: WK\nBlack pawn: B\nBlack knight: BN\nBlack bishop: BB")
        print("Black rook: BR\nBlack queen: BQ\nBlack king: BK")

    def change_parameters(self):
        """ Allows user to choose which parameters to change"""

        while True:
            selection = int(input(f"\n1: Change amount of time computer has per move. Current: {self.max_move_time}s\n0: Return\nInput: "))
            if selection == 1:
                new_max_time = int(input("\nNew amount of time computer has per move: "))
                self.max_move_time = new_max_time
                print("Updated succesfully!")
            elif selection == 0:
                break
            else:
                print("\nInvalid selection \n")


    def game_selection(self):
        """ Allows user to select from
            1: Set up standard board
            2. Load position from memory
            3. Instructions
            4. Change engine parameters"""
        while True:
            selection = int(input("\n1. Setup standard board \n2. Load position from memory\n3. Instructions \n4. Change engine parameters \nInput: "))
            if selection == 1:
                self.new_game()
                break
            elif selection == 2:
                self.load_ready_position()
                break
            elif selection == 3:
                self.instructions()
            elif selection == 4:
                self.change_parameters()
            else:
                print("\nInvalid selection \n")

    


game = Game()
game.game_selection()