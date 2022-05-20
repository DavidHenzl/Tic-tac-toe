"""
This class is responsible for storing the information about the current state of a tic-tac-toe game.
"""

import random


class GameState():
    def __init__(self):
        self.board = [
            ["-", "-", "-"],
            ["-", "-", "-"],
            ["-", "-", "-"]
        ]

        self.XToMove = random.choice([True, False])
        self.XToMoveLast = self.XToMove

    def EndGameCheck(self):
        triples = []
        winner = ""
        for i in range(len(self.board)):
            triples.append(self.board[i][0] +
                           self.board[i][1] + self.board[i][2])
            triples.append(self.board[0][i] +
                           self.board[1][i] + self.board[2][i])
        triples.append(self.board[0][0] + self.board[1][1] + self.board[2][2])
        triples.append(
            self.board[0][2] + self.board[1][1] + self.board[2][0])
        if "xxx" in triples:
            winner = "player X"
        elif "ooo" in triples:
            winner = "player O"
        elif "-" not in self.board[0] and "-" not in self.board[1] and "-" not in self.board[2]:
            winner = "draw"
        return winner
