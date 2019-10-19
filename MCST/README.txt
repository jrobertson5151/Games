To use MCTS:
-write a state class with the following:
        -state.player_num = 1 or -1
        -state.result() returning 1 if player 1 has won, -1 if player -1 has won,
       		       0 is a tie, None is the game isn't over yet
	-state.moves_available() returning a list of moves
	-state.move(m) where m is a move (i.e. a member of whatever list moves_available() has returned) that returns a new state representing the result of playing m
-create an instance of MCTS with MCTS(iterations = 50, time = 1) 
