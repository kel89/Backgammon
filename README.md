# Backgammon
This project attempts to build a nerural net that can play backgammon. This will be done with adversarial learning, with the network playing games against itself to generate data. To that end, the project will be broken into a few components:
- Play Scripts
- Data handlers
- Network and training
- Interface

## Play Scripts
Before we can being generating data and training the network we need to be able to play the game. To do this we must first come up with a definition for the *game state*, clearly define the rules, come up with a way to find possible moves, and a way to track and update the game state. 

### Game State
![board](