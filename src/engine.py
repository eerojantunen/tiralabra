from moves import *
from evaluation import *
import copy 
import time

move_dict = {}

def run_engine_local(current_board, legal_moves, maxing, max_time_parameter ,move_history = []):
    """ Runs the minimax algorithm iteratively with alpha beta pruning and move ordering for a given board and legal moves
        Parameters:
            current_board: target Board object
            legal_moves: list of all legal moves for computer (white)
            maxing: boolean indicating is minimax algorithm started with maximizing or minimizing
            max_time_parameter: int indicating amount of time to run engine
            move_history: list of previous moves (optional)
        Returns:
            Tuple of (int evaluation, list move history)
        """
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
    return best_move
def order_moves(board_hash, legal_moves):
    """ Orders moves if current board has appeared before and best move is in legal_moves 
    Parameters:
        board_hash: int of unique representation of board state
        legal_moves: list of legal moves
    returns:
        legal_moves with found (best) move as first if found"""
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
    """ minimax algorithm with alpha-beta pruning and move ordering which tries moves to find best possible move sequence
        according to evaluation function and assuming both players play optimally
        Parameters:
            current_board: target Board object
            legal_moves: list of all legal moves for computer (white)
            maxing: boolean indicating is minimax algorithm started with maximizing or minimizing
            max_time_parameter: int indicating amount of time to run engine
            move_history: list of previous moves
            alpha: alpha value for alpha-beta pruning
            beta: beta value for alpha-beta pruning
        Returns:
            Tuple of evaluation for a move sequence and move history of said sequence"""
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
            current_board.make_move_board(move[0],move[1],move[2])
            new_moves = all_moves(current_board,"B")
            new_move_history = move_history.copy()
            new_move_history.append(move)
            score = alphabetaminimax(current_board, new_moves, depth-1, False, new_move_history, alpha, beta)  
            current_board.undo_move_board()
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
            current_board.make_move_board(move[0],move[1],move[2])
            new_moves = all_moves(current_board,"W")
            new_move_history = move_history.copy()
            new_move_history.append(move)
            score = alphabetaminimax(current_board, new_moves, depth-1, True, new_move_history, alpha, beta)
            current_board.undo_move_board()
            if score:
                if min_score[0] > score[0]:
                    min_score = score
                    move_dict[current_hash] = move

                beta = min(beta, min_score[0])
                if beta <= alpha:
                    break
        return min_score