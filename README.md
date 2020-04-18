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

The game board is broken up into four quadrants, each of which has six triangles, called "points," for a total of 24 points. The goal of the game is to move all of your pieces off of the board. Pieces can be *kicked off* the board in certain circumstances and get placed in the center *bar*, which must be included as an extra place. From the perspective of a single player, then, there are 24 points, 1 bar, and 1 end game catchall, making for 26 places where chips can be placed. As we have two players, there are 26 times 2, 52, total places we need to keep track of--as we need a way to distinguish which player has chips on which point, so we must have two identical vectors, one for each player. However, to compress this, we will use a single vector with 28 spaces, and denote player 1 with positive numbers, and player 2 with engatives. 

We will represent the game state as a 56 dimensional vector of integers, which is broken down as follows:

- 0 to 23 represent point chip placement
- 24 and 25 are the bars for player 1 and 2 respectively
- 26 and 27 are the end game spaces for player 1 and 2 respectively

### Rules
Game moves are determined by rolling two dice. The game stats in the position shown in the above image. Each player rolls a single dice, and the one that rolls the higher number starts (the game cannot start when doubles are rolled). Players can move according to their roll to:

- any open point
- any opint that contains chips of their color
- a point that only has one opponent chip

All provided, of course, the numbers rolled allow for it. A chip is sent to the bar if it was first alone on a point, then the opponent lands a chip there. The first move a play *must* make when a chip is at the bar is to remove it. This is done by starting it at the begining of the board. If doubles are rolled, that player gets to play the number rolled *four* times. 

Once all of a player's chips are in the last quadrant, they can start taking them off the board. In this stage, if a player rolls a number higher than the max number of points that the furthest chip can be moved, ther can remove any one. For example, if there are two chips at five, and a five and a six are rolled, both chips can be removed. 

## Data Handlers
As the network plays against itself, we want to keep track of each game state, then if that player ended up winning or losing. For now, we will do that with a csv file (later if this gets too big we will setup a database). 

As a game is being played we will store moves for each player in an array with 28 entries, then, once the game is over, we will go through and for each play record if that board state lead to a win. 

## Network Design and Training
Two networks are initialized, one as player 1 and the other as player 2. They are made to play a large number of games against each other. After every few games (a trainig parameter that can be set) the networks are trained. After each game, all the boards that each player saw are added to trackers, and paired with a vector of 1's or 0's depending on if that player ended up winning or losing the game when they saw that board. The idea is that the model will take in a board state and predict a probability of winnig.

The bots play the game using those win probabilities. When it is their turn they look at the current state and the value of the dice and come up with all possible boards they could have depending on how they move their chips. Each of those possible boards is run through the model to come up with a win probability. The move the yeilds the board with the highest win probability is the one choosen. 

To speed up the training process I will leverage Google Colab. Not that the models are especially big and take a long time to train, but just because I am do so many calculations, and their machines are just generally faster than mine (in testing they can play 4-5 games per second while my computer can only handle 1-2). A notebook specifically for Colab has been made. This handles linking in the GitHub repo and adding it to the path. The only mannual bit will be making sure that the saved model weights are downloaded. 

## Interface
The final step will be to design an interface to actually play against the computer. I think it would be fun to deploy this as a website, so will probably setup a flask server. Stay tuned... 
