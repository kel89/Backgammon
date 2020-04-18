
import tensorflow as tf
import numpy as np
from backgammon import *
from tensorflow.keras.layers import Input, Dense, Dropout


class PlayerANN():
	def __init__(self, which):
		self.which = which
		self.setupNetwork()

	def setupNetwork(self):
		"""
		Sets up the keras NN
		"""
		in_layer = Input(shape=(28, ))
		d1 = Dense(40, activation='relu')(in_layer)
		d2 = Dense(10, activation='relu')(d1)
		out = Dense(1, activation='sigmoid')(d2)

		self.model = tf.keras.Model(inputs=in_layer, outputs=out)

	def action(self, board, vals):
		"""
		Takes in the current board state and
		the value of the dice
		Returns the moves this player would like to make
		First, determiens all possible moves and the boards
		that would accompany them, then it runs all boards
		through the model and takes the move that yields
		the board with the highest probability of winning
		"""
		# Get all the moves
		all_moves = get_all_moves(board, vals, self.which)

		if (len(all_moves) == 0):
			return []

		# Get all the boards for those moves
		board = np.copy(board)
		boards = np.zeros([len(all_moves), 28])
		i = 0
		for move in all_moves:
			boards[i] = update_by_moves(board, move)

		# Get the predicted probabilities for each board
		probs = self.model(boards)

		# Take the move with argmax board probs
		best_move = all_moves[np.argmax(probs)]

		return best_move

	def update_model(self, boards, outcomes, verbose=0):
		"""
		Training step for the model, takes in the boards to be trained on
		and a vector of the outcomes associated with that board
		"""
		# Compile the model
		self.model.compile(
			optimizer='adam',
			loss='mse'
		)

		# Train the model
		mf = self.model.fit(boards, outcomes, verbose=verbose)

		# Crush the graph, maybe that is what is messing with RAM?
		tf.keras.backend.clear_session()

	def save_model(self, file_name):
		"""
		Saves the model weights tensorflow style
		to the given file_name
		"""
		self.model.save_weights(file_name)

	def load_model(self, file_name):
		"""
		Loads model weights tensorflow style
		from the given file_name
		"""
		self.model.load_weights(file_name)
