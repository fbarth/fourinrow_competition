# Implementig a player for the game Four in a Row Popout
from random import randint
from Player import Player
from math import inf
import numpy as np


class PalestraPlayer(Player):
    def __init__(self):
        self.player_code = None
        self.opponent_code = None

    def name(self):
        return "Palestra"

    def move(self, player_code, board):
        """Return the best movement"""

        # Set the player code
        self.player_code = player_code
        self.opponent_code = 1 if player_code == 2 else 2

        # Get the best movement
        oppenent_moves = self.get_children(board, self.opponent_code)
        for child in oppenent_moves:
            if self.is_winning(child["board"], self.opponent_code):
                if child["action"] != "p":
                    return child["action"], child["column"]

        player_moves = self.get_children(board, self.player_code)
        for child in player_moves:
            # Check if the opponent can win in the next movement
            if self.is_winning(child["board"], self.player_code):
                return child["action"], child["column"]

        score, best_move = self.min_max(board, 5, -inf, inf, True)

        # print("Score: ", score)
        # print("Best move: ", best_move)

        # Return the best movement of the agent
        return best_move["action"], best_move["column"]

    def min_max(self, board, depth, alpha, beta, maximizingPlayer):
        """Return the best movement of the board"""

        # If the depth is 0 or the game is over, return the score of the board
        if self.is_winning(board, self.player_code):
            return inf, None
        if self.is_winning(board, self.opponent_code):
            return -inf, None
        if depth == 0:
            return self.eval(board), None

        # If the player is maximizing, get the best movement
        if maximizingPlayer:
            best_score = -inf
            should_replace = lambda x: x > best_score
        # If the player is minimizing, get the worst movement
        else:
            best_score = inf
            should_replace = lambda x: x < best_score

        best_move = None

        # Get all possible movements
        children = self.get_children(
            board, self.player_code if maximizingPlayer else self.opponent_code
        )

        for child in children:
            temp = self.min_max(
                child["board"], depth - 1, alpha, beta, not maximizingPlayer
            )[0]

            if should_replace(temp):
                best_score = temp
                best_move = child

            if maximizingPlayer:
                alpha = max(alpha, best_score)
            else:
                beta = min(beta, best_score)

            if alpha >= beta:
                break

        return best_score, best_move

    def get_children(self, board, player_code):
        """https://github.com/kupshah/Connect-Four/blob/master/player.py"""

        children = []
        # Get all possible movements
        for i in range(7):
            # If the movement is valid on "i" column, add it to the children list
            new_board = self.movement(player_code, board, i)
            if new_board is not None:
                children.append({"board": new_board, "column": i, "action": None})

            # If the popout is valid on "i" column, add it to the children list
            new_board_pop = self.pop(player_code, board, i)
            if new_board_pop is not None:
                children.append({"board": new_board_pop, "column": i, "action": "p"})

        return children

    def domain_center(self, player, board):
        """Return the number of pieces in the center of the board"""
        h = np.matrix(
            [
                [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                [0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0],
                [0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0],
                [0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0],
                [0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0],
                [0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0],
            ]
        )

        return np.sum(np.logical_and(board == player, h))

    def eval(self, board):
        """Return the evaluation of the board"""

        # Get the quantity of pieces that are side by side of our player
        player_points_line = self.count_row_line(self.player_code, board)
        player_points_col = self.count_row_column(self.player_code, board)
        player_points_dig = self.count_row_diag(self.player_code, board)
        player_points_dig2 = self.count_row_diag(self.player_code, board[::-1])

        # Sum of occurences of pieces that are side by side by 2 pieces
        player_qtd_2 = (
            player_points_line["2"]
            + player_points_col["2"]
            + player_points_dig["2"]
            + player_points_dig2["2"]
        )

        # Sum of occurences of pieces that are side by side by 3 pieces
        player_qtd_3 = (
            player_points_line["3"]
            + player_points_col["3"]
            + player_points_dig["3"]
            + player_points_dig2["3"]
        )

        player_qtd_4 = (
            player_points_line["4"]
            + player_points_col["4"]
            + player_points_dig["4"]
            + player_points_dig2["4"]
        )

        # Get the quantity of pieces that are side by side of the opponent
        opponent_points_line = self.count_row_line(self.opponent_code, board)
        opponent_points_col = self.count_row_column(self.opponent_code, board)
        opponent_points_dig = self.count_row_diag(self.opponent_code, board)
        opponent_points_dig2 = self.count_row_diag(self.opponent_code, board[::-1])

        # Sum of occurences of pieces that are side by side by 2 pieces
        opponent_qtd_2 = (
            opponent_points_line["2"]
            + opponent_points_col["2"]
            + opponent_points_dig["2"]
            + opponent_points_dig2["2"]
        )

        # Sum of occurences of pieces that are side by side by 3 pieces
        opponent_qtd_3 = (
            opponent_points_line["3"]
            + opponent_points_col["3"]
            + opponent_points_dig["3"]
            + opponent_points_dig2["3"]
        )

        opponent_qtd_4 = (
            opponent_points_line["4"]
            + opponent_points_col["4"]
            + opponent_points_dig["4"]
            + opponent_points_dig2["4"]
        )

        if opponent_qtd_4 > 0:
            return -inf
        if player_qtd_4 > 0:
            return inf

        # Sum the points of our player
        sum_player_points = 100 * player_qtd_3 + player_qtd_2

        # Sum the points of our opponent
        sum_opponent_points = 1000 * opponent_qtd_3 + opponent_qtd_2

        return (
            sum_player_points
            - sum_opponent_points
            + self.domain_center(self.player_code, board)
        )

    def count_row_line(self, player, board):
        """Return the quantity of pieces that are side by side by 2 or 3 pieces in the lines"""
        retorno = {"2": 0, "3": 0, "4": 0}
        for i in range(6):
            counter = 0
            for j in range(6):
                if (board[i, j] == player) and (board[i, j] == board[i, j + 1]):
                    counter = counter + 1
                else:
                    counter = 0
                if counter == 1:
                    retorno["2"] += 1
                if counter == 2:
                    retorno["3"] += 1
                if counter == 3:
                    retorno["4"] += 1
        return retorno

    def count_row_column(self, player, board):
        """Return the quantity of pieces that are side by side by 2 or 3 pieces in the columns"""
        retorno = {"2": 0, "3": 0, "4": 0}
        for i in range(6):
            counter = 0
            for j in range(5):
                if (board[j, i] == player) and (board[j, i] == board[j + 1, i]):
                    counter = counter + 1
                else:
                    counter = 0
                if counter == 1:
                    retorno["2"] += 1
                if counter == 2:
                    retorno["3"] += 1
                if counter == 3:
                    retorno["4"] += 1
        return retorno

    def count_row_diag(self, player, board):
        """Return the quantity of pieces that are side by side by 2 or 3 pieces in the diagonals"""
        retorno = {"2": 0, "3": 0, "4": 0}
        for k in range(-2, 4):
            counter = 0
            x = np.diag(board, k=k)
            for i in range(0, len(x) - 1):
                if (x[i] == player) and (x[i] == x[i + 1]):
                    counter = counter + 1
                else:
                    counter = 0
                if counter == 1:
                    retorno["2"] += 1
                if counter == 2:
                    retorno["3"] += 1
                if counter == 3:
                    retorno["4"] += 1
        return retorno

    def movement(self, player, board, column):
        result_board = np.matrix(board)

        for i in range(5, -2, -1):
            if board[i, column] == 0:
                break
        if i < 0:
            return None

        result_board[i, column] = player
        return result_board

    def pop(self, player, board, column):
        result_board = np.matrix(board)

        if result_board[5, column] == player:
            for i in range(1, 6):
                result_board[i, column] = result_board[i - 1, column]

            result_board[0, column] = 0

            return result_board
        else:
            return None

    def is_winning(self, board, player):
        player_points_line = self.count_row_line(player, board)
        player_points_col = self.count_row_column(player, board)
        player_points_dig = self.count_row_diag(player, board)
        player_points_dig2 = self.count_row_diag(player, board[::-1])

        player_qtd_4 = (
            player_points_line["4"]
            + player_points_col["4"]
            + player_points_dig["4"]
            + player_points_dig2["4"]
        )

        return player_qtd_4 > 0
