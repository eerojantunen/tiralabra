from moves import *
from evaluation import *
import copy 

def run_engine_local(current_board, legal_moves, depth, maxing, move_history = [], alpha=0, beta=0):
    bestmove, _ = alphabetaminimax(current_board, legal_moves, depth, maxing, move_history,)
    return bestmove

def alphabetaminimax(current_board, legal_moves, depth, maxing, move_history = [], alpha=-9999999999, beta=99999999999): #1st version only for white side
    #remove move_history ?
    #fix
    if depth == 0:
        return None, evaluate(current_board)

    bestmove = None

    if maxing == True: 
        max_score = -9999999999
        for move in legal_moves:
            
            new_board = copy.deepcopy(current_board) #check deepcopy speed
            new_board.make_move_board(move[0],move[1],move[2])

            new_moves = all_moves(new_board,"B")
            _, score = alphabetaminimax(new_board,new_moves,depth-1,False)         
            if score > max_score:
                max_score = score
                bestmove = move
            alpha = max(alpha, max_score)
            if beta <= alpha: 
                break
        return bestmove, max_score

    else:
        min_score = 9999999999
        for move in legal_moves:
            new_board = copy.deepcopy(current_board)
            new_board.make_move_board(move[0],move[1],move[2])

            new_moves = all_moves(new_board,"W")
            _, score = alphabetaminimax(new_board,new_moves,depth-1,True)
            if score < min_score:
                min_score = score
                bestmove = move
            beta = min(beta, min_score)
            if beta >= alpha:
                break
        return bestmove, min_score