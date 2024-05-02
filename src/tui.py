"""
referred to connectm's tui.py implementation for inspiration
"""
import colorama
from colorama import Fore, Style

from blokus import BlokusBase, Blokus, ShapeKind
from fakes import BlokusStub, BlokusFake

grid: BlokusStub
# grid: list[list[Optional[tuple[int, ShapeKind]]]]

# printing board (visual display with gui)
def print_board(grid: BlokusStub):
    colorama.init() # to color symbols

    # grid's top edge
    print(Fore.BLACK + "┎" + ("┮" * (grid.size - 1)) + "┑")
    # sides and inner sections (between spots)
    for x in range(grid.size):
        base = Fore.BLACK + "│"
        for y in range(grid.size):
            player = grid[x][y][0]
            piece = grid[x][y][1]
            # None: place empty space in it
            if grid[x][y] is None:
                base += " "
            # process per player (1 and 2)
            elif player == 1:
                base += " "
                for section in piece:
                    base[x + section[0], y + section[1]] = Fore.BLUE + "█"
            elif player == 2:
                base += " "
                for section in piece:
                    base[x + section[0], y + section[1]] = Fore.RED + "█"
            base += Fore.BLACK + "│"
        print(base)

        # middle sections or bottom edge
        if x < grid.size - 1: # not at end yet
            print(Fore.BLACK + "┡" + ("╁" * (grid.size - 1)) + "┥")
        else: # at end (x == row)
            print(Fore.BLACK + "┕" + ("┵" * (grid.size - 1)) + "┙") # symbols are too thin?

# Future tasks
def play_blokus(blokus: BlokusBase) -> None:
    # game loop: ends when player/players win (all pieces are placed)
    while True:
        print(blokus)
        # TODO: game process
        # If there is a winner, break out of the loop
        if BlokusFake.winners is not None:
            break
        # TODO: Update the player - switch between the different players

if __name__ == "__main__":
    #play_blokus()
    #game = 
    #print_board(game)
    raise NotImplementedError
