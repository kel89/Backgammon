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

We will represent the game state as a 56 dimensional vector of integers, which is broken down as follows:

- 0 to 23 represent player ones point chip placement
- 24 is player ones bar
- 25 is player ones end game/off board state
- 26 to 53 is player twos point chip placement
- 54 is player twos bar
- 55 is player twos end game/off board state

### Rules
Game moves are determined by rolling two dice. The game stats in the position shown in the above image. Each player rolls a single dice, and the one that rolls the higher number starts (the game cannot start when doubles are rolled). Players can move according to their roll to:

- any open point
- any opint that contains chips of their color
- a point that only has one opponent chip

All provided, of course, the numbers rolled allow for it. A chip is sent to the bar if it was first alone on a point, then the opponent lands a chip there. The first move a play *must* make when a chip is at the bar is to remove it. This is done by starting it at the begining of the board. If doubles are rolled, that player gets to play the number rolled *four* times. 

Once all of a player's chips are in the last quadrant, they can start taking them off the board. In this stage, if a player rolls a number higher than the max number of points that the furthest chip can be moved, ther can remove any one. For example, if there are two chips at five, and a five and a six are rolled, both chips can be removed. 

## Data Handlers
As the network plays against itself, we want to keep track of each game state, then if that player ended up winning or losing. For now, we will do that with a csv file (later if this gets too big we will setup a database). 

As a game is being played we will store moves for each player in an array with 56 entries, then, once the game is over, we will go through and for each play record if that board state lead to a win. 

## Network Design and Training
At a highlevel, we will have a network that takes in the game state and predicts the probability of winning given that state. TO train the network will play against itself to generate date. At each step, all the available moves will be run through the existing model, and the argmax will be used to decide on the next move. After each game (or maybe after a few) the model will be retrainied. 

I am not yet sure about network arcitecture, but I am thinking of a basic dense net with a few layers--the final layer will use...., and some dropout. 

## Interface
The final step will be to design an interface to actually play against the computer. I think it would be fun to deploy this as a website, so will probably setup a flask server. 