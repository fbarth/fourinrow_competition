from Player import Player
import numpy as np
from random import randint

#
# authors: Fabricio Barth
# date: May, 2020

class Trio_De_Ferro_Player(Player):

    def name(self):
        return "Trio_De_Ferro"

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

    def isThereAnyEmergency(self, board, player_code):
        '''
        Verifica se o oponente está prestes a vencer a partida
        '''
        opponent = self.opponent(player_code)
        op_points_line = self.count_row_line(opponent, board)
        op_points_col = self.count_row_column(opponent, board)
        op_points_dig = self.count_row_diag(opponent, board)
        op_points_dig2 = self.count_row_diag(opponent, board[::-1])
        if (op_points_col['3'] > 0 or op_points_line['3'] > 0 or op_points_dig['3'] > 0 or op_points_dig2['3']> 0):
            return True
        return False


    def move(self, player_code, board):
        '''
        Determina a jogado que o player vai fazer
        '''
        _, action = self.max_value(board, None, -999999, 999999, player_code, 7)
        #
        # Poderiamos fazer soh o 
        #
        if (self.isThereAnyEmergency(board, player_code)):
            # simulando ser o adversario para identificar qual a jogada de vitoria
            sucessores = self.sucessores(self.opponent(player_code), board)
            for s in sucessores:
                if type(s['action']) == int:
                    v = self.eval(self.opponent(player_code), s['board'])
                    if (v > 70000):
                        return None, s['action']
                else:
                    v = self.eval(self.opponent(player_code), s['board'])
                    if (v > 70000):
                        return 'p', int(s['action'])
            
        return None ,int(action)
            



    def sucessores(self, player_code, board):
        sucessors = []
        #a = None
        for i in range(0,7):
            #if (board[5,i] == player_code):
                #a = self.movement(player_code, board, 'p', i) # tirar a peça
            b = self.movement(player_code, board, None, i) # colocar a peça
            if(b is not None):
                sucessors.append({'board':b, 'action':i})
            #if(a is not None):
            #    sucessors.append({'board':a, 'action':str(i)})
        return sucessors

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
        my_points_line = self.count_row_line(player, board) # verificando MEU dicionario da linha
        my_points_col = self.count_row_column(player, board) # verificando MEU dicionario da coluna
        my_points_dig = self.count_row_diag(player, board) # verificando MEU dicionario da diagonal
        my_points_dig2 = self.count_row_diag(player, board[::-1]) # verificando MEU dicionario da outra diagonal
        my_qtd_2 = my_points_line['2'] + my_points_col['2'] + my_points_dig['2'] + my_points_dig2['2']
        my_qtd_3 = my_points_line['3'] + my_points_col['3'] + my_points_dig['3'] + my_points_dig2['3']
        my_qtd_4 = my_points_line['4'] + my_points_col['4'] + my_points_dig['4'] + my_points_dig2['4']
        #print('my 2', str(my_qtd_2))
        #print('my 3', str(my_qtd_3))
        #print('my 4', str(my_qtd_4))
        sum_my_points = 100000*my_qtd_4 + 100*my_qtd_3 + my_qtd_2

        opponent = self.opponent(player)
        op_points_line = self.count_row_line(opponent, board) # verificando dicionario da linha do OPONENTE
        op_points_col = self.count_row_column(opponent, board) # verificando dicionario da coluna do OPONENTE
        op_points_dig = self.count_row_diag(opponent, board) # verificando dicionario da diagonal do OPONENTE
        op_points_dig2 = self.count_row_diag(opponent, board[::-1]) # verificando dicionario da outra diagonal do OPONENTE
        op_qtd_2 = op_points_line['2'] + op_points_col['2'] + op_points_dig['2'] + op_points_dig2['2']
        op_qtd_3 = op_points_line['3'] + op_points_col['3'] + op_points_dig['3'] + op_points_dig2['3']
        op_qtd_4 = op_points_line['4'] + op_points_col['4'] + op_points_dig['4'] + op_points_dig2['4']
        #print('op 2', str(op_qtd_2))
        #print('op 3', str(op_qtd_3))
        #print('op 4', str(op_qtd_4))
        sum_op_points = 100000*op_qtd_4 + 10000*op_qtd_3 + op_qtd_2
        
        return sum_my_points - sum_op_points + self.domain_center(player, board)

    def count_row_line(self, player, board):
        '''
        Faz a contagem de peças nas linhas, e coloca no dicionario retorno
        '''
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
        '''
        Faz a contagem de peças nas coluna, e coloca no dicionario retorno
        '''
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
        '''
        Faz a contagem de peças nas diagonais, e coloca no dicionario retorno
        '''
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

    
    def movement(self, player, board, option, column):
        '''
        Define um novo tabuleiro a partir da inserção de uma peça
        '''
        result_board = np.matrix(board)
        if option == 'p': # retirando uma peça (pop)
            if int(board[5,column]) == player:
                for i in range(4,-1,-1):
                    board[i+1,column] =board[i,column]


        else: # colocando uma peça
            for i in range(5,-2,-1):
                if (board[i,column] == 0):
                    break
            if(i < 0):
                return None
            result_board[i, column] = player
        
        return result_board

