from moves import *
from evaluation import *
import copy 
import time

move_dict = {}

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
        current_hash = current_board.get_board_state_hash()
        ordered_moves = order_moves(current_hash,legal_moves)
        score_data = alphabetaminimax(current_board, ordered_moves, depth, maxing, move_history)
        if score_data and max_time - (time.time()-initial_time) > 0:
            best_move = score_data 
            move_dict[current_hash] = best_move[1][0]
        else:
            break
        depth += 1
    print("depth",depth-1)
    return best_move

def order_moves(board_hash, legal_moves):
    if board_hash in move_dict:
        best_move = move_dict.get(board_hash)
        ordered_moves = []
        for move in legal_moves:
            if move == best_move:
                ordered_moves.append(move)
        for move in legal_moves:
            if move != best_move:
                ordered_moves.append(move)
        return ordered_moves
    return legal_moves
    
def alphabetaminimax(current_board, legal_moves, depth, maxing, move_history = [], alpha=-9999999999, beta=9999999999): 
    global initial_time
    global max_time
    if depth == 0 or legal_moves is None:
        return (evaluate(current_board), move_history)

    current_hash = current_board.get_board_state_hash()
    ordered_moves = order_moves(current_hash, legal_moves)
    
    if maxing == True: 
        max_score = (-9999999999, None)
        for move in ordered_moves:
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
                    move_dict[current_hash] = move
                alpha = max(alpha, max_score[0])
                if beta <= alpha:
                    break
        return max_score

    else:
        min_score = (9999999999, None)
        
        for move in ordered_moves:
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
                    move_dict[current_hash] = move

                beta = min(beta, min_score[0])
                if beta <= alpha:
                    break
        return min_score