import numpy as np
from Player import Player
class AkatsukiPlayer(Player):

    def __init__(self):
        self.firstMove = True

    def name(self):
        return "Akatsuki"

    def move(self, player_code, board):
        
        if self.firstMove:
            self.firstMove = False
            return None, 3
        _, action = self.max_value(board, None, -999999, 999999, player_code, 6)
        if (self.isThereAnyEmergency(board, player_code)):
            # simulando ser o adversario para identificar qual a jogada de vitoria
            sucessores = self.sucessores(self.opponent(player_code), board)
            for s in sucessores:
                v = self.eval(self.opponent(player_code), s['board'])
                if (v > 70000):
                    return s['action']        
        return action

    # def move(self, player, board):
    #     _, action = self.alphabeta(board, None, self.depth, -float('inf'), float('inf'), player)
    #     return action

    def max_value(self, board, action, alpha, beta, player_code, p):
        if (p==0):
            return self.eval(player_code, board), action
        sucessores = self.sucessores(player_code, board)
        for s in sucessores:
            mv, ac = self.min_value(s['board'], s['action'], alpha, beta, player_code, p-1)
            if (mv > alpha):
                alpha = mv
                action = ac
            if (alpha >= beta):
                return alpha, action
        return alpha, action
    
    def min_value(self, board, action, alpha, beta, player_code, p):
        if (p==0):
            return self.eval(player_code, board), action
        sucessores = self.sucessores(player_code, board)
        for s in sucessores:
            mv, ac = self.max_value(s['board'], s['action'], alpha, beta, player_code, p-1)
            if (mv < beta):
                beta = mv
                action = ac
            if (beta <= alpha):
                return beta, action 
        return beta, action

    #alpha = -inf
    #beta = inf
    depth = 5
    def alphabeta(self, board, action, depth, alpha, beta, player):
        if (depth == 0):
            return self.eval(player, board), action

        suc = self.sucessores(player, board)
        if player == 2:
            alpha = -float('inf')
            for i in suc:
                new_value, new_action = self.alphabeta(i["board"], i["action"], depth-1, alpha, beta, 2)    
                if (new_value > alpha):        
                    alpha = new_value
                    action = new_action
                    # alpha = max(alpha, value)
                if (alpha >= beta):
                    break
            return alpha, action
        elif player == 1:
            beta = float('inf')
            for i in suc:
                new_value, new_action = self.alphabeta(i["board"], i["action"], depth-1, alpha, beta, 1)            
                if (new_value < beta):        
                    beta = new_value
                    action = new_action
                # beta = min(beta, value)
                if (beta <= alpha):
                    break
                return beta, action

    def isThereAnyEmergency(self, board, player_code):
        opponent = self.opponent(player_code)
        op_points_line = self.count_row_line(opponent, board)
        op_points_col = self.count_row_column(opponent, board)
        op_points_dig = self.count_row_diag(opponent, board)
        op_points_dig2 = self.count_row_diag(opponent, board[::-1])
        if (op_points_col['3'] > 0 or op_points_line['3'] > 0 or op_points_dig['3'] > 0 or op_points_dig2['3']> 0):
            return True
        return False

    def opponent(self, player):
        if player==1:
            return 2
        return 1

    def eval(self, player, board): 
        my_points_line = self.count_row_line(player, board)
        my_points_col = self.count_row_column(player, board)
        my_points_dig = self.count_row_diag(player, board)
        my_points_dig2 = self.count_row_diag(player, board[::-1])
        my_points_isolated = self.calculate_isolated(self.find_isolated(player,board))
        my_qtd_2 = my_points_line['2'] + my_points_col['2'] + my_points_dig['2'] + my_points_dig2['2']
        my_qtd_3 = my_points_line['3'] + my_points_col['3'] + my_points_dig['3'] + my_points_dig2['3']
        my_qtd_4 = my_points_line['4'] + my_points_col['4'] + my_points_dig['4'] + my_points_dig2['4']
        sum_my_points = 10000*my_qtd_4 + 1000*my_qtd_3 + 100+my_qtd_2 + my_points_isolated
        
        opponent = self.opponent(player)
        op_points_line = self.count_row_line(opponent, board)
        op_points_col = self.count_row_column(opponent, board)
        op_points_dig = self.count_row_diag(opponent, board)
        op_points_dig2 = self.count_row_diag(opponent, board[::-1])
        op_points_isolated = self.calculate_isolated(self.find_isolated(opponent,board))
        op_qtd_2 = op_points_line['2'] + op_points_col['2'] + op_points_dig['2'] + op_points_dig2['2']
        op_qtd_3 = op_points_line['3'] + op_points_col['3'] + op_points_dig['3'] + op_points_dig2['3']
        op_qtd_4 = op_points_line['4'] + op_points_col['4'] + op_points_dig['4'] + op_points_dig2['4']
        sum_op_points = 10000*op_qtd_4 + 1000*op_qtd_3 + 100*op_qtd_2 + op_points_isolated
        return sum_my_points - sum_op_points

        
    def sucessores(self, player_code, board):
        suc = []
        for i in range(0,7):
            b0 = self.movement(player_code, board, i)
            if(b0 is not None):
                suc.append({'board' : b0, 'action' : (None, i)})

            b1 = self.movement_popout(player_code, board, i)
            if(b1 is not None):
                suc.append({'board' : b1, 'action' : ('p', i)})
        return suc

    def movement(self, player, board, column):
        # result_board = np.matrix(board)
        for i in range(5,-2,-1):
            if (board[i][column] == 0):
                board[i][column] = player
                return board
        return None

    def movement_popout(self, player, board, column):
        if self.bottomDiscExist(player, board, column):
            for i in range(5, -1,-1):
                if i == 0:
                    board[i][column] = 0
                else:
                    board[i][column] = board[i-1][column]
            
            return board
        return None
        
    def bottomDiscExist(self, player_code, board, column):
        board = board.tolist()
        if board[5][column] == player_code:
            return True
        return False

    def count_row_line(self, player, board):
        retorno = {'2': 0, '3': 0, '4': 0}
        for i in range(6):
            counter = 0
            for j in range(6):
                if ((board[i, j] == player) and (board[i, j] == board[i, j + 1])):
                    counter = counter + 1
                else:
                    counter = 0
                if (counter==1):
                    retorno['2'] = retorno['2'] + 1
                if (counter==2):
                    retorno['3'] = retorno['3'] + 1
                if (counter==3):
                    retorno['4'] = retorno['4'] + 1
        return retorno
    
    def count_row_column(self, player, board):
        retorno = {'2': 0, '3': 0, '4': 0}
        for i in range(6):
            counter = 0
            for j in range(5):
                if ((board[j, i] == player) and (board[j,i] == board[j+1,i])):
                    counter = counter + 1
                else:
                    counter = 0
                if (counter==1):
                    retorno['2'] = retorno['2'] + 1
                if (counter==2):
                    retorno['3'] = retorno['3'] + 1
                if (counter==3):
                    retorno['4'] = retorno['4'] + 1
        return retorno

    def count_row_diag(self, player, board):
        retorno = {'2': 0, '3': 0, '4': 0}
        board = np.matrix(board)
        for k in range(-2,4):
            counter = 0
            x = np.diag(board, k=k)
            for i in range(0,len(x)-1):
                if ((x[i] == player) and (x[i] == x[i+1])):
                    counter = counter + 1
                else:
                    counter = 0
                if (counter==1):
                    retorno['2'] = retorno['2'] + 1
                if (counter==2):
                    retorno['3'] = retorno['3'] + 1
                if (counter==3):
                    retorno['4'] = retorno['4'] + 1
        return retorno

    def find_isolated(self, player, board):
        board = board.tolist()
        
        height, width = len(board), len(board[0])
        isolated = {
            0 : 0,
            1 : 0,
            2 : 0,
            3 : 0,
            4 : 0,
            5 : 0,
            6 : 0
        }
        for row in range(height):
            for col in range(width):
                if board[row][col] == player:
                    notIsolated = False
                    if (board[row][col] == player):
                        if (width > col+1 and board[row][col+1] == player):
                            notIsolated = True
                        if (height > row+1 and board[row+1][col] == player):
                            notIsolated = True
                        if (row-1 > 0 and board[row-1][col] == player):
                            notIsolated = True
                        if (col-1 > 0 and board[row][col-1] == player):
                            notIsolated = True
                        if (height > row+1 and width > col+1 and board[row+1][col+1] == player):
                            notIsolated = True
                        if (height > row+1 and col-1 > 0 and board[row+1][col-1] == player):
                            notIsolated = True
                        if (row-1 > 0 and col-1 > 0 and board[row-1][col-1] == player):
                            notIsolated = True
                        if (row-1 > 0 and width > col+1 and board[row-1][col-1] == player):
                            notIsolated = True
                    if (not notIsolated):
                        isolated[col] += 1

        return isolated

    def calculate_isolated(self, isolated : dict):
        weights = {
            0 : 40,
            1 : 70,
            2 : 120,
            3 : 200,
            4 : 120,
            5 : 70,
            6 : 40
        }
        h = 0
        for iso_v, w_v in zip(isolated.values(), weights.values()):
            h += iso_v * w_v

        return h
                                    

