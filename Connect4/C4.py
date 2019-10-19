from game import *
import re

class C4State(State):
    def __init__(self, player_num = 1, n = 6, m = 7, player1_sym = 'X', player2_sym = 'Y'):
        self.player_num = 1
        self.n = n
        self.m = m
        self.player1_sym = player1_sym
        self.player2_sym = player2_sym
        self.board = np.zeros((n,m), dtype=int)
        
    def __str__(self):
        def dig_to_char(x):
            if x == 1:
                return self.player1_sym
            elif x == -1:
                return self.player2_sym
            else:
                return ' '
        rtn = []
        for i in range(self.n):
            rtn.append('|'.join(dig_to_char(x) for x in self.board[i, :]))
        return 'Player ' + dig_to_char(self.player_num) + ' to move: \n' + \
            ('\n' + '-'*(2*self.m-1)+'\n').join(rtn) + \
            '\n' + ' '.join([str(i) for i in range(self.m)])
        
    def column_available(self, j):
        #return first row number that is unfilled in col j
        #if col j full, return None
        if j < 0 or j >= self.m:
            return None
        col = list(self.board[:, j])
        col.reverse()
        try:
            return self.n - 1 - col.index(0)
        except:
            return None
        
    def moves_available(self):
        if self.result() is not None:
            return []
        rtn = []
        for j in range(self.m):
            if self.column_available(j) is not None:
                rtn.append(j)
        return rtn
    
    def move(self, move):
        class InvalidMove(Exception):
            pass
        row_num = self.column_available(move)
        if move < 0 or move >= self.m or row_num is None:
            raise InvalidMove()
        self.board[row_num, move] = self.player_num
        self.player_num *= -1
        
    def result(self):
        def check_list(l):
            if len(l) <= 3:
                return 0
            for (i, p) in enumerate(l[:-3]):
                if p == l[i+1] and p == l[i+2] and p == l[i+3]:
                    return p
            return 0
        for i in range(self.n):
            v = check_list(list(self.board[i, :]))
            if v != 0:
                return v
        for j in range(self.m):
            v = check_list(list(self.board[:, j]))
            if v != 0:
                return v
        indices = [[(i,j) for i in range(self.n)
                    for j in range(self.m) if i + j == c]
                   for c in range(self.n+self.m-1)] 
        for l in indices:
            v = check_list(list(self.board[tuple(zip(*l))]))
            if v != 0:
                return v
        indices_2 = [[(i,j) for i in range(self.n)
                    for j in range(self.m) if i - j == c]
                   for c in range(-self.m+1, self.n)]
        for l in indices_2:
            v = check_list(list(self.board[tuple(zip(*l))]))
            if v != 0:
                return v
        for j in range(self.m):
            if self.column_available(j) is not None:
                return None
        return 0
            
class C4Game(Game):
    def __init__(self, player_1, player_2, player_num = 1, n = 6, m = 7):
        self.player_1 = player_1
        self.player_2 = player_2
        self.state = C4State(player_num, n, m)

class C4HumanPlayer(Player):
    def __init__(self):
        pass

    def get_move(self, state):
        #print(state)
        valid_move = False
        c = re.compile(r'(\d+)')
        while not valid_move:
            move_str = input("What is your move? Enter the column number:\t")
            match = c.match(move_str)
            if match:
                move = int(match.group(1))
                if state.column_available(move) is not None:
                    return move                    
                print("Invalid move. Try again.")
            else:
                print("Could not parse response.")
