# Backgammon
This project attempts to build a nerural net that can play backgammon. This will be done with adversarial learning, with the network playing games against itself to generate data. To that end, the project will be broken into a few components:

- Play Scripts
- Data handlers
- Network and training
- Interface

## Play Scripts
Before we can being generating data and training the network we need to be able to play the game. To do this we must first come up with a definition for the *game state*, clearly define the rules, come up with a way to find possible moves, and a way to track and update the game state. 

### Game State
![board](/images/board_setup.jpg)
The game board is broken up into four quadrants, each of which has six triangles, called "points," for a total of 24 points. The goal of the game is to move all of your pieces off of the board. Pieces can be *kicked off* the board in certain circumstances and get placed in the center *bar*, which must be included as an extra place. From the perspective of a single player, then, there are 24 points, 1 bar, and 1 end game catchall, making for 26 places where chips can be placed. As we have two players, there are 26 times 2, 52, total places we need to keep track of--as we need a way to distinguish which player has chips on which point, so we must have two identical vectors, one for each player. 

We will represent the game state as a vector in $\mathbb{Z}^_+^{56}$, which is broken down as follows:

- 0 to 23 represent player ones point chip placement
- 24 is player ones bar
- 25 is player ones end game/off board state
- 26 to 53 is player twos point chip placement
- 54 is player twos bar
- 55 is player twos end game/off board state

### Rules

