from C4 import *

'''
c4state = C4State()
print(c4state)
print('moves_available: ' + str(c4state.moves_available()))
c4state.board[:, 1] = 1
print('c4state.column_available(1) ' + str(c4state.column_available(1)))
print(c4state)
print('moves_available: ' + str(c4state.moves_available()))
c4state.move(0)
print(c4state)
'''

c4 = C4Game(C4HumanPlayer(), MachinePlayer(iterations=1000))

c4.go()
