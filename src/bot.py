import sys
import random
from fakes import BlokusStub

NUM_GAMES: int = int(sys.argv[1])
bot0_wins: int = 0
bot1_wins: int = 0
tie: int = 0

for i in range(NUM_GAMES):
    # Create a BlokusStub object with two players and board size 14x14
    test = BlokusStub(2, 14, {(4,4), (9,9)})

    while not test.game_over:
        if len(test.available_moves()) > 0:
            # Picking a location at random
            next_piece = random.choice(list(test.available_moves()))
            if test.legal_to_place(next_piece):
                test.maybe_place(next_piece)
        else:
            test.retire()

    if len(test.winners) == 1:
        if 1 in test.winners:
            bot0_wins += 1
        elif 2 in test.winners:
            bot1_wins += 1
    elif len(test.winners) == 2:
        tie += 1

print("Bot 0 Wins |  ", bot0_wins/NUM_GAMES * 100, "%")
print("Bot 1 Wins |  ", bot1_wins/NUM_GAMES * 100, "%")
print("Ties       | ", tie/NUM_GAMES * 100, "%")
