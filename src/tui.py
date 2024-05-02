import sys
from typing import Optional
import bot

import click
from colorama import Fore, Style

from blokus import BlokusBase, Blokus, ShapeKind
from fakes import BlokusStub, BlokusFake
from piece import Shape, Piece
import base

system: BlokusStub
grid: list[list[Optional[tuple[int, ShapeKind]]]]

# printing board (visual display with gui)
def print_board(system: BlokusStub):
    
    row = len(grid)
    col = len(grid[0])

    # grid's top edge
    print(Fore.BLACK + "┌" + ("─┬" * (col - 1)) + "─┐")

    # sides and inner sections (between spots)
    for r in range(row):
        base = "│"
        for c in range(col):

            player = grid[r][c][0]
            piece = grid[r][c][1]
            # None: place empty space in it
            if grid[r][c] is None:
                base += " "
            # process per player (1 and 2)
            elif player == 1:
                for section in piece:

                    base += Fore.BLUE + Style.BRIGHT + "█"
            elif player == 2:
                base += Fore.RED + Style.BRIGHT + "█"
            base += Fore.BLUE + Style.NORMAL + "│"
        print(base)

        # middle sections or bottom edge
        if r < row - 1:
            print(Fore.BLUE + "├" + ("─┼" * (col - 1)) + "─┤")
        else:
            print(Fore.BLUE + "└" + ("─┴" * (col - 1)) + "─┘" + Style.RESET_ALL)

# some features to implement moving forward:
# settings for each player - to implement later
class TUIPlayer:

    name: str
    blokus: BlokusBase
    color: str
    # to add: bot

    def __init__(self, number: int, player_type: str, color: str):
        # setting player
        if player_type == "human":
            self.name = f"Player {number}"
        elif player_type == "bot":
            self.name = f"Bot {number}"
        # setting color to differentiate between players
        self.color = color
        # TODO: more attributes
    
    #TODO: functional methods for TUIPlayer

# initiate playing the game
def play_blokus(blokus: BlokusBase) -> None:
    current = blokus.COLOR

    # game loop: ends when player/players win (all pieces are placed)
    # U+258x: 8  full box character
    while True:
        # print() ?
        print(blokus)
        # TODO: game process

        # If there is a winner, break out of the loop
        if BlokusFake.winners is not None:
            break

        # TODO: Update the player - switch between the different players

if __name__ == "__main__":
    #play_blokus(game)
    NotImplementedError