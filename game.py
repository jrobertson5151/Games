from board import *
from player import *

class Game():
    def __init__(self, n, player_1, player_2, first_move = 1):
        self.board = Board(n)
        self.player_1 = player_1
        self.player_2 = player_2
        self.mover = first_move

    def step(self): #return False if game over before move is made
        result = self.board.result()
        if result == 1:
            print("Player 1 wins!")
            print(self.board)
            return False
        elif result == -1:
            print("Player 2 wins!")
            print(self.board)
            return False
        elif result == 0:
            print("Tie")
            print(self.board)
            return False
        if self.mover == 1:
            (next_move_x, next_move_y) = self.player_1.get_move(self.board, 1)
            self.board.board[next_move_x, next_move_y] = 1
        elif self.mover == -1:
            (next_move_x, next_move_y) = self.player_2.get_move(self.board, -1)
            self.board.board[next_move_x, next_move_y] = -1
        self.mover *= -1
        return True
            
    def go(self):
        while self.step():
            continue
