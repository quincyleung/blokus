import sys, random
from fakes import BlokusStub
from piece import Point, Shape, Piece

# Create a BlokusStub object with two players and board size 14x14
test = BlokusStub(2, 14, {(4,4), (9,9)})
NUM_GAMES = int(sys.argv[1])

# Keep track of the fact that there are two bots playing. 
# Both follow the same strategy: picking a location at random from the board.
bot0_wins = 0
bot1_wins = 0
tie = 0

for i in range(NUM_GAMES):
    # Each bot will make moves until game is over. A bot retires only if available_moves says there are no available moves left
    while not test.game_over:        
        if len(test.available_moves()) > 0:
            print("available moves:", test.available_moves(), "len", len(test.available_moves()))
            next_piece = random.choice(list(test.available_moves()))
            print("next piece:", next_piece)
            if test.legal_to_place(next_piece):
                test.maybe_place(next_piece)
                print("placed ", next_piece)
        else:
            test.retire

    print("winner:", test.winners)
    if len(test.winners) == 1:
        if 1 in test.winners:
            bot0_wins += 1
        elif 2 in test.winners:
            bot1_wins += 1
    elif len(test.winners) == 2:
        tie += 1

print("Bot 0 Wins |  ", bot0_wins, bot0_wins/NUM_GAMES * 100, "%")
print("Bot 1 Wins |  ", bot1_wins, bot1_wins/NUM_GAMES * 100, "%")
print("Ties       | ", tie, tie/NUM_GAMES * 100, "%")

# After playing all the games, print a summary like this:
"""
python3 src/bot.py 1000
Bot 0 Wins |  1.90 %
Bot 1 Wins |  1.30 %
Ties       | 96.80 %
"""


