from moves import *
from evaluation import *
import copy 

def run_engine_local(current_board, legal_moves, depth, maxing, move_history = [], alpha=0, beta=0):
    score_data = alphabetaminimax(current_board, legal_moves, depth, maxing, move_history,)
    return score_data

def alphabetaminimax(current_board, legal_moves, depth, maxing, move_history = [], alpha=-9999999999, beta=99999999999): #1st version only for white side
    if depth == 0:
        return (evaluate(current_board), move_history)

    if maxing == True: 
        max_score = (-9999999999, None)
        for move in legal_moves:
            
            new_board = copy.deepcopy(current_board) #check deepcopy speed
            new_board.make_move_board(move[0],move[1],move[2])
            new_moves = all_moves(new_board,"B")
            new_move_history = move_history.copy()
            new_move_history.append(move)
            score = alphabetaminimax(new_board,new_moves,depth-1,False, new_move_history)     

            if max_score[0] < score[0]:
                max_score = score
            alpha = max(alpha, max_score[0])
            if beta <= alpha:
                break               
        return max_score

    else:
        min_score = (9999999999, None)
        for move in legal_moves:
            new_board = copy.deepcopy(current_board)
            new_board.make_move_board(move[0],move[1],move[2])
            new_moves = all_moves(new_board,"W")
            new_move_history = move_history.copy()
            new_move_history.append(move)
            score = alphabetaminimax(new_board,new_moves,depth-1,True,new_move_history)
            if score[0] < min_score[0]:
                min_score = score
            beta = min(beta, min_score[0])
            if beta <= alpha:
                break
        return min_score