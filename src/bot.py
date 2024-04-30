from fakes import BlokusStub

# Create a BlokusStub object with two players and board size 14x14
test = BlokusStub(2, 14, ((4,4), (9,9)))

# Keep track of the fact that there are two bots playing. 
# Both follow the same strategy: picking a location at random from the board. 
# Make sure to use the available_moves method


# Each bot will make moves until game is over (according to game_over method). 
# A bot retires only if available_moves says there are no available moves left


# Repeat the above NUM_GAMES times, keeping track of wins and ties.

# After playing all the games, print a summary like this:
"""
python3 src/bot.py 1000
Bot 0 Wins |  1.90 %
Bot 1 Wins |  1.30 %
Ties       | 96.80 %
"""


