import numpy as np

class Board:
    def __init__(self, n, symbol_1 = 'X', symbol_2 = 'O'):
        self.n = n
        self.symbol_1 = symbol_1
        self.symbol_2 = symbol_2
        self.board = np.zeros((n, n), dtype=int)
        
    def valid_move(self, i, j):
        if type(i) != int or type(j) != int:
            return False
        if i < 0 or i >= self.n or j < 0 or j >= self.n:
            return False
        return (self.board[i,j] == 0)

    def empty_squares(self):
        moves = []
        for i in range(self.n):
            for j in range(self.n):
                if self.board[i,j] == 0:
                    moves.append((i,j))
        return moves

    def moves_available(self):
        if self.result() is not None:
            return []
        else:
            return self.empty_squares()
            
    
    def result(self): #1 if 1 wins, -1 if -1 wins, 0 if tie, None if moves remaining and no winner
        def check_row(array): #return 1 if 1 wins, -1 if -1 wins, 0 else
            first_el = array[0]
            for x in array[1:]:
                if x != first_el:
                    return 0
            return first_el
        for i in range(self.n):
            row_result = check_row(self.board[i, :])
            if row_result != 0:
                return row_result
        for j in range(self.n):
            col_result = check_row(self.board[:, j])
            if col_result != 0:
                return col_result
        diagonal_result = check_row(self.board.diagonal())
        if diagonal_result != 0:
            return diagonal_result
        anti_diagonal_result = check_row(np.fliplr(self.board).diagonal())
        if anti_diagonal_result != 0:
            return anti_diagonal_result
        if self.empty_squares() == []:
            return 0
        return None
                           
    def __str__(self):
        rtn = ''
        for i in range(self.n):
            for j in range(self.n):
                if self.board[i,j] == 1:
                    rtn += self.symbol_1 + '|'
                elif self.board[i,j] == -1:
                    rtn += self.symbol_2 + '|'
                else:
                    rtn += ' |'
            rtn = rtn[:-1] #remove final |
            if i != self.n-1:
                rtn += '\n' + (2*self.n-1)*'-' + '\n'
        return rtn

    def __getitem__(self, key):
        return self.board[key]

    def __setitem__(self, key, value):
        self.board[key] = value

    def __copy__(self):
        rtn = Board(self.n, self.symbol_1, self.symbol_2)
        rtn.board = np.copy(self.board)
        return rtn
