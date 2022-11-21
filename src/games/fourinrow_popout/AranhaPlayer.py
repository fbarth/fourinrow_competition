import time
import numpy as np
from Player import Player

class AranhaPlayer(Player):
    
    def __init__(self):
        self.p = 4
        self.u = 0
        self.g = []
        self.t = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    def name(self):
        return "Aranhatron 8000"

    def minmax(self, board, action, player_code, p):
        self.u += 1
        terminal, placar = self.estado_terminal(board)
        if terminal:
            ##print(board, "\n", p, action, "\n")
            if (placar[player_code] > 0) and ((placar[self.opponent(player_code)] == 0) or (((self.p + p) % 2) == 0)):
                return 10**(10+p), action
            else:
                return -10**(10+p), action
        if p == 0:
            return (self.eval(player_code, board) - self.eval(self.opponent(player_code), board)), action
        if (((self.p + p) % 2) == 0):
            sucessores = self.sucessores(player_code, board)
        else:
            sucessores = self.sucessores(self.opponent(player_code), board)
        acoes = []
        for s in sucessores:
            acoes += [self.minmax(s['board'], s['action'] if p == self.p else action, player_code, p-1)]
        
        ##if p == self.p:
        ##print(p, acoes)

        valor = 0
        if (((self.p + p) % 2) == 0):
            valor = max(list(map(int, np.array(acoes)[:,0])))
            ##print("max")
        else:
            valor = min(list(map(int, np.array(acoes)[:,0])))
            ##print("min")
        
        ##print(valor, "\n")
        return acoes[list(map(int, np.array(acoes)[:,0])).index(valor)]

    def move(self, player_code, board):
        start = time.time()
        _, action = self.minmax(board, None, player_code, self.p)
        end = time.time()
        #print('Duration in seconds = '+str(end-start))
        if len(action) > 1:
            return 'p', int(action[-1])
        else:
            return None, int(action[-1])

    def sucessores(self, player_code, board):
        suc = []
        for i in range(0,7):
            for j in ["", "p"]:
                code = j + str(i)
                b = self.movement(player_code, board, code)
                if(b is not None):
                    suc.append({'board':b, 'action':code})
        return suc

    def opponent(self, player):
        return -player +3

    def domain_board(self, player, board):
        h = np.matrix([
            [3., 4., 5., 6., 5., 4., 3.],
            [4., 6., 8., 10., 8., 6., 4.],
            [5., 8., 11., 13., 11., 8., 5.],
            [5., 8., 11., 13., 11., 8., 5.],
            [4., 6., 8., 10., 8., 6., 4.],
            [12., 13., 14., 15., 14., 13., 12.]])
        
        return int(np.sum(np.multiply(board == player, h)))

    def eval(self, player, board):
        b = np.array(board)

        if player == 2:
            b = np.array(b)
            b[b == 1] = 3
            b[b == 2] = 1
            b[b == 3] = 2

        pseudo_board = np.array(b)
        for i in range(6):
            x = 0
            while(b[5-x, i] == 1):
                x += 1
            for j in range(5, -1, -1):
                if b[j, i] == 1:
                    for k in range(x):
                        if j+k+1 <= 5:
                            if pseudo_board[j+k+1][i] == 2:
                                pseudo_board[j+k+1][i] = 0

        sequencias = ()
        for i in range(7):  ## vertical
            sequencias += (tuple(b[:, i]),)
        for i in range(6):  ## horizontal
            sequencias += (tuple(pseudo_board[i]),)
        for i in range(-2, 4):  ## diagonais
            sequencias += (tuple(np.diag(pseudo_board, k=i)), tuple(np.diag(pseudo_board[::-1], k=i)))

        h = {
            (1,0,1,1,0,1): 5000,
            (0,1,1,1,0): 5000,
            (1,1,1,0): 1500,
            (1,1,0,1): 1500,
            (0,1,1,0,0): 500,
            (0,1,0,1,0): 500,
            (1,1,0,0,0): 300,
            (1,0,1,0,0): 300,
            (1,1,0,0): 100,
            (0,1,1,0): 100,
            (1,0,1,0): 100,
            (1,0,0,1): 100,
            (0,0,0,1,0,0,0): 3,
            (0,0,1,0,0,0): 2,
            (0,1,0,0,0): 1,
            (0,0,1,0,0): 1,
            (0,1,0,0): 1,
            (1,0,0,0): 1
        }
        
        valor = 0

        for seq in sequencias:
            combado = 0
            for combo in h:

                if combado == 1:
                    break

                for i in range(len(seq) - len(combo) +1):
                    if not(seq[i:i+len(combo)] == combo):
                        if not(seq[i:i+len(combo)] == combo[::-1]):
                            continue

                    valor += h[combo]
                    combado = 1
                    break

        return valor + self.domain_board(player, board)

    def movement(self, player, board, code):
        result_board = np.matrix(board)
        column = int(code[-1])
        if len(code) == 1:
            for i in range(5,-2,-1):
                if (board[i,column] == 0):
                    break
            if(i<0):
                return None
            result_board[i, column] = player
            return result_board
        else:
            if board[5, column] == player:
                for i in range(5,0,-1):
                    result_board[i, column] = result_board[i-1, column]
                    result_board[0, column] = 0
                return result_board
            else:
                return None

    def estado_terminal(self, board):
        sequencias = []
        b = np.array(board)
        for i in range(7):  ## vertical
            sequencias += [b[:, i]]
        for i in range(6):  ## horizontal
            sequencias += [b[i]]
        for i in range(-2, 4):  ## diagonais
            sequencias += [np.diag(b, k=i), np.diag(b[::-1], k=i)]

        placar = [0, 0, 0]
        for seq in sequencias:
            counter = 0
            for i in (range(len(seq)-1)):
                if ((seq[i] != 0) and (seq[i] == seq[i+1])):
                    counter += 1
                else:
                    counter = 0
                if counter == 3:
                    placar[int(seq[i])] += 1

        return (sum(placar) > 0), placar
