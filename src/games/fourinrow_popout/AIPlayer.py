import copy
from Player import Player
import numpy as np
from random import randint

TOTAL_LINES = 6
TOTAL_COLUMNS = 7

TOP_LINE_INDEX = 0
BOTTOM_LINE_INDEX = TOTAL_LINES - 1

LEFT_COLUMN_INDEX = 0
RIGHT_COLUMN_INDEX = TOTAL_COLUMNS - 1
CENTER_INDEX = RIGHT_COLUMN_INDEX // 2

DROP_IN_ACTION = None
POP_OUT_ACTION = 'p'
MAX_DEPTH = 5

def new_counting(player_counting: dict, counter: int):
  if (counter==1):
    player_counting['2'] = player_counting['2'] + 1
  if (counter==2):
    player_counting['3'] = player_counting['3'] + 1
  if (counter==3):
    player_counting['4'] = player_counting['4'] + 1

  return player_counting

class Board:
  def __init__(self, board: list[list[float]]):
    self.board = board

  def array_to_bitstring(self, player_code) -> int:
    position = ''
    mask = ''
    # enemy = ''
    for j in range(TOTAL_COLUMNS - 1, -1, -1):
      mask += '0'
      position += '0'
      # enemy = '0'
      for i in range(TOTAL_LINES):
        value = self.board[i][j]
        if value == 0:
          position += '0'
          mask += '0'
        elif value == player_code:
          position += '1'
          mask += '1'
        else:
          position += '0'
          mask += '1'
          # enemy += '1'
    
    # print(position)
    # print(mask)
        
    # int(mask, 2)#, int(enemy, 2)
    return int(position, 2)

  def has_four_connect(self, player_code):
    bytestring = self.array_to_bitstring(player_code)
    # Horizontal check
    horizontal = bytestring & (bytestring >> 7)
    if horizontal & (horizontal >> 14):
      return True
    # Diagonal \
    diagonal = bytestring & (bytestring >> 6)
    if diagonal & (diagonal >> 12):
      return True
    # Diagonal /
    diagonal = bytestring & (bytestring >> 8)
    if diagonal & (diagonal >> 16):
      return True
    # Vertical
    vertical = bytestring & (bytestring >> 1)
    if vertical & (vertical >> 2):
      return True
    # Nothing found
    return False

  def is_empty(self) -> bool:
    return np.sum(self.board) == 0

  def is_column_full(self, column: int) -> bool:
    return self.board[TOP_LINE_INDEX][column] != 0

  def is_player_on_bottom(self, player_code: int, column: int):
    return self.board[BOTTOM_LINE_INDEX][column] == player_code

  def count_row_line(self, player_code: int):
    player_counting = {'2': 0, '3': 0, '4': 0}
    for line in range(TOTAL_LINES):
      counter = 0
      for column in range(TOTAL_COLUMNS - 1):
        if ((self.board[line, column] == player_code) and (self.board[line, column] == self.board[line, column + 1])):
          counter = counter + 1
          player_counting = new_counting(player_counting, counter)
        else:
          counter = 0
          
    return player_counting
    
  def count_row_column(self, player_code: int):
    player_counting = {'2': 0, '3': 0, '4': 0}
    for line in range(TOTAL_LINES):
      counter = 0
      for column in range(TOTAL_COLUMNS - 2):
        if ((self.board[column, line] == player_code) and (self.board[column,line] == self.board[column+1,line])):
          counter = counter + 1
          player_counting = new_counting(player_counting, counter)
        else:
          counter = 0
          
    return player_counting
    
  def count_row_diag(self, player_code: int, reverse: bool = False):
    player_counting = {'2': 0, '3': 0, '4': 0}
    board = self.board
    if reverse:
      board = board[::-1]
    for k in range(-2,4):
      counter = 0
      diag = np.diag(board, k=k)
      for line in range(0,len(diag)-1):
        if ((diag[line] == player_code) and (diag[line] == diag[line+1])):
          counter = counter + 1
          player_counting = new_counting(player_counting, counter)
        else:
          counter = 0

    return player_counting

  def is_one_move_to_finish(self, player_code: int) -> bool:
    player_points_line = self.count_row_line(player_code)
    player_points_col = self.count_row_column(player_code)
    player_points_dig = self.count_row_diag(player_code)
    player_points_dig2 = self.count_row_diag(player_code)
    if (player_points_col['3'] > 0 or player_points_line['3'] > 0 or player_points_dig['3'] > 0 or player_points_dig2['3'] > 0):
        return True
    return False

  def calc_points(self, player_code):
    points_line = self.count_row_line(player_code)
    points_col = self.count_row_column(player_code)
    points_dig = self.count_row_diag(player_code)
    points_dig2 = self.count_row_diag(player_code, reverse=True)
    qtd_2 = points_line['2'] + points_col['2'] + points_dig['2'] + points_dig2['2']
    qtd_3 = points_line['3'] + points_col['3'] + points_dig['3'] + points_dig2['3']
    qtd_4 = points_line['4'] + points_col['4'] + points_dig['4'] + points_dig2['4']
    sum_points = 100000*qtd_4 + 100*qtd_3 + qtd_2
    return sum_points

class State:
  def __init__(
    self,
    board: Board,
    column: int = CENTER_INDEX,
    action: str = ''
  ):
    self.board = board
    self.column = column
    self.action = action

  def domain_center(self, player, board):
        h = np.matrix([
            [0., 0., 0., 0., 0., 0., 0.],
            [0., 0., 0., 0., 0., 0., 0.],
            [0., 0., 1., 1., 1., 0., 0.],
            [0., 0., 1., 1., 1., 0., 0.],
            [0., 0., 1., 1., 1., 0., 0.],
            [0., 1., 1., 1., 1., 1., 0.]])
        
        return np.sum(np.logical_and(self.board.board==player, h))

  # Return state points
  def eval(self, player_code: int) -> float:
    return self.board.calc_points(player_code)

# AI that uses max-min to play connect-4 with alpha-beta pruning
class AIPlayer(Player):

    def name(self):
      return "AIPlayer"

    def move(self, player_code: float, board_matrix: list[list[float]]) -> tuple[str, float]:
      board = Board(board_matrix) # convert the board to a Board class
      player = player_code 
      opponent = self.opponent_code(player_code) # get the opponent code
    
      # If the board is empty, play in the center
      if board.is_empty():
        return (DROP_IN_ACTION, CENTER_INDEX)

      # Player is about to win, finish the game
      if board.is_one_move_to_finish(player):
        player_best_move = self.max_state(player, State(board), depth=1)
        return player_best_move.action, player_best_move.column

      # If the opponent is about to win, block it
      opponent_best_move = self.max_state(opponent, State(board, action=None), depth=1)
      if opponent_best_move.board.has_four_connect(opponent):
        return opponent_best_move.action, opponent_best_move.column


      # If the board is not empty, play using the max-min algorithm
      player_best_move = self.max_state(player, State(board))
      return player_best_move.action, player_best_move.column
    
    def max_state(
      self,
      player_code: int,
      state: State,
      alpha: int = -999999,
      beta: int = 999999,
      depth: int = MAX_DEPTH
    ) -> State:
      if (depth == 0):
        return state

      successors = self.successors(state.board, player_code)
      for successor in successors:
        min_state = self.min_state(player_code, successor, alpha, beta, depth - 1)
        min_value = self.eval(min_state.board, player_code)
        if min_value > alpha:
          alpha = min_value
          state = min_state
        if alpha >= beta:
          return state
        
      return state

    
    def min_state(
      self,
      player_code: int,
      state: State,
      alpha: int = -999999,
      beta: int = 999999,
      depth: int = MAX_DEPTH
    ) -> State:
      if (depth==0):
        return state

      successors = self.successors(state.board, player_code)
      for successor in successors:
        max_state = self.max_state(player_code, successor, alpha, beta, depth - 1)
        max_value = self.eval(max_state.board, player_code)
        if max_value < beta:
          beta = max_value
          state = max_state
        if beta <= alpha:
          return state
      return state

    def successors(self, board: Board, player_code: int) -> list[State]:
      next_successors = []
      for column in range(TOTAL_COLUMNS):
        if not board.is_column_full(column):
          next_successors.append(self.add_to_column(board, player_code, column))
        
        # if board.is_player_on_bottom(player_code, column):
        #   next_successors.append(self.pop_from_column(board, player_code, column))

      return next_successors

    def add_to_column(self, board: Board, player_code: int, column: int) -> State:
      result_board = np.array(board.board)
      for line in range(BOTTOM_LINE_INDEX, TOP_LINE_INDEX - 1, -1):
        if (result_board[line][column] == 0):
          result_board[line][column] = player_code
          return State(Board(result_board), column, DROP_IN_ACTION)

      return State(board, column, DROP_IN_ACTION)

    def pop_from_column(self, board: Board, player_code: int, column: int) -> State:
      result_board = np.array(board)
      for line in range(BOTTOM_LINE_INDEX, TOP_LINE_INDEX - 1, -1):
        if line < TOP_LINE_INDEX:
          result_board[line][column] = result_board[line - 1][column]

      return State(Board(result_board), column, POP_OUT_ACTION)

    def eval(self, board: Board, player_code) -> int:
      my_points = board.calc_points(player_code)
      opponent_points = board.calc_points(self.opponent_code(player_code))
      return my_points - opponent_points

    def opponent_code(self, player):
      if player==1:
          return 2
      return 1