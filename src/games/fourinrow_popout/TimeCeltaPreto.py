from Player import Player
import numpy as np
import math

class CeltaPretoPlayer(Player):
    def __init__(self):
        self.me = None
        self.win_con = False
        self.depth = 5

    def name(self):
        return "Celta Preto"

    def move(self, player_code, board):
        self.me = player_code

        _, action = self.max_value(board, None, -1000000, 1000000, player_code, self.depth)


        if (self.isThereAnyEmergency(board, player_code) and not self.win_con):
            sucessores = self.sucessores(self.opponent(player_code), board)
            for s in sucessores:
                if self.check_win(player_code, s['board']) == 0:
                    if s['action'][0] == 'p':
                        pass    #return 'p', int(s['action'][1])
                    else:
                        return None, int(s['action'])

        if self.win_con:
            self.win_con = False

        if action[0] == 'p':
            if board[5,int(action[1])] == player_code:
                return 'p', int(action[1])
            else: #entrega jogo
                col = self.concede(board)
                return None, col

        return None, int(action)

    def concede(self, board):
        for i in range(7):
            if board[0, i] == 0:
                return i

    def isThereAnyEmergency(self, board, player_code):
        opponent = self.opponent(player_code)
        op_points_line, gap = self.count_row_line(opponent, board)
        op_points_col = self.count_row_column(opponent, board)
        op_points_dig, gap = self.count_row_diag(opponent, board)
        op_points_dig2, gap = self.count_row_diag(opponent, board[::-1])
        if (op_points_col['3'] > 0 or op_points_line['3'] > 0 or op_points_dig['3'] > 0 or op_points_dig2['3']> 0 or gap):
            return True
        return False, 


    def max_value(self, board, action, alpha, beta, player_code, p):
        if self.check_win(self.me, board):
            return 100000, action
        elif self.check_win(self.me, board) == 0 or self.check_win(self.me, board) == 2:          
            return -100000, action
        else: 
            pass

        if (p==0):
            return self.eval(self.me, board), action

        sucessores = self.sucessores(self.me, board)

        for s in sucessores:
            mv, ac = self.min_value(s['board'], s['action'], alpha, beta, player_code, p-1)
            if (mv > alpha):
                alpha = mv
                if(p == self.depth):
                    action = s['action']
            if (alpha >= beta):
                return alpha, action
        return alpha, action
    
    def min_value(self, board, action, alpha, beta, player_code, p):
        if self.check_win(self.me, board):
            if p == self.depth - 1:
                self.win_con = True
                return 1000000, action #ganha jogo
            return 100000, action
        elif self.check_win(self.me, board) == 0 or self.check_win(self.me, board) == 2:
            return -100000, action
        else: 
            pass

        if (p==0):
            return self.eval(self.me, board), action
        sucessores = self.sucessores(self.opponent(self.me), board)
        for s in sucessores:
            mv, ac = self.max_value(s['board'], s['action'], alpha, beta, player_code, p-1)
            if (mv < beta):
                beta = mv
                #action = ac
            if (beta <= alpha):
                return beta, action 
        return beta, action

    def sucessores(self, player_code, board):
        suc = []
        for i in range(0,7):
            b = self.movement(player_code, board, i)
            if b is not None:
                suc.append({'board':b, 'action': str(i)})
            
            #Movimentos de retirada
            c = self.popout(player_code, board, i)
            if c is not None:
                suc.append({'board':c, 'action': 'p' + str(i)})

        return suc

    def movement(self, player, board, column):
        result_board = np.matrix(board)
        for i in range(5,-2,-1):
            if (board[i,column] == 0):
                break
        if(i<0):
            return None
        result_board[i, column] = player
        return result_board

    def opponent(self, player):
        if player==1:
            return 2
        return 1

    def count_row_line(self, player, board):
        retorno = {'2': 0, '3': 0, '4': 0}
        gap = False
        for i in range(6):
            counter = 0
            for j in range(6):
                if ((board[i, j] == player) and (board[i, j] == board[i, j + 1])):
                    counter = counter + 1
                else:
                    counter = 0
                if (counter==1):
                    retorno['2'] = retorno['2'] + 1
                    
                    if j-3 < 0 and board[i, j-2] != player and board[i, j-3] == player:
                        gap = True

                    try:
                        if board[i, j+3] == player and board[i, j+2] != player:
                            gap = True
                    except:
                        pass

                if (counter==2):
                    retorno['3'] = retorno['3'] + 1
                if (counter==3):
                    retorno['4'] = retorno['4'] + 1
        return retorno, gap
    

    def count_row_column(self, player, board):
        retorno = {'2': 0, '3': 0, '4': 0}
        for i in range(7):
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
        gap = False
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
                    
                    try:
                        if x[i - 2] == player and board[i - 1] != player:
                            gap = True
                    except:
                        pass

                    try:
                        if x[i + 3] == player and board[i + 2] != player:
                            gap = True
                    except:
                        pass

                if (counter==2):
                    retorno['3'] = retorno['3'] + 1
                if (counter==3):
                    retorno['4'] = retorno['4'] + 1
        return retorno, gap

    def domain_center(self, player, board):
        h = np.matrix([
            [0., 0., 0., 0., 0., 0., 0.],
            [0., 0., 0., 0., 0., 0., 0.],
            [0., 0., 1., 1., 1., 0., 0.],
            [0., 0., 1., 1., 1., 0., 0.],
            [0., 0., 1., 1., 1., 0., 0.],
            [0., 1., 1., 1., 1., 1., 0.]])
        
        return np.sum(np.logical_and(board==player, h))

    
    def popout(self, player, board, column):
        result_board = np.matrix(board)
        if board[5, column] == player:
            for i in range(5, 0, -1):
                result_board[i, column] = board[i-1, column]
            result_board[0, column] = 0
            return result_board 
        return None

    def check_win(self, player, board):
        my_points_line, _ = self.count_row_line(player, board)
        my_points_col = self.count_row_column(player, board)
        my_points_dig, _ = self.count_row_diag(player, board)
        my_points_dig2, _ = self.count_row_diag(player, board[::-1])

        opponent = self.opponent(player)
        op_points_line, _ = self.count_row_line(opponent, board)
        op_points_col = self.count_row_column(opponent, board)
        op_points_dig, _ = self.count_row_diag(opponent, board)
        op_points_dig2, _= self.count_row_diag(opponent, board[::-1])

        if my_points_line['4'] == 1 or my_points_col['4'] == 1 or my_points_dig['4'] == 1 or my_points_dig2['4'] == 1:
            return 1
        elif op_points_line['4'] == 1 or op_points_col['4'] == 1 or op_points_dig['4'] == 1 or op_points_dig2['4'] == 1:
            return 0
        elif (my_points_line['4'] == 1 or my_points_col['4'] == 1 or my_points_dig['4'] == 1 or my_points_dig2['4'] == 1) and (op_points_line['4'] == 1 or op_points_col['4'] == 1 or op_points_dig['4'] == 1 or op_points_dig2['4'] == 1):
            return 2
        else:
            return None

    def eval(self, player, board): 
        my_points_line, _ = self.count_row_line(player, board)
        my_points_col = self.count_row_column(player, board)
        my_points_dig, _ = self.count_row_diag(player, board)
        my_points_dig2, _ = self.count_row_diag(player, board[::-1])
        my_qtd_2 = my_points_line['2'] + my_points_col['2'] + my_points_dig['2'] + my_points_dig2['2']
        my_qtd_3 = my_points_line['3'] + my_points_col['3'] + my_points_dig['3'] + my_points_dig2['3']
    
        sum_my_points =  100*my_qtd_3 + my_qtd_2

        opponent = self.opponent(player)
        op_points_line, _ = self.count_row_line(opponent, board)
        op_points_col = self.count_row_column(opponent, board)
        op_points_dig, _ = self.count_row_diag(opponent, board)
        op_points_dig2, _ = self.count_row_diag(opponent, board[::-1])
        op_qtd_2 = op_points_line['2'] + op_points_col['2'] + op_points_dig['2'] + op_points_dig2['2']
        op_qtd_3 = op_points_line['3'] + op_points_col['3'] + op_points_dig['3'] + op_points_dig2['3']

        sum_op_points = 10000*op_qtd_3 + op_qtd_2
        
        return sum_my_points - sum_op_points + self.domain_center(player, board)