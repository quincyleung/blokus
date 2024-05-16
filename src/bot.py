"""
Bots for Blokus
"""
import random
import click

from piece import Piece
from blokus import Blokus

#
# BOTS
#

class NBot:
    """
    Needs Improvement Bot that just picks a move at random.
    """

    _board: Blokus
    _player_num: int

    def __init__(self, blokus: Blokus, player_num: int):
        """
        Constructor.

        Args:
            blokus: The Blokus board
            player_num: Bot's player number
        """
        self._board = blokus
        self._player_num = player_num
    
    def suggest_move(self) -> Piece:
        """
        Suggests a move at random

        Returns: None
        """
        return random.choice(list(self._board.available_moves()))

class SBot:
    """
    Satisfactory Bot that incorporates simple Blokus-specific heuristics. 
    
    Will do the following:
    - Place larger pieces over smaller ones
    """

    _board: Blokus
    _player_num: int

    def __init__(self, blokus: Blokus, player_num: int):
        """
        Constructor.

        Args:
            blokus: The Blokus board
            player_num: Bot's player number
        """
        self._board = blokus
        self._player_num = player_num
    
    def suggest_move(self) -> Piece:
        """
        Suggests a move

        Returns: None
        """
        largest_length: int = 0
        largest_piece: Piece = None

        # Places larger ones over smaller ones
        for piece in self._board.available_moves():
            if len(piece.squares()) > largest_length:
                largest_piece = piece
                largest_length = len(piece.squares())
        return largest_piece

class UBot:
    """
    Unsatisfactory Bot that incorporates Blokus-specific heuristics
    to perform worse than the Needs Improvement Bot.
    
    Will do the following:
    - Place smaller pieces over larger ones
    """

    _board: Blokus
    _player_num: int

    def __init__(self, blokus: Blokus, player_num: int):
        """
        Constructor.

        Args:
            blokus: The Blokus board
            player_num: Bot's player number
        """
        self._board = blokus
        self._player_num = player_num
    
    def suggest_move(self) -> Piece:
        """
        Suggests a move

        Returns: None
        """
        smallest_length: int = 10
        smallest_piece: Piece = None

        # Places smaller ones over larger ones
        for piece in self._board.available_moves():
            if len(piece.squares()) < smallest_length:
                smallest_piece = piece
                smallest_length = len(piece.squares())
        return smallest_piece

#
# SIMULATION CODE
#

@click.command()
@click.option('-n', '--num-games', default=20, help='Number of games')
@click.option('-1', '--player1', default='N', help='Strategy played by the first player')
@click.option('-2', '--player2', default='N', help='Strategy played by the second player')

def main(num_games, player1, player2) -> None:
    NUM_GAMES: int = num_games #int(sys.argv[1])
    bot1_wins: int = 0
    bot2_wins: int = 0
    tie: int = 0
    for i in range(NUM_GAMES):
        # Create a Blokus object with two players, board size 11x11 and two 
        # start positions in upper-left (0,0) and bottom-right (10,10) corners
        board = Blokus(num_players=2, size=11, start_positions={(0,0), (10,10)})

        bot_type: dict[str, 'SBot'|'NBot'|'UBot'] = {'S':SBot,'N':NBot,'U':UBot}
        bot1 = bot_type.get(player1, SBot)(board, 1)
        bot2 = bot_type.get(player2, SBot)(board, 2)

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
                print("Game", i, "bot 1 wins!")
            elif 2 in board.winners:
                bot2_wins += 1
                print("Game", i, "bot 2 wins!")
        elif len(board.winners) == 2:
            tie += 1
            print("Game", i, "tie!")
    print("Bot 1 (", player1,") Wins |  ", bot1_wins/NUM_GAMES * 100, "%")
    print("Bot 2 (", player2,") Wins |  ", bot2_wins/NUM_GAMES * 100, "%")
    print("Ties             |  ", tie/NUM_GAMES * 100, "%")

if __name__ == '__main__':
    main()

