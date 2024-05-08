"""
Bots for Blokus
"""
import sys
import random

from piece import Point, Shape, Piece
from blokus import Blokus
from fakes import BlokusFake

#
# BOTS
#

class NBot:
    """
    Needs Improvement Bot that just picks a move at random.
    """

    def __init__(self, blokus: Blokus, player_num: int):
        """
        Constructor.

        Args:
            blokus: The Blokus board
            player_num: Bot's player number
        """
        self._blokus = blokus
        self._player_num = player_num
    
    def suggest_move(self) -> Piece:
        """
        Suggests a move at random

        Returns: None
        """
        return random.choice(list(board.available_moves()))

class SBot:
    """
    Satisfactory Bot that incorporates simple Blokus-specific heuristics. 
    Will do the following:

    - If possible, block other players' corners
    - Otherwise, place larger pieces over smaller ones
    """

    def __init__(self, blokus: Blokus, player_num: int):
        """
        Constructor.

        Args:
            blokus: The Blokus board
            player_num: Bot's player number
        """
        self._blokus = blokus
        self._player_num = player_num
    
    def suggest_move(self) -> Piece:
        """
        Suggests a move

        Returns: None
        """
        largest_length: int = 0
        largest_piece: Piece = None

        #print("--- AVAIL MOVES:", board.available_moves())

        # --- NEED TO IMPLEMENT ---
        # If possible, block other players' corners

        # Places larger ones over smaller ones

        for piece in board.available_moves():
            if len(piece.squares()) > largest_length:
                largest_piece = piece
                largest_length = len(piece.squares())
        #print("largest piece has length", largest_length)
        return largest_piece

#
# SIMULATION CODE
#

NUM_GAMES: int = int(sys.argv[1])
bot1_wins: int = 0
bot2_wins: int = 0
tie: int = 0

for i in range(NUM_GAMES):
    # Create a Blokus object with two players, board size 11x11 and two start
    # positions in the upper-left (0,0) and bottom-right (10,10) corners
    board = BlokusFake(num_players=2, size=11, start_positions={(0,0), (10,10)})

    bot1 = NBot(board, 1)
    bot2 = SBot(board, 2)

    while not board.game_over:
        if board.curr_player == 1 and len(board.available_moves()) > 0:
            board.maybe_place(bot1.suggest_move())
        elif board.curr_player == 2 and len(board.available_moves()) > 0:
            board.maybe_place(bot2.suggest_move())
        else:
            board.retire()

    if len(board.winners) == 1:
        if 1 in board.winners:
            bot1_wins += 1
        elif 2 in board.winners:
            bot2_wins += 1
    elif len(board.winners) == 2:
        tie += 1

print("Bot 1 Wins |  ", bot1_wins/NUM_GAMES * 100, "%")
print("Bot 2 Wins |  ", bot2_wins/NUM_GAMES * 100, "%")
print("Ties       |  ", tie/NUM_GAMES * 100, "%")
