from board import *

class Game:
    def __init__(self):
        self.main_board = Board()
        self.max_move_time = 20

    def run_game(self): #add mate
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
        self.main_board.setup_standard_board()
        self.run_game()
    


    def load_ready_position(self):

        self.main_board.add_material("BKh8")
        self.main_board.add_material("BQh6")
        self.main_board.add_material("BRe6")
        self.main_board.add_material("WKg1")
        self.main_board.add_material("WQe4")
        self.main_board.add_material("WRc2")

        self.main_board.add_material("BNb5")
        self.main_board.add_material("BNe7")
        self.main_board.add_material("Bf5")
        self.main_board.add_material("Bg7")
        self.main_board.add_material("WBb1")
        self.main_board.add_material("WNb7")
        self.main_board.add_material("Wg2")
        self.main_board.add_material("Wh3")

        self.run_game()

    def instructions(self):
        print("\nComputer plays white, you play black")
        print("The computer will make a move and will let you know what piece it moved from which square into what square")
        print("You will be prompted to input the inital square of the piece you want to move, the square it moves to and the piece type")
        print("These squares are to be communicated in coordinate notation for example: a2, h5, d8")
        print("\nThe piece types are:")
        self.print_piece_names()

    def print_piece_names(self):
        print("White pawn: W\nWhite knight: WN\nWhite bishop: WB\nWhite rook: WR")
        print("White queen: WQ\nWhite king: WK\nBlack pawn: B\nBlack knight: BN\nBlack bishop: BB")
        print("Black rook: BR\nBlack queen: BQ\nBlack king: BK")

    def change_parameters(self):
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
        """ select game type (new, loaded position)"""
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