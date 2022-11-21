from Player import Player
import numpy as np
import math
import random

ROW_COUNT = 6
COLUMN_COUNT = 7

PLAYER_PIECE = 1
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


def is_terminal_node(board):
	return winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE) or len(get_valid_locations(board)) == 0


def get_pop_valid_locations(valid_locations, board, maximizingPlayer):

	if maximizingPlayer:
		piece = AI_PIECE
	else:
		piece = PLAYER_PIECE
	# if depth > 6:
    # Verificar a ultima linha
	if board[0][3] == piece:
		valid_locations.append('p'+str(3))
	if board[0][4] == piece:
		valid_locations.append('p'+str(4))
	if board[0][2] == piece:
		valid_locations.append('p'+str(2))
	if board[0][5] == piece:
		valid_locations.append('p'+str(5))
	if board[0][1] == piece:
		valid_locations.append('p'+str(1))
	if board[0][6] == piece:
		valid_locations.append('p'+str(6))
	if board[0][0] == piece:
		valid_locations.append('p'+str(0))

	return valid_locations


def is_valid_location(board, col):
	return board[ROW_COUNT-1][col] == 0


def get_valid_locations(board):
	valid_locations = []

	if is_valid_location(board, 3):
		valid_locations.append(3)

	if is_valid_location(board, 4):
		valid_locations.append(4)

	if is_valid_location(board, 2):
		valid_locations.append(2)

	if is_valid_location(board, 5):
		valid_locations.append(5)

	if is_valid_location(board, 1):
		valid_locations.append(1)

	if is_valid_location(board, 6):
		valid_locations.append(6)

	if is_valid_location(board, 0):
		valid_locations.append(0)

	return valid_locations


def evaluate_window(window, piece):
	score = 0
	opp_piece = PLAYER_PIECE
	if piece == PLAYER_PIECE:
		opp_piece = AI_PIECE

	elif window.count(piece) == 3 and window.count(EMPTY) == 1:
		score += 100
	elif window.count(piece) == 3 and window.count(opp_piece) == 1:
		score += 10
	elif window.count(piece) == 2 and window.count(EMPTY) == 2:
		score += 5
	elif window.count(piece) == 2 and window.count(EMPTY) == 1:
		score += 2
	elif window.count(piece) == 2 and window.count(opp_piece) == 2:
		score += 2
	if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
		score -= 8
	if window.count(opp_piece) == 3 and window.count(piece) == 1:
		score -= 4

	return score


def score_position(board, piece):
	score = 0

	# Score center column
	center_array = [int(i) for i in list(board[:, COLUMN_COUNT//2])]
	center_count = center_array.count(piece)
	score += center_count * 2

	# Score Horizontal
	for r in range(ROW_COUNT):
		row_array = [int(i) for i in list(board[r, :])]
		for c in range(COLUMN_COUNT-3):
			window = row_array[c:c+WINDOW_LENGTH]
			score += evaluate_window(window, piece)

	# Score Vertical
	for c in range(COLUMN_COUNT):
		col_array = [int(i) for i in list(board[:, c])]
		for r in range(ROW_COUNT-3):
			window = col_array[r:r+WINDOW_LENGTH]
			score += evaluate_window(window, piece)

	# Score posiive sloped diagonal
	for r in range(ROW_COUNT-3):
		for c in range(COLUMN_COUNT-3):
			window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
			score += evaluate_window(window, piece)

	for r in range(ROW_COUNT-3):
		for c in range(COLUMN_COUNT-3):
			window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
			score += evaluate_window(window, piece)

	return score


def get_next_open_row(board, col):
	for r in range(ROW_COUNT):
		if board[r][int(str(col)[-1])] == 0:
			return r


def drop_piece(board, row, col, piece):
	board[row][col] = piece


def pop_piece(board, col):
	board[0][col] = board[1][col]
	board[1][col] = board[2][col]
	board[2][col] = board[3][col]
	board[3][col] = board[4][col]
	board[4][col] = board[5][col]
	board[5][col] = 0


def minimax(board, depth, alpha, beta, maximizingPlayer):
	valid_locations = get_valid_locations(board)
	valid_locations = get_pop_valid_locations(valid_locations, board, maximizingPlayer)
	is_terminal = is_terminal_node(board)
	if depth == 0 or is_terminal:
		if is_terminal:
			if winning_move(board, PLAYER_PIECE):
				return (None, -100000000000000*(depth+2))
			elif winning_move(board, AI_PIECE):
				return (None, 100000000000000*(depth+1))
			else:  # Game is over, no more valid moves
				return (None, 0)
		else:  # Depth is zero
			return (None, score_position(board, AI_PIECE))
	if maximizingPlayer:
		value = -math.inf
		column = 0
		for col in valid_locations:
			row = get_next_open_row(board, col)
			b_copy = board.copy()
			if 'p' in str(col):
				pop_piece(b_copy,int(col[-1]))
			else:
				drop_piece(b_copy, row, col, AI_PIECE)
			new_score = minimax(b_copy, depth-1, alpha, beta, False)[1]
			# if winning_move(board, AI_PIECE) and depth == 5:
			# 	return col, new_score
			if new_score > value:
				value = new_score
				column = col
			alpha = max(alpha, value)

			# if (depth==5): print(depth, value, new_score, column, valid_locations)
			if alpha >= beta:
				break

		return column, value

	else: # Minimizing player
		value = math.inf
		column = 0
		for col in valid_locations:
			row = get_next_open_row(board, col)
			b_copy = board.copy()

			if 'p' in str(col):
				pop_piece(b_copy, int(col[1]))
			else:
				drop_piece(b_copy, row, col, PLAYER_PIECE)
			new_score = minimax(b_copy, depth-1, alpha, beta, True)[1]
			# if winning_move(board, PLAYER_PIECE) and depth == 4:
			# 	return col, new_score
			if new_score < value:
				value = new_score
				column = col
			beta = min(beta, value)
			# if (depth==2): print(depth, value, new_score, column, valid_locations)
			if alpha >= beta:
				break
		return column, value

class Bergsons4(Player):
	def name(self):
		return "Bergsons4"
	
	def move(self, player_code, board, depth=5):
		col, minimax_score = minimax(np.flip(board,0), depth, -math.inf, math.inf, True)
		pop =  'p' if str(col)[0] == 'p' else None
		return pop, int(str(col)[-1])
