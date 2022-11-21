from random import randint
from Player import Player

from Player import Player
import numpy as np
import math
import random

ROW_COUNT = 6
COLUMN_COUNT = 7

#other_player(player_code) = 1
AI_PIECE = 2
EMPTY = 0

WINDOW_LENGTH = 4

def winning_move(board, piece):
	# Check horizontal locations for win
	for c in range(COLUMN_COUNT-3):
		for r in range(ROW_COUNT):
			if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
				return True

	# Check vertical locations for win
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT-3):
			if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
				return True

	# Check positively sloped diaganols
	for c in range(COLUMN_COUNT-3):
		for r in range(ROW_COUNT-3):
			if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
				return True

	# Check negatively sloped diaganols
	for c in range(COLUMN_COUNT-3):
		for r in range(3, ROW_COUNT):
			if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
				return True

def is_terminal_node(board,player_code):
    #print(f"wP={winning_move(board, other_player(player_code))}")
    #print(f"wAI={winning_move(board, player_code)}")
    #print(f"len={len(get_valid_locations(board)) == 0}")
    return winning_move(board, other_player(player_code)) or winning_move(board, player_code) or (len(get_valid_locations(board)) == 0 and len(get_valid_removals(board,player_code)) == 0)

def is_valid_location(board, col):
	return board[0][col] == 0

def get_valid_locations(board):
	valid_locations = []
	for col in range(COLUMN_COUNT):
		if is_valid_location(board, col):
			valid_locations.append(col)
	return valid_locations

def bottomDiscExist(player_code, board, column):
        if board[5][column] == player_code:
            return True
        return False

def get_valid_removals(board,player_code):
    valid_removals = []
    for col in range(COLUMN_COUNT):
        if bottomDiscExist(player_code,board,col):
            valid_removals.append(col)
    return valid_removals

def evaluate_window(window, piece, player_code):
	score = 0
	opp_piece = other_player(player_code)
	if piece == other_player(player_code):
		opp_piece = player_code

	if window.count(piece) == 4:
		score += 100
	elif window.count(piece) == 3 and window.count(EMPTY) == 1:
		score += 5
	elif window.count(piece) == 2 and window.count(EMPTY) == 2:
		score += 2

	if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
		score -= 4

	return score

def score_position(board, piece,player_code):
	score = 0

	## Score center column
	center_array = [int(i) for i in list(board[:, COLUMN_COUNT//2])]
	center_count = center_array.count(piece)
	score += center_count * 3

	## Score Horizontal
	for r in range(ROW_COUNT):
		row_array = [int(i) for i in list(board[r,:])]
		for c in range(COLUMN_COUNT-3):
			window = row_array[c:c+WINDOW_LENGTH]
			score += evaluate_window(window, piece,player_code)

	## Score Vertical
	for c in range(COLUMN_COUNT):
		col_array = [int(i) for i in list(board[:,c])]
		for r in range(ROW_COUNT-3):
			window = col_array[r:r+WINDOW_LENGTH]
			score += evaluate_window(window, piece,player_code)

	## Score posiive sloped diagonal
	for r in range(ROW_COUNT-3):
		for c in range(COLUMN_COUNT-3):
			window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
			score += evaluate_window(window, piece,player_code)

	for r in range(ROW_COUNT-3):
		for c in range(COLUMN_COUNT-3):
			window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
			score += evaluate_window(window, piece,player_code)

	return score

def get_next_open_row(board, col):
	for r in reversed(range(ROW_COUNT)):
		if board[r][col] == 0:
			return r

def drop_piece(board, row, col, piece):
	board[row][col] = piece

def drop_col(board, col):
    for row in reversed(range(len(board))):
        if row == 0:
            board[row][col] = 0
        board[row][col] = board[row-1][col]

def minimax(board, depth, alpha, beta, maximizingPlayer,player_code):
	valid_locations = get_valid_locations(board)
	is_terminal = is_terminal_node(board,player_code)
	if depth == 0 or is_terminal:
		if is_terminal:
			if winning_move(board, player_code):
				return (None, 100000000000000,None)
			elif winning_move(board, other_player(player_code)):
				return (None, -10000000000000,None)
			else: # Game is over, no more valid moves
				return (None, 0,None)
		else: # Depth is zero
			return (None, score_position(board, player_code,player_code),None)
	if maximizingPlayer:
		valid_removals = get_valid_removals(board,player_code)
		value = -math.inf
		column = random.choice(valid_locations)
		removing = None
		for col in valid_locations:
			row = get_next_open_row(board, col)
			b_copy = board.copy()
			drop_piece(b_copy, row, col, player_code)
			new_score = minimax(b_copy, depth-1, alpha, beta, False,player_code)[1]
			if new_score > value:
				value = new_score
				column = col
			alpha = max(alpha, value)
			if alpha >= beta:
				break
		for col in valid_removals:
			b_copy = board.copy()
			drop_col(b_copy, col)
			new_score = minimax(b_copy, depth-1, alpha, beta, False,player_code)[1]
			if new_score > value:
				value = new_score
				column = col
				rem = 'p'
			alpha = max(alpha, value)
			if alpha >= beta:
				break
		return column, value, removing

	else: # Minimizing player
		valid_removals = get_valid_removals(board,other_player(player_code))
		value = math.inf
		column = random.choice(valid_locations)
		removing = False
		for col in valid_locations:
			row = get_next_open_row(board, col)
			b_copy = board.copy()
			drop_piece(b_copy, row, col, other_player(player_code))
			new_score = minimax(b_copy, depth-1, alpha, beta, True,player_code)[1]
			if new_score < value:
				value = new_score
				column = col
			beta = min(beta, value)
			if alpha >= beta:
				break
		for col in valid_removals:
			b_copy = board.copy()
			drop_col(b_copy, col)
			new_score = minimax(b_copy, depth-1, alpha, beta, False,player_code)[1]
			if new_score > value:
				value = new_score
				column = col
				removing = 'p'
			alpha = max(alpha, value)
			if alpha >= beta:
				break
		return column, value, removing

    
def other_player(player_code):
	if player_code == 1:
		return 2
	return 1


class MyPlayer(Player):

    def name(self):
        return "Marco"

    

    

    def isThereNoSpace(self, board, column): 
        if board[0][column] != 0:
            return True
        return False

    def move(self,  player_code, board, depth=6):

        col, minimax_score,removing = minimax(board, depth, -math.inf, math.inf, True, player_code)
        #print([removing,minimax_score,col])
        return removing,col
    
"""     def move(self, player_code, board):
        x = randint(0,13)
        if x >= 7:
            p = x - 7
            if self.bottomDiscExist(player_code, board, p):
                #print(f'p{p}')
                return 'p', p
        
        x = randint(0,6)
        while self.isThereNoSpace(board, x):
            x = randint(0,6)
        #print(x)
        return None, x """

