import sys, random
from fakes import BlokusStub
from piece import Point, Shape, Piece

# Create a BlokusStub object with two players and board size 14x14
test = BlokusStub(2, 14, ((4,4), (9,9)))

# Keep track of the fact that there are two bots playing. 
# Both follow the same strategy: picking a location at random from the board. 
# Make sure to use the available_moves method

next_piece = test.available_moves().pop()
if test.legal_to_place(next_piece):
    test.maybe_place(next_piece)

# Each bot will make moves until game is over (according to game_over method). 
# A bot retires only if available_moves says there are no available moves left


# Repeat the above NUM_GAMES times, keeping track of wins and ties.
NUM_GAMES = sys.argv[1]
print("Num games:", NUM_GAMES)

# After playing all the games, print a summary like this:
"""
python3 src/bot.py 1000
Bot 0 Wins |  1.90 %
Bot 1 Wins |  1.30 %
Ties       | 96.80 %
"""


