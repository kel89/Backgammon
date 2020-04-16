# backgammon.py

"""
Contrains the functions required to play a game
"""

import numpy as np
import random
from tqdm import tqdm
from RandomPlayer import *

def init_state():
	"""
	Retruns a new game state array for the start of a game
	"""
	state = np.zeros(28)

	# Place player one
	state[0] = 2
	state[11] = 5
	state[16] = 3
	state[18] = 5

	# Place player two
	state[5] = -5
	state[7] = -3
	state[12] = -5
	state[23] = -2

	return state


def pretty_print(board):
	"""
	Prints a nicer version of the game state to look
	like the board
	"""
	string = ""

	# Do the top of the board
	string += np.array2string(board[12:24]) + '\n'

	# Do the bottom of the board
	string += np.array2string(np.flip(board[0:12])) + '\n'

	# Show the bar
	string += 'Bar: ' + np.array2string(board[24:26]) + "\n"

	# Show the end
	string += 'End: ' + np.array2string(board[26:])

	print("Board:")
	print(string)


def roll():
	"""
	Returns dice roll values, will be an array of size either 2 or four
	indicating the number of moves that can be made (four if doubles)
	"""
	# Roll
	roll = np.random.randint(1, 7, 2)

	# Check for doubles
	if (roll[0] == roll[1]):
		roll = np.concatenate([roll, roll])

	return roll


def update_board(board, start, end):
	"""
	Takes in a game state board array, the
	index of a chip we would like to move, and
	the index of where we would like it to end up
	**This function does __not__ check if the
	requested move is legal

	Returns the updated game state array
	"""
	# Determine which player we are dealing with
	if (board[start] < 0):
		player = 'neg'
	elif (board[start] > 0):
		player = 'pos'
	else:
		raise ValueError("Moving from a place with no chips")


	# Update start and end positions
	if (player == 'pos'):
		board[start] -= 1

		# Check case we are sending a piece to the bar
		if (board[end] == -1):
			board[end] = 1
			board[25] -= 1
		else:
			# standard move
			board[end] += 1

	else:
		board[start] += 1

		# Check case we are sending piece to bar
		if (board[end] == 1):
			board[end] = -1
			board[24] += 1
		else:
			# standard move
			board[end] -= 1

	return board


def flip_board(board):
	"""
	Returns a copy of the game board with the points
	and values flipped to it always looks like player
	one is playing
	"""
	# Copy the board
	copy = np.copy(board)

	# Swap playing spots
	idx = np.concatenate([np.arange(23, -1, -1), [24, 25, 26, 27]])
	copy = copy[idx]

	# Swap bar and end
	idx = np.concatenate([np.arange(0, 24, 1), [25, 24, 27, 26]])
	copy = copy[idx]

	# Change signs
	copy = np.negative(copy)

	return copy


def flip_moves(moves):
	"""
	Flips the moves that are otherwise from the perspective
	of player 1 to player 2
	Swaps the bar and end spaces
	"""
	# print("Moves to flip", moves)
	new_moves = []
	for m in moves:
		move = []
		for p in m:
			# If normal game play space
			if (p <= 23):
				p1 = 23 - p
			# Special space, so swap it
			else:
				if (p == 24):
					p1 = 25
				elif (p == 25):
					p1 = 24
				elif (p == 26):
					p1 = 27
				else:
					p1 = 27

			move.append(p1)

		new_moves.append(move)
	return new_moves


def get_possible_moves(board, val, player):
	"""
	Returns an array of tuples that are the possible moves
	for player 1 based on a given game board and
	the roll of a single value
	"""
	# Copy the board
	bc = np.copy(board)

	# Set the board constants
	last_quad_start = 18
	bar = 24
	end_holder = 26

	if (player == "player 2"):
		bc = flip_board(bc)

	# Initialize move tracker
	possible_moves = []

	# Check if at the bar
	if (bc[bar] > 0):
		if bc[val-1] >= -1:
			possible_moves.append([bar, val-1])

	# None at the bar
	else:
		# get our inds
		our_inds = np.where(bc[0:24] > 0)[0] # as we don't want to consider end game state
		if (len(our_inds) == 0):
			return possible_moves

		# Check if last quadrant
		if (np.min(our_inds) >= last_quad_start):
			last_quad = True
		else:
			last_quad = False

		# Check possible chips to move
		for ind in our_inds:
			if (ind + val < 24): # note, other player moves in other direciton
				# legal, non chip removal move
				if (bc[ind + val] >= -1):
					possible_moves.append([ind, ind+val])
			else:
				if (last_quad):
					# then we can remove this piece
					possible_moves.append([ind, end_holder])

	# Check if we need to flip the moves
	if (player == "player 2"):
		possible_moves = flip_moves(possible_moves)

	return possible_moves



def get_all_moves(board, vals, player):
	"""
	Takes in a game board, the dice array
	and a string indicating which player we are dealign with
	and returns an array of the possible moves
	"""
	# Initialize move tracker
	moves = []

	# If not doubles
	if (len(vals) == 2):
		# Try val 1 then val 2-----------------------------------------------------
		possible_first_moves = get_possible_moves(board, vals[0], player)

		# For each of the possible first moves, get the seoncd
		for m in possible_first_moves:
			# Get the new board state
			tmp_board = np.copy(board)
			tmp_board = update_board(tmp_board, m[0], m[1])
			possible_second_moves = get_possible_moves(tmp_board, vals[1], player)

			# Keep track of each of the second state moves
			if (len(possible_second_moves) == 0): moves.append([m]) # in case no second move
			for m2 in possible_second_moves:
				moves.append([m, m2])

		# Try val 2 then val 1-----------------------------------------------------
		possible_first_moves = get_possible_moves(board, vals[1], player)

		for m in possible_first_moves:
			# Get the new board state
			tmp_board = np.copy(board)
			tmp_board = update_board(tmp_board, m[0], m[1])
			possible_second_moves = get_possible_moves(tmp_board, vals[0], player)

			# Keep track of each of the second state moves
			if (len(possible_second_moves) == 0): moves.append([m]) # in case no second move
			for m2 in possible_second_moves:
				moves.append([m, m2])

	# Else, is doubles
	else:
		for m in get_possible_moves(board, vals[0], player):
			tb1 = update_board(np.copy(board), m[0], m[1])
			second_moves = get_possible_moves(tb1, vals[1], player)
			if (len(second_moves) == 0): moves.append([m])

			for m2 in second_moves:
				tb2 = update_board(np.copy(tb1), m2[0], m2[1])
				third_moves = get_possible_moves(np.copy(tb2), vals[2], player)
				if (len(third_moves) == 0): moves.append([m, m2])

				for m3 in third_moves:
					tb3 = update_board(np.copy(tb2), m3[0], m3[1])
					fourth_moves = get_possible_moves(np.copy(tb3), vals[3], player)
					if (len(fourth_moves) == 0): moves.append([m, m2, m3])

					for m4 in fourth_moves:
						moves.append([m, m2, m3, m4])

	return moves


def update_by_moves(board, moves):
	"""
	Takes in a board an a list of moves, and returns
	the updated version of the board
	"""
	# Copy the board
	board = np.copy(board)

	# For each move, update board
	for m in moves:
		board = update_board(board, m[0], m[1])

	return board

def play_game(p1, p2):
	"""
	Runs through a game with the given players
	Returns the player who won

	At some point, for training, we are going to have to figure out
	if we wnat to keep track of the boards
	that each player saw individually
	"""
	# Initialize a board
	board = init_state()
	board_tracker = [board] # list of boards

	# Initialize players
	# p1 = Player("player 1")
	# p2 = Player("player 2")

	# Roll the first to decide who goes first
	not_same = True
	while not_same:
		vals = roll()
		not_same = True if (len(vals) != 2) else False

	if (vals[0] > vals[1]):
		starting_player = p1
		player = p1
	else:
		starting_player = p2
		player = p2

	# Game loop
	game_over = False
	i = 0
	while not game_over:
		i += 1

		# Get players move
		next_move = player.action(board, vals)

		# Update the board
		board = update_by_moves(board, next_move)
		board_tracker.append(board)

		# Roll the dice
		vals = roll()

		# Switch player
		player = p2 if (player == p1) else p1

		# Check if the game is over
		if (board[26] >= 15. or board[27] <= -15.):
			game_over = True

		if (i >= 10000):
			print("PROBLEM")
			game_over = True

	# Now that the game is over determine the winner
	winner = p1 if (board[26] == 15) else p2
	obj = {'winner': winner, 'turns': i, 'boards':board_tracker,
		'starting_player':starting_player}

	return obj

if __name__ == "__main__":
	p1 = RandomPlayer("player 1")
	p2 = RandomPlayer("player 2")

	N = 500
	turn_tracker = np.zeros(N)
	winner_tracker = [0,0]

	for i in tqdm(range(N), leave=False):
		obj = play_game(p1, p2)
		turn_tracker[i] = obj['turns']
		if (obj['winner'] == p1):
			winner_tracker[0] += 1
		else:
			winner_tracker[1] += 1

	import matplotlib.pyplot as plt

	print("Player 1", winner_tracker[0])
	print("Player 2", winner_tracker[1])

	plt.hist(turn_tracker, bins=40)
	plt.show()
