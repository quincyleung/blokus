"""
referred to connectm's tui.py implementation for inspiration 
on constructing the grid and utilizing colorama
"""
import colorama
from colorama import Fore
import sys

from blokus import BlokusBase, Blokus, ShapeKind
from fakes import BlokusStub, BlokusFake

# milestone 1 to 2 change: board input is BlokusFake instead of BlokusStub
board: BlokusFake
SIZE = int(sys.argv[1])

# printing board (visual display with gui)
def print_board(board: BlokusFake):
    colorama.init() # to color symbols

    # grid's top edge
    print(Fore.BLACK + "┌──" + ("┬──" * (board.size - 1)) + "┐")

    # sides and inner sections (between spots)
    for x in range(board.size):
        base = Fore.BLACK + "│"
        for y in range(board.size):
            # None: place empty space in it
            if board.grid[x][y] is None:
                base += "  "
            # process per player (1 and 2)
            else:
                player = board.grid[x][y][0]
                piece = board.grid[x][y][1]
                if player == 1:
                    if piece is not None:
                        base += Fore.BLUE + "██"
                    else:
                        base += "  "
                elif player == 2:
                    if piece is not None:
                        base += Fore.RED + "██"
                    else:
                        base += "  "
            base += Fore.BLACK + "│"
        print(base)

        # middle sections or bottom edge
        if x < board.size - 1: # not at end yet
            print(Fore.BLACK + "├──" + ("┼──" * (board.size - 1)) + "┤")
        else: # at end (x == row)
            print(Fore.BLACK + "└──" + ("┴──" * (board.size - 1)) + "┘") # symbols are too short?

def play_blokus(blokus: BlokusBase) -> None:
    # game loop: ends when player/players win (all pieces are placed)
    while True:
        print(blokus)
        # If there is a winner, break out of the loop
        if BlokusFake.winners is not None:
            break

if __name__ == "__main__":
    board_size = SIZE
    board: BlokusFake = BlokusFake(2, board_size, {(0, 0), (board_size - 1, board_size - 1)})
    print_board(board)
