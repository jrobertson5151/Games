from board import *
import random
import re
import ipdb
import math

class Player():
    def __init__(self):
        pass

    def get_move(self, board, player_num):
        pass

class HumanPlayer(Player):
    def __init__(self):
        pass

    def get_move(self, board, player_num):
        print(board)
        if player_num == 1:
            player_symbol = board.symbol_1
        if player_num == -1:
            player_symbol = board.symbol_2
        print("You are " + player_symbol)
        valid_move = False
        c = re.compile(r'(\d+),\s*(\d+)')
        while not valid_move:
            move = input("What is your move? Enter in the form of i, j:\t")
            match = c.match(move)
            if match:
                if board.valid_move(int(match.group(1)), int(match.group(2))):
                    return (int(match.group(1)), int(match.group(2)))
            print("Invalid move. Try again.")

class RandomPlayer(Player):
    def __init__(self):
        pass

    def get_move(self, board, player_num):
        moves = board.moves_available()
        return moves[np.random.randint(len(moves))]

class MachinePlayer(Player):
    def __init__(self, iterations = 50):
        self.iterations = iterations

    class State():
        def __init__(self, board, player_num):
            self.board = board
            self.player_num = player_num

        def choose_random_move(self):
            moves = self.board.moves_available()
            if moves == []:
                return None
            next_move = random.choice(moves)
            return self.create_next_state(next_move)

        def create_next_state(self, move):
            new_board = self.board.__copy__()
            new_board[move] = self.player_num
            return MachinePlayer.State(new_board, self.player_num*-1)
        
        def child_states(self):
            moves = self.board.moves_available()
            children = []
            for m in moves:
                children.append(self.create_next_state(m))
            return children

        def playout(self):
            curr_state = self
            while True:
                next_state = curr_state.choose_random_move()
                if next_state is None:
                    return curr_state.board.result()
                curr_state = next_state        
        
    class Node():
        def __init__(self, state):
            self.state = state
            self.wins = 0
            self.playouts = 0
            self.children = None
            self.moves = None

        def expand(self):
            self.children = []
            self.moves = []
            for m in self.state.board.moves_available():
                self.children.append(MachinePlayer.Node(self.state.create_next_state(m)))
                self.moves.append(m)

        def choose_child(self):
            def child_criterion(child_node):
                return child_node.wins/(1+child_node.playouts)+math.sqrt(2*math.log(self.playouts)/(1+child_node.playouts))
            child_index = np.argmax([child_criterion(c) for c in self.children])
            return self.children[child_index]
            
        def choose_optimal_move(self):
            win_ratios = [c.wins/c.playouts for c in self.children if c.playouts > 0]
            optimal_index = np.argmax(win_ratios)
            return self.moves[optimal_index]
        
    def get_move(self, board, player_num):
        head = MachinePlayer.Node(MachinePlayer.State(board, player_num))
        for i in range(self.iterations):
            path = [head]
            while path[-1].children is not None and path[-1].children != []:
                path.append(path[-1].choose_child())
            if path[-1].children is None:
                path[-1].expand()
            result = path[-1].state.playout()
            for n in path:
                n.playouts += 1
                if result == 0:
                    n.wins += 0.5 
                elif result != n.state.player_num:
                    n.wins += 1
        ipdb.set_trace()
        return head.choose_optimal_move()
        
    
