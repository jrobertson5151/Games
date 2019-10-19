from game import *

'''
for j in range(10):
    b = Board(3)
    for i in range(3):
        for j in range(3):
            b.board[i, j] = np.random.choice([-1, 1])
    print(b)
    print("result is " + str(b.result()))

g = Game(3, HumanPlayer(), RandomPlayer())
g.go()
'''

g = Game(3, HumanPlayer(), MachinePlayer(20000))
g.go()
