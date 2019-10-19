from player import *
from state import *

class Game():
    def __init__(self, player_1, player_2, player_num = 1):
        pass

    def step(self): #return False if game over before move is made
        result = self.state.result()
        if result == 1:
            print("Player 1 wins!")
            print(self.state)
            return False
        elif result == -1:
            print("Player 2 wins!")
            print(self.state)
            return False
        elif result == 0:
            print("Tie")
            print(self.state)
            return False
        if self.state.player_num == 1:
            move = self.player_1.get_move(self.state)
            self.state.move(move)
        elif self.state.player_num == -1:
            move = self.player_2.get_move(self.state)
            self.state.move(move)
        return True
            
    def go(self):
        while self.step():
            print(self.state)

