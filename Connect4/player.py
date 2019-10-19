from state import *
import copy
import ipdb
import math

class Player():
    def __init__(self):
        pass

    def get_move(self, state):
        pass

class RandomPlayer(Player):
    def __init__(self):
        pass

    def get_move(self, state):
        moves = state.moves_available()
        return np.random.choice(moves)

class MachinePlayer(Player):
    def __init__(self, iterations = 50, time = 1):
        self.time = time
        self.iterations = iterations

    class Node():
        def __init__(self, state):
            self.state = copy.deepcopy(state)
            self.wins = 0
            self.playouts = 0
            self.children = None
            self.moves = None

        def expand(self):
            self.children = []
            self.moves = []
            for m in self.state.moves_available():
                self.children.append(MachinePlayer.Node(self.state))
                self.children[-1].state.move(m)
                self.moves.append(m)

        def choose_child(self):
            def child_criterion(child_node):
                return child_node.wins/(1+child_node.playouts)    \
                    +math.sqrt(2*math.log(self.playouts)/(1+child_node.playouts))
            child_index = np.argmax([child_criterion(c) for c in self.children])
            return self.children[child_index]
            
        def choose_optimal_move(self):
            win_ratios = [c.wins/c.playouts for c in self.children if c.playouts > 0]
            optimal_index = np.argmax(win_ratios)
            return self.moves[optimal_index]

        def playout(self):
            curr_state = copy.deepcopy(self.state)
            while True:
                moves = curr_state.moves_available()
                if moves == []:
                    return curr_state.result()
                curr_state.move(np.random.choice(moves))                    
        
    def get_move(self, state):
        head = MachinePlayer.Node(state)
        for i in range(self.iterations): #or time
            path = [head]
            while path[-1].children is not None and path[-1].children != []:
                path.append(path[-1].choose_child())
            if path[-1].children is None:
                path[-1].expand()
            result = path[-1].playout()
            for n in path:
                n.playouts += 1
                if result == 0:
                    n.wins += 0.5 
                elif result != n.state.player_num:
                    n.wins += 1
        #ipdb.set_trace()
        return head.choose_optimal_move()
        
