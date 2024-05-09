"""
referred to connectm's tui.py implementation for inspiration 
on constructing the grid and utilizing colorama
"""
import curses
import colorama
from colorama import Fore
import sys
from typing import Any

from blokus import BlokusBase
from fakes import BlokusStub, BlokusFake

ESC = 27
curses.set_escdelay(25)
ENTER_KEYS = [10, 13]
ARROW_KEYS = [curses.KEY_LEFT, curses.KEY_RIGHT, curses.KEY_UP, curses.KEY_DOWN]

# main function for running tui
def run_tui(user_input: str) -> str:
    # mono and duo versions
    board: BlokusFake
    if user_input == "mono":
        board = BlokusFake(1, 11, {(5, 5)})
    elif user_input == "duo":
        board = BlokusFake(2, 14, {(4, 4), (9, 9)})
        print_board(board)
    # board size - milestone 1
    else:
        board_size = int(user_input)
        board = BlokusStub(2, board_size, {(0, 0), (board_size - 1, board_size - 1)})
        print_board(board)

# printing board (visual display with gui)
def print_board(board: BlokusFake) -> str:
    colorama.init() # to color symbols

    # grid's top edge
    print(Fore.BLACK + "┌───" + ("┬───" * (board.size - 1)) + "┐")

    # sides and inner sections (between spots)
    for x in range(board.size):
        base = Fore.BLACK + "│"
        for y in range(board.size):
            # None: place empty space in it
            if board.grid[x][y] is None:
                base += "   "
            # process per player (1 and 2)
            else:
                player = board.grid[x][y][0]
                piece = board.grid[x][y][1]
                if player == 1:
                    if piece is not None:
                        base += Fore.BLUE + "███"
                    else:
                        base += "   "
                elif player == 2:
                    if piece is not None:
                        base += Fore.RED + "███"
                    else:
                        base += "   "
            base += Fore.BLACK + "│"
        print(base)

        # middle sections or bottom edge
        if x < board.size - 1:
            print(Fore.BLACK + "├───" + ("┼───" * (board.size - 1)) + "┤")
        else:
            print(Fore.BLACK + "└───" + ("┴───" * (board.size - 1)) + "┘")

    # DISPLAY
    # pending piece AND current player
    print("\n")
    print(f"current player {board.curr_player} has pending piece TODO\n")
    # summary of remaining pieces needed to be played
    print("STATUS SCREEN:\n")
    shapes: list[str] = ["1", "2", "3", "4", "5", "7", "A", "C", "F", "S", "L", "N", "O", "P", "T", "U", "V", "W", "X", "Y", "Z"]
    for i in range (1, board.num_players + 1):
        status_screen: str = f"player {i}: "
        for shape in shapes:
            if shape in board.remaining_shapes(i):
                status_screen += Fore.YELLOW + shape + " "
            else:
                status_screen += Fore.BLACK + shape + " "
        print(f"{status_screen}")

def user_interact(screen: Any) -> None:
    raise NotImplementedError

def play_blokus(blokus: BlokusBase) -> None:
    # game loop: ends when player/players win (all pieces are placed)
    while True:
        # print state of screen
        run_tui(blokus)
        # curses:
        #key_action = screen.getch()

        # If there is a winner, break out of the loop
        if BlokusFake.winners is not None:
            break

if __name__ == "__main__":
    run_tui(sys.argv[1])
