"""
referred to connectm's tui.py implementation for inspiration 
on constructing the grid and utilizing colorama
"""
import random
import curses
import colorama
from colorama import Fore
import sys
from typing import Any

from blokus import BlokusBase, Shape, Piece
from fakes import BlokusStub, BlokusFake
from shape_definitions import ShapeKind, definitions

ESC = 27
curses.set_escdelay(25)
ENTER_KEYS = [10, 13]
ARROW_KEYS = [curses.KEY_LEFT, curses.KEY_RIGHT, curses.KEY_UP, curses.KEY_DOWN]

# main function for running tui
def run_tui(user_input: str) -> str:
    # mono and duo versions
    board: BlokusFake | BlokusStub
    if user_input == "mono":
        board = BlokusFake(1, 11, {(5, 5)})
    elif user_input == "duo":
        board = BlokusFake(2, 14, {(4, 4), (9, 9)})
        print_board(board)
    # board size - milestone 1: I used Stub here just for now to show I've completed this stage with the pieces
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

def play_blokus() -> None:
    curses.wrapper(_play_blokus)

# 
def _play_blokus(blokus: BlokusBase | BlokusFake, screen: Any) -> None:
    # game loop: ends when player/players win (all pieces are placed)
    while True:
        # state of screen - q: print every move?
        run_tui(blokus)

        # choose random remaining piece from remaining pieces
        random_piece: ShapeKind = random.choice(blokus.remaining_shapes(blokus.curr_player))
        cur_piece: Piece = Piece(blokus.shapes[random_piece])
        cur_piece.set_anchor((blokus.size / 2, blokus.size / 2))
       
        # USER CONTROL
        key = screen.getch()
        # if ESC pressed, simply exit
        if key == ESC or BlokusFake.winners is not None:
            break

        # move the piece
        elif key in ARROW_KEYS:
            x, y = cur_piece.anchor
            if key == curses.KEY_LEFT and not blokus.any_wall_collisions(cur_piece):
                cur_piece.set_anchor(x, y - 1)
            elif key == curses.KEY_RIGHT and not blokus.any_wall_collisions(cur_piece):
                cur_piece.set_anchor(x, y + 1)
            elif key == curses.KEY_UP and not blokus.any_wall_collisions(cur_piece):
                cur_piece.set_anchor(x - 1, y)
            elif key == curses.KEY_DOWN and not blokus.any_wall_collisions(cur_piece): 
                cur_piece.set_anchor(x + 1, y)
        
        # decide the piece location
        elif key in ENTER_KEYS:
            blokus.maybe_place(cur_piece)

        # change player
        if blokus.curr_player == 1:
            blokus.curr_player = 2
        else:
            blokus.curr_player = 1
        
        # if someone has won
        if blokus.winners is not None:
            report: str = "Winners are "
            for player in blokus.winners:
                report += f"player {player} "
            break

if __name__ == "__main__":
    #run_tui(sys.argv[1])
    _play_blokus(sys.argv[1], None)
