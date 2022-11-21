import sys
import datetime

try:
    if sys.argv[1] == 'log':
        sys.stderr = open('results/log_error_campeonato.txt', 'w')
        sys.stdout = open('results/log_campeonato.txt', 'w')
except IndexError:
    pass

from FourInRow import FourInRow
from RandomPlayer import RandomPlayer
from AIPlayer import AIPlayer
from BarthJrPlayer import BarthJrPlayer 
#from MecatPlayer import MecatPlayer
from AkatsukiPlayer import AkatsukiPlayer
from MCTSPlayer import MCTSPlayer
#from Bergsons4 import Bergsons4
from TimeCeltaPreto import CeltaPretoPlayer
from connect4_player import Player_x
from AranhaPlayer import AranhaPlayer
from MyPlayer import MyPlayer
#from PalestraPlayer import PalestraPlayer
from RoboticaPlayer import RoboticaPlayer
from Liga4 import Trio_De_Ferro_Player

players = [
    RandomPlayer(),
    AIPlayer(),
    BarthJrPlayer(),
    AkatsukiPlayer(),
    MCTSPlayer(),
    CeltaPretoPlayer(),
    Player_x(),
    AranhaPlayer(),
    MyPlayer(),
    RoboticaPlayer(),
    Trio_De_Ferro_Player()
    ]
    
points = {}
for p in players:
    points[p.name()] = 0

print(f'Tournament starting at {datetime.datetime.now()}')

for i in range(0,len(players)):
    for j in range(i+1, len(players)):
        print(players[i].name() + " vs "+players[j].name())
        winner = FourInRow(players[i], players[j]).game()
        if winner == 'DRAW':
            points[players[i].name()] += 0.5
            points[players[j].name()] += 0.5
        else:
            points[winner] += 1 

for i in range(0,len(players)):
    for j in range(i+1, len(players)):
        print(players[j].name() + " vs "+players[i].name())
        winner = FourInRow(players[j], players[i]).game()
        if winner == 'DRAW':
            points[players[i].name()] += 0.5
            points[players[j].name()] += 0.5
        else:
            points[winner] += 1

print(f'Tournament finishing at {datetime.datetime.now()}')

print('Results:')
print('\n')
print(points)
