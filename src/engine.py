from moves import *
from evaluation import *
import copy 
import time

def run_engine_local(current_board, legal_moves, depth, maxing, max_time_parameter ,move_history = []):
    global initial_time
    global max_time
    max_time = max_time_parameter
    initial_time = time.time()
    best_move = None
    depth = 1
    alpha=-9999999999
    beta=9999999999
    while True:
        time_left = max_time - (time.time()-initial_time)
        if time_left <= 0:
            break
        score_data = alphabetaminimax(current_board, legal_moves, depth, maxing, move_history)
        if score_data and max_time - (time.time()-initial_time) > 0:
            best_move = score_data 
        else:
            break
        depth += 1
    return best_move
    
def alphabetaminimax(current_board, legal_moves, depth, maxing, move_history = [], alpha=-9999999999, beta=9999999999): 
    global initial_time
    global max_time
    if depth == 0 or legal_moves is None:
        return (evaluate(current_board), move_history)
    
    if maxing == True: 
        max_score = (-9999999999, None)
        for move in legal_moves:
            if time.time()-initial_time >= max_time:
                break
            new_board = copy.deepcopy(current_board) 
            new_board.make_move_board(move[0],move[1],move[2])
            new_moves = all_moves(new_board,"B")
            new_move_history = move_history.copy()
            new_move_history.append(move)
            score = alphabetaminimax(new_board, new_moves, depth-1, False, new_move_history, alpha, beta)     
            if score:
                if max_score[0] < score[0]:
                    max_score = score
                alpha = max(alpha, max_score[0])
                if beta <= alpha:
                    break
        return max_score

    else:
        min_score = (9999999999, None)
        for move in legal_moves:
            if time.time()-initial_time >= max_time:
                break
            new_board = copy.deepcopy(current_board)
            new_board.make_move_board(move[0],move[1],move[2])
            new_moves = all_moves(new_board,"W")
            new_move_history = move_history.copy()
            new_move_history.append(move)
            score = alphabetaminimax(new_board, new_moves, depth-1, True, new_move_history, alpha, beta)
            if score:
                if min_score[0] > score[0]:
                    min_score = score
                beta = min(beta, min_score[0])
                if beta <= alpha:
                    break
        return min_score
