# Player.py

"""
Class for a random player
"""

import numpy as np
import random

from backgammon import *

class RandomPlayer(object):
	def __init__(self, which):
		# player 1 or player 2
		self.which = which

	def __str__(self):
		return self.which

	def __repr__(self):
		return self.which

	def action(self, board, vals):
		"""
		Takes in the board state and the value of the
		dice rolled, and returns the desired move
		"""
		# get all the moves
		all_moves = get_all_moves(board, vals, self.which)

		# Randomly pick one
		if (len(all_moves) == 0):
			move = []
		else:
			move = random.choice(all_moves)

		return move
