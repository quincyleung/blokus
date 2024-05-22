"""
referred to connectm's tui.py implementation for inspiration 
on constructing the grid and utilizing colorama
"""
import click
import curses
import random
import sys
from typing import Any

from blokus import Piece, Blokus
from shape_definitions import ShapeKind

# constants for command line interface keys
ESC = 27
curses.set_escdelay(25)
ENTER_KEYS = [10, 13]
ARROW_KEYS = [curses.KEY_LEFT, curses.KEY_RIGHT, curses.KEY_UP, curses.KEY_DOWN]
ORIENT_KEYS = [101, 114, 32] # left, right, flip
RETIRE = 113

blokus: None | Blokus
num_players: int
size: int
screen: Any
players_list: list[int]
size: int
start_position: set

class TUI:
    """
    Class for TUI simulation of blokus
    """
    def __init__(self, screen: Any,
                 num_players: int,
                 size: int,
                 start_position: set[tuple],
                 game_mode: None | str) -> None:
        """
        Constructor for TUI class
        """
        # self.blokus = blokus
        self.screen = screen
        self.blokus = None
        self.num_players = int(num_players)
        self.size = int(size)
        # list of players-block colors referenced to curses colors list, initialized below
        self.players_list = []
        for i in range(num_players):
            self.players_list.append(i + 1)
        
        # initialize Blokus object for given round of TUI, based on user input
        if game_mode == "mono":
            self.blokus = Blokus(1, 11, {5, 5})
        elif game_mode == "duo":
            self.blokus = Blokus(2, 14, {(4, 4), (9, 9)})
        elif game_mode == "classic-2":
            self.blokus = Blokus(2, 20, {(0,0), (0,19), (19,0), (19,19)})
        elif game_mode == "classic-3":
            self.blokus = Blokus(3, 20, {(0,0), (0,19), (19,0), (19,19)})
        elif game_mode == "classic-4":
            self.blokus = Blokus(4, 20, {(0,0), (0,19), (19,0), (19,19)})
        else:
            self.blokus = Blokus(num_players, size, start_position)

        # initialize colors from curses
        curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK) # player 1
        curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_BLACK) # player 2
        curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK) # player 3
        curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK) # player 4
        curses.init_pair(5, curses.COLOR_CYAN, curses.COLOR_BLACK) # current player
        curses.init_pair(6, curses.COLOR_MAGENTA, curses.COLOR_BLACK) # pieces needed to be played
        curses.init_pair(7, curses.COLOR_BLACK, curses.COLOR_BLACK) # already-played pieces


    def print_board(self, cur_piece: Piece) -> str:
        """
        Print the blokus board's status visually onto the terminal

        Input:
            cur_piece: current player's currently hovering piece

        Returns: string-type visualization of the blokus board
        """
        self._print("┌───" + ("┬───" * (self.blokus.size - 1)) + "┐" + "\n", 0)
        #self._print("\n", 0)

        # sides and inner sections (between spots)
        for x in range(self.blokus.size):
            self._print("│", 0)
            for y in range(self.blokus.size):
                # hovering piece
                state: bool = False
                for loc in cur_piece.shape.squares:
                    x1, y1 = loc
                    x2, y2 = cur_piece.anchor
                    if (x, y) == (x1 + x2, y1 + y2):
                        self._print("███", 5)
                        state = True
                if state:
                    break        
                # blank or already-placed piece on the board
                if self.blokus.grid[x][y] is None:
                    self._print("   ", 0)
                else:
                    player = self.blokus.grid[x][y][0]
                    piece = self.blokus.grid[x][y][1]
                    if piece is not None:
                        self._print("███", player)
                    else:
                        self._print("   ", 0)
                self._print("│", 0)
            self._print("\n", 0)

            # middle sections or bottom edge
            if x < self.blokus.size - 1:
                self._print("├───" + ("┼───" * (self.blokus.size - 1)) + "┤" + "\n", 0)
            else:
                self._print("└───" + ("┴───" * (self.blokus.size - 1)) + "┘"+ "\n", 0)

        self._print("\n", 0)
        
    def print_display(self) -> str:
        """
        Print display for the blokus game by tracking pending piece and current player

        Input: 
            None

        Returns [str]: display of blokus board's current state
        """
        self._print(f"layer {self.blokus.curr_player} is currently making a move\n", 0)
        # summary of remaining pieces needed to be played
        self._print("STATUS SCREEN:\n", 0)
        shapes : list[str] = ["1", "2", "3", "4", "5", "7", "A", "C", "F", "S", "L", "N", "O", "P", "T", "U", "V", "W", "X", "Y", "Z"]
        # supports any given number of players
        for player in range (1, self.blokus.num_players + 1):
            if self.blokus.curr_player is player:
                self._print(f"player {player}: ", 5)
            else:
                self._print(f"player {player}: ", 0)
            for shape in shapes:
                if shape in self.blokus.remaining_shapes(player):
                    self._print(shape + " ", 1)
            self._print("\n", 0)
            # print player's score
            self._print(f"Player's score: {self.blokus.get_score(player)}", 0)
            self._print("\n", 0)

    def _print(self, string: str, color: int) -> str:
        """
        Applies print and color using addstr() to show text on the Terminal screen

        Inputs:
            string [str]: string to print
            color [int]: color to apply

        Returns [str]: terminal string
        """
        self.screen.addstr(string, curses.color_pair(color)) # in specific color?
    
    def user_interaction(self, screen: Any) -> None:
        """
        runs the full game logic loop of a blokus match

        Inputs:
            screen: Any
        
        Returns [None]: updates the terminal with the game until it ends
        """
        while True: # game runs until someone wins
            screen.clear()
            
            random_piece: ShapeKind = random.choice(self.blokus.remaining_shapes(self.blokus.curr_player))
            cur_piece: Piece = Piece(self.blokus.shapes[random_piece])
            cur_piece.set_anchor((self.blokus.size / 2, self.blokus.size / 2))

            self.print_board(cur_piece)
            self.print_display()
            key = screen.getch()

            if key == ESC or self.blokus.winners is not None: # if ESC pressed, exit terminal
                # screen.getch() <-- need this or not?
                break

            while True: # until player places piece (break in ENTER)
            # move the piece
                if key in ARROW_KEYS:
                    x, y = cur_piece.anchor
                    # move left
                    if key == curses.KEY_LEFT and not self.blokus.any_wall_collisions(cur_piece):
                        cur_piece.set_anchor(x, y - 1)
                    # move right
                    elif key == curses.KEY_RIGHT and not self.blokus.any_wall_collisions(cur_piece):
                        cur_piece.set_anchor(x, y + 1)
                    # move up
                    elif key == curses.KEY_UP and not self.blokus.any_wall_collisions(cur_piece):
                        cur_piece.set_anchor(x - 1, y)
                    # move down
                    elif key == curses.KEY_DOWN and not self.blokus.any_wall_collisions(cur_piece): 
                        cur_piece.set_anchor(x + 1, y)
                    self._print(f"Arrow key: {key}", 0)
                elif key in ORIENT_KEYS:
                    temp: Piece = Piece(cur_piece.shape)
                    temp.set_anchor(cur_piece.anchor)
                    # rotate left
                    if key == 101:
                        temp.rotate_left()
                        if not self.blokus.any_wall_collisions(temp):
                            cur_piece.rotate_left()
                            self._print(f"Piece {cur_piece} has been rotated left", 0)
                    # rotate right
                    elif key == 114:
                        temp.rotate_right()
                        if not self.blokus.any_wall_collisions(temp):
                            cur_piece.rotate_right()
                            self._print(f"Piece {cur_piece} has been rotated right", 0)
                    # flip horizontally
                    else:
                        temp.flip_horizontally()
                        if not self.blokus.any_wall_collisions(temp):
                            cur_piece.flip_horizontally()
                            self._print(f"Piece {cur_piece} has been flipped horizontally", 0)
                elif key in ENTER_KEYS:
                    self.blokus.maybe_place(cur_piece)
                    break

                self.print_board(cur_piece)
                self.print_display()
                key = screen.getch()
                screen.refresh()

            # a player retires
            if key in RETIRE:
                    self._print(f"player {self.blokus.curr_player} has retired", 0)
                    self.blokus.retire()
            
            # change player turn
            if self.blokus.curr_player == len(self.players_list):
                self.blokus.set_curr_player(1)
            else:
                self.blokus.set_curr_player(self.blokus.curr_player + 1)
            
            # if someone has won
            if self.blokus.winners is not None:
                report: str = "Winners are "
                for player in self.blokus.winners:
                    report += f"player {player} "
                self._print(report, 5)
                break
            
            screen.refresh()

# COMMAND LINE INTERFACE (Click) - defaulted to duo set-up
@click.command(name = "blokus-tui")
@click.option("-n", "--num_players", default = 2)
@click.option("-s", "--size", default = 14)
@click.option("-p", "--start-position", nargs = 2, multiple = True, default = (("4", "4"), ("9", "9")))
@click.option("--game", default = None)

def run_tui(num_players, size, start_position, game) -> None:
    set_of_positions: set = set()
    for position in start_position:
        x, y = position
        set_of_positions.add((int(x), int(y)))
    
    def curses_main(screen: Any) -> None:
        tui = TUI(screen, num_players, size, set_of_positions, game)
        tui.user_interaction(screen)
    
    curses.wrapper(curses_main)

def main() -> None:
    run_tui()

if __name__ == "__main__":
    main()