from Player import Player
import numpy as np
from random import randint

class MecatPlayer(Player):

    def name(self):
        return "Mecat"

    def max_value(self, board, Type, action, alpha, beta, player_code, p):
        if (p==0):
            return self.eval(player_code, board), Type, action
        sucessores = self.sucessores(player_code, board)
        for s in sucessores:
            mv, t, ac = self.min_value(s['board'],s['Type'], s['action'], alpha, beta, player_code, p-1)
            if (mv > alpha):
                alpha = mv
                action = ac
                Type = t
            if (alpha >= beta):
                return alpha, Type, action
        return alpha, Type,  action
    
    def min_value(self, board, Type, action, alpha, beta, player_code, p):
        if (p==0):
            return self.eval(player_code, board), Type, action
        sucessores = self.sucessores(player_code, board)
        for s in sucessores:
            mv, t, ac = self.max_value(s['board'],s['Type'], s['action'], alpha, beta, player_code, p-1)
            if (mv < beta):
                beta = mv
                action = ac
                Type = t
            if (beta <= alpha):
                return beta, Type, action 
        return beta, Type, action

    def isThereAnyEmergency(self, board, player_code):
        opponent = self.opponent(player_code)
        op_points_line = self.count_row_line(opponent, board)
        op_points_col = self.count_row_column(opponent, board)
        op_points_dig = self.count_row_diag(opponent, board)
        op_points_dig2 = self.count_row_diag(opponent, board[::-1])
        if (op_points_col['3'] > 0 or op_points_line['3'] > 0 or op_points_dig['3'] > 0 or op_points_dig2['3']> 0):
            return True
        return False


    def move(self, player_code, board):
        _, Type, action = self.max_value(board, None, None, -999999, 999999, player_code, 5)
        #
        # Poderiamos fazer soh o 
        #
        if (self.isThereAnyEmergency(board, player_code)):
            # simulando ser o adversario para identificar qual a jogada de vitoria
            sucessores = self.sucessores(self.opponent(player_code), board)
            for s in sucessores:
                v = self.eval(self.opponent(player_code), s['board'])
                if (v > 1):
                    return s['Type'], s['action']
        return Type, action
            

        # sucessores = self.sucessores(player_code, board)
        # max_eval = 0
        # action = randint(3, 5)
        # for s in sucessores:
        #     v = self.eval(player_code, s['board'])
        #     print(str(s['action'])+' '+str(v))
        #     if (v > max_eval):
        #         max_eval = v
        #         action = s['action']
        # return action

    def sucessores(self, player_code, board):
        suc = []
        for i in range(0,7):
            t, b = self.movement(player_code, board, i)
            if(b is not None):
                suc.append({'board':b,'Type':t,'action':i})
        return suc

    def opponent(self, player):
        if player==1:
            return 2
        return 1

    def domain_center(self, player, board):
        h = np.matrix([
            [0., 0., 0., 0., 0., 0., 0.],
            [0., 0., 0., 0., 0., 0., 0.],
            [0., 0., 1., 1., 1., 0., 0.],
            [0., 0., 1., 1., 1., 0., 0.],
            [0., 0., 1., 1., 1., 0., 0.],
            [0., 1., 1., 1., 1., 1., 0.]])
        
        return np.sum(np.logical_and(board==player, h))

    def eval(self, player, board): 
        my_points_line = self.count_row_line(player, board)
        my_points_col = self.count_row_column(player, board)
        my_points_dig = self.count_row_diag(player, board)
        my_points_dig2 = self.count_row_diag(player, board[::-1])
        my_qtd_2 = my_points_line['2'] + my_points_col['2'] + my_points_dig['2'] + my_points_dig2['2']
        my_qtd_3 = my_points_line['3'] + my_points_col['3'] + my_points_dig['3'] + my_points_dig2['3']
        my_qtd_4 = my_points_line['4'] + my_points_col['4'] + my_points_dig['4'] + my_points_dig2['4']
        #print('my 2', str(my_qtd_2))
        #print('my 3', str(my_qtd_3))
        #print('my 4', str(my_qtd_4))
        sum_my_points = 0.9*my_qtd_4 + 0.3*my_qtd_3 + 0.1*my_qtd_2

        opponent = self.opponent(player)
        op_points_line = self.count_row_line(opponent, board)
        op_points_col = self.count_row_column(opponent, board)
        op_points_dig = self.count_row_diag(opponent, board)
        op_points_dig2 = self.count_row_diag(opponent, board[::-1])
        op_qtd_2 = op_points_line['2'] + op_points_col['2'] + op_points_dig['2'] + op_points_dig2['2']
        op_qtd_3 = op_points_line['3'] + op_points_col['3'] + op_points_dig['3'] + op_points_dig2['3']
        op_qtd_4 = op_points_line['4'] + op_points_col['4'] + op_points_dig['4'] + op_points_dig2['4']
        #print('op 2', str(op_qtd_2))
        #print('op 3', str(op_qtd_3))
        #print('op 4', str(op_qtd_4))
        sum_op_points = 0.9*op_qtd_4 + 0.3*op_qtd_3 + 0.1*op_qtd_2
    
        return sum_my_points - sum_op_points + self.domain_center(player, board)

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

    
    def movement(self, player, board, column):
        result_board = np.copy(np.matrix(board))
        for i in range(5,-2,-1):
            if (i == 5 and result_board[i,column] == player):
                if(self.bottomDiscExist(player, result_board, column)):
                    break
            if (board[i,column] == 0):
                break
        if(i<0):
            return None, None
        if(i == 5 and result_board[5,column] == player):
            result_board = self.PopOut(result_board,column)
            return 'p', result_board
        if(i >= 0 and i <= 5 and board[i,column] == 0):
            result_board[i, column] = player
            return None, result_board

    def bottomDiscExist(self, player_code, board, column):
        if board[5][column] == player_code:
            return True
        return False

    def PopOut(self, board, column):
        col = board[:,column].astype(int).tolist()
        col.pop()
        col.insert(0,0)
        board[:,column] = col
        return board