# function_tests.py

"""
Testing the for the game functions
to help troubleshoot and ensure no new
bugs were introduced
"""

from backgammon import *
import numpy as np
import random


def check_moves(m1,  m2):
	"""
	Takes in two move arrays and
	returns if they are the same or not
	"""
	if (len(m1) != len(m2)):
		return False
	for m in m1:
		if not (m in m2):
			return False
	return True

# Test someone at the bar
board = init_state()
board[24] = 1
moves = get_possible_moves(board, 1, "player 1")
assert(moves == [[24, 0]])

# Test Standard move
board = init_state()
moves = get_possible_moves(board, 1, "player 1")
assert(check_moves(moves, [[0, 1], [16, 17], [18, 19]]))

# Test Bigger move
board = init_state()
moves = get_possible_moves(board, 5, "player 1")
assert(check_moves(moves, [[11, 16], [16, 21]]))

# Test most in last quadrant except one
board = init_state()
board[0] = 0
board[11] = 0
board[16] = 1
board[18] = 0
board[19] = 5
board[20] = 5
moves = get_possible_moves(board, 6, "player 1")
# print(moves)
assert(check_moves(moves, [[16, 22]]))

# Test all in last quadrant, ready to move
board = init_state()
board[0] = 0
board[11] = 0
board[16] = 0
board[18] = 0
board[22] = 5
moves = get_possible_moves(board, 2, "player 1")
# print(moves)
assert(check_moves(moves, [[22, 26]]))

# Another end state test with bigger roll
board = init_state()
board[0] = 0
board[11] = 0
board[16] = 0
board[18] = 0
board[22] = 5
moves = get_possible_moves(board, 5, "player 1")
# print(moves)
assert(check_moves(moves, [[22, 26]]))

# Test allowed to send an opponent to bar
board = init_state()
board[5] = -1
moves = get_possible_moves(board, 5, "player 1")
# print(moves)
assert(check_moves(moves, [[0, 5], [11, 16], [16, 21]]))

# Test standard player two move
board = init_state()
moves = get_possible_moves(board, 3, "player 2")
# print(moves)
assert(check_moves(moves, [[23, 20], [12, 9], [7, 4], [5, 2]]))

# Test someone at the bar
board = init_state()
board[25] = -1
moves = get_possible_moves(board, 1, "player 2")
# pretty_print(board)
# print(moves)
assert(moves == [[25, 23]])

# Case when there are no possible moves for player 2
board = init_state()
board[23] = 0
board[12] = 0
# board[5] = 0
board[7] = 0
moves = get_possible_moves(board, 5, "player 2")
# print(moves)
assert(moves == [])

# Player 2 end game affirmative
board = init_state()
board[23] = 0
board[12] = 0
# board[5] = 0
board[7] = 0
# pretty_print(board)
moves = get_possible_moves(board, 6, "player 2")
# print(moves)
assert(check_moves(moves, [[5, 27]]))

# Player 2 end game negative, but close
board = init_state()
board[23] = -1
board[22] = 0
board[12] = 0
# board[5] = 0
board[7] = 0
moves = get_possible_moves(board, 6, "player 2")
# print(moves)
assert(check_moves(moves, [[23, 17]]))

# Player 2, but game is already over
board = init_state()
board[5] = 0
board[7] = 0
board[12] = 0
board[23] = 0
board[27] = -15
moves = get_possible_moves(board, 3, "player 2")
assert(check_moves(moves, []))



print("-"*20)
print("All tests passed")
print("-"*20)
