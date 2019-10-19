from state import *
import copy
import ipdb
import math
from itertools import count

#get_move takes a state. A state must have:
#an attribute player_num such that player_num = 1 or -1
#a function result() that equals player_num if that player has won,
#or 0 if the game has ended in a tie, or None is the game has not ended
#a function moves_available() giving the list of valid moves for the current player
#a function move(m) which given a move m returns the state resulting from m being played

class MCTS(Player):
    def __init__(self, iterations = 50, time = None):
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
        start_time = time.time() 
        for i in count():
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
            if self.iterations is not None and i >= self.iterations:
                break
            if self.time is not None and time.time()-start_time > self.time:
                break
        #ipdb.set_trace()
        return head.choose_optimal_move()
        
