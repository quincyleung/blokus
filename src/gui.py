

"""
CMSC 14200, Spring 2024
Homework #3

People Consulted:
   List anyone (other than the course staff) that you consulted about
   this assignment.

Online resources consulted:
   List the URLs of any online resources other than the course text and
   the official Python language documentation that you used to complete
   this assignment.
"""
import os
import sys
import random
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
from fakes import BlokusStub, BlokusFake
from piece import Point, Shape, Piece
from shape_definitions import definitions, ShapeKind
from blokus import Blokus
import click

key_to_shape = {
    '1': ShapeKind.ONE,
    '2': ShapeKind.TWO,
    '3': ShapeKind.THREE,
    '4': ShapeKind.FOUR,
    '5': ShapeKind.FIVE,
    '7': ShapeKind.SEVEN,
    'a': ShapeKind.A,
    'c': ShapeKind.C,
    'f': ShapeKind.F,
    's': ShapeKind.S,
    'l': ShapeKind.L,
    'n': ShapeKind.N,
    'o': ShapeKind.LETTER_O,
    'p': ShapeKind.P,
    't': ShapeKind.T,
    'u': ShapeKind.U,
    'v': ShapeKind.V,
    'w': ShapeKind.W,
    'x': ShapeKind.X,
    'y': ShapeKind.Y,
    'z': ShapeKind.Z,
}

@click.command()
@click.option('-n', '--num-players', default=2, type=int, help='Number of players.')
@click.option('-s', '--size', default=14, type=int, help='Board size.')
@click.option('-p', '--start-position', nargs=2, type=int, multiple=True, help='Start position.')
@click.option('--game', type=click.Choice(['mono', 'duo', 'classic-2', 'classic-3', 'classic-4']), help='Game configuration.')

def main(num_players: int, size: int, start_position: set[int], game: str):
    """
    num_players: number of players
    start_positions: set of starting positions
    game: string form of game style
    """
    if game == 'mono':
        num_players = 1
        size = 11
        start_position = {(5, 5)}
    elif game == 'duo':
        num_players = 2
        size = 14
        start_position = {(4, 4), (9, 9)}
    elif game == 'classic-2':
        num_players = 2
        start_position = {(0, 0), (0, size - 1), (size - 1, 0), (size - 1, size - 1)}
    elif game == 'classic-3':
        num_players = 3
        start_position = {(0, 0), (0, size - 1), (size - 1, 0), (size - 1, size - 1)}
    elif game == 'classic-4':
        num_players = 4
        start_position = {(0, 0), (0, size - 1), (size - 1, 0), (size - 1, size - 1)}

    gui = GUI(size, num_players, start_position)
    gui.event_loop()

class GUI:
    """
    Class for a GUI-based game
    """
    width:   int
    height:  int
    border:  int
    number:  int
    buttons: dict[str, tuple[int, int]]
    most_recent: str
    square_size: int
    spacer: int
    duration: int
    font_size: int
    width: int
    height: int
    display_nums: str
    most_recent_timer: str

    def __init__(self, board_size: int, num_player: int, start_positions: set[tuple[int, int]]) -> None:
        """
        constructor for GUI object

        board_size: size of the board
        num_player: number of players
        start_positions: starting positions

        sets up all ncessary variables for use
        Adjusts square_size so the area of the board is always the same regardless of how many squares in the board
        """

        if len(start_positions) == 0:
            start_positions = {(4, 4), (9, 9)}
        self.blokusS = Blokus(num_player, board_size, start_positions)
        self.font_size = 30
        self.spacer = 7
        self.grid_top_separation = 32
        self.grid_left_separation =32
        self.size = board_size
        self.square_size = (523 - (self.size + 1) * self.spacer)/self.size
        self.width = (14) * (32 + 5) + 5 + self.grid_left_separation * 2
        self.height = ((14) + 5) * (32 + self.spacer)
        self.player_colors = [(0, 252, 0), (128, 128, 255), (0, 0, 252), (255, 127, 80), (252, 0, 0)]
        self.start_positions = start_positions
        self.hovering = list(self.blokusS.available_moves())[0]

        # initialize Pygame
        pygame.init()
        pygame.display.set_caption("")
        self.font = pygame.font.Font(None, size= self.font_size)
        self.surface = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.running = True
        self.display_text = {
            "ONE" : "1",
            "TWO" : "2",
            "THREE" : "3",
            "FOUR" : "4",
            "FIVE" : "5",
            "SEVEN" : "7",
            "A" : "A",
            "C" : "C",
            "F" : "F",
            "S" : "S",
            "L" : "L",
            "N" : "N",
            "LETTER_O" : "O",
            "P" : "P",
            "T" : "T",
            "U" : "U",
            "V" : "V",
            "W" : "W",
            "X" : "X",
            "Y" : "Y",
            "Z" : "Z"
        }
        self.event_loop()
        
    def draw_board(self) -> None:
        """
        draws board including the grid, starting positions, info-bar below, retired players, player scores, winners, current player,
        remaining pieces for every single player. 

        Creates a big black board and then creates squares over to create a grid effect. Creates bar below and adds info on top of it

        returns None
        """
        board_rect = (self.grid_left_separation, self.grid_top_separation, self.size * (self.square_size + self.spacer) + self.spacer, self.size * (self.square_size + self.spacer) + self.spacer)
        pygame.draw.rect(self.surface, color=(0, 0, 0), rect=board_rect, width=0)
        for row in range(self.size):
            for col in range(self.size):
                rect = ((col) * (self.square_size + self.spacer) + self.grid_left_separation + self.spacer, (row) * (self.square_size + self.spacer) + self.grid_top_separation + self.spacer, self.square_size, self.square_size)
                if (row, col) in self.start_positions:
                    pygame.draw.rect(self.surface, color=(128, 128, 128), rect=rect, width=0)
                else:
                    pygame.draw.rect(self.surface, color=(255, 222, 173), rect=rect, width=0)
        remaining_box = (self.grid_left_separation, self.grid_top_separation + 523, 523, 160 + self.spacer) #creates box for text
        pygame.draw.rect(self.surface, color=(0, 0, 0), rect=remaining_box, width=0) #draws box for text
        retired_players = "Retired Players: " + str(list(self.blokusS.retired_players))[1 : -1] + "     Curr_Player: " + str(self.blokusS.curr_player) #creates text for retired player
        if self.blokusS.game_over:
            retired_players = retired_players[:-14]
            retired_players += ("Winner: " + str(self.blokusS.winners)[1 : -1])
        score_board = "{ Scores } "
        retired_players_text = self.font.render(retired_players, True, (255, 255, 255)) #creates display for retired players
        self.surface.blit(retired_players_text, (32, self.grid_top_separation + 523)) #draws display for retired players

        for i in range(self.blokusS.num_players): #for each player displays remaining shapes and scores
            add_on = "  P " + str(i + 1) + ": " + str(self.blokusS.get_score(i + 1))
            score_board += add_on
            pos = 0
            remaining_list = []
            for j in self.blokusS.remaining_shapes(i+1):
                remaining_list.append(self.display_text[str(j)[10:]])
            for k in self.display_text.values():
                color_of = (128, 128, 128)
                if k in remaining_list:
                    color_of = self.player_colors[i]       
                pieces_remaining_text = self.font.render(k, True, color_of)
                self.surface.blit(pieces_remaining_text, (25 * pos + self.grid_left_separation, 603 + 24 * i))
                pos += 1
        score_board_text = self.font.render(score_board, True, (255, 255, 255))
        self.surface.blit(score_board_text, (32, self.grid_top_separation + 547))
    def hovering_piece(self, direction: str, switch: bool, mouse_pos: tuple[int, int] = (0,0)) -> None:
        """
        parameters:
        direction: where to move if moved
        switch: whether or not piece is switched
        mous_pos: position of mouse to determine if piece switch necessary if clicked
        decides if game finished


        Makes the piece that is currently hovering over.
        Takes in arguments to shift or rotate or switch if need be.
        You can click on each piece below on the info bar OR press keys
        Places hovering piece on to the board if placed

        """
        if len(self.blokusS.remaining_shapes(self.blokusS.curr_player)) == 0:
            self.hovering.shape.squares = []
        if switch:
            shape_kind_list = list(self.display_text.keys())
            shape_kind = shape_kind_list[(mouse_pos[0] - self.grid_left_separation)//25]
            for i in list(self.blokusS.available_moves()):
                if str(i.shape.kind)[10:] == shape_kind:
                    self.hovering = i
                    return None
        else:
            new_squares = []
            bounds = True
            implement = True
            if direction == "up":
                row, col = self.hovering.anchor
                self.hovering.anchor = (row - 1, col)
                for temp in self.hovering.squares():
                    r, c = temp
                    if r < 0:
                        bounds = False
                if not bounds:
                    self.hovering.anchor = (row, col)
            elif direction == "down":
                row, col = self.hovering.anchor
                self.hovering.anchor = (row + 1, col)
                for temp in self.hovering.squares():
                    r, c = temp
                    if r == self.size:
                        bounds = False
                if not bounds:
                    self.hovering.anchor = (row, col)
            elif direction == "right":
                row, col = self.hovering.anchor
                self.hovering.anchor = (row, col + 1)
                for temp in self.hovering.squares():
                    r, c = temp
                    if c == self.size:
                        bounds = False
                if not bounds:
                    self.hovering.anchor = (row, col)
            elif direction == "left":
                row, col = self.hovering.anchor
                self.hovering.anchor = (row, col - 1)
                for temp in self.hovering.squares():
                    r, c = temp
                    if c < 0:
                        bounds = False
                if not bounds:
                    self.hovering.anchor = (row, col)
            elif direction == "place":
                if self.blokusS.legal_to_place(self.hovering):
                    self.blokusS.maybe_place(self.hovering)
                    if len(self.blokusS.available_moves()) == 0:
                        self.blokusS.retire()
                    if self.blokusS.game_over:
                        self.hovering.shape.squares = []
                        self.draw_board()
                        self.draw_pieces()
                        self.game_over()
                    else:
                        self.hovering = list(self.blokusS.available_moves())[0]

    def draw_pieces(self) -> None:
        """
        draws pieces on board and hovering piece
        
        For every non empty square on the grid. Fill in the grid but not the border initially. 
        Then if two squares are adjacent to each other from the same player removes the border between to make it seem like one piece.
        Finally if there's a square configuration of squares on the grid all from the same player, covers up the center dot to make it seem like one piece

        Returns None
        """
    
        for row in range(self.size):
            for col in range(self.size):
                if self.blokusS.grid[row][col] is not None:
                    rect = (col * (self.square_size + self.spacer) + self.grid_left_separation + self.spacer, (row) * (self.square_size + self.spacer) + self.grid_top_separation + self.spacer, self.square_size, self.square_size)
                    pygame.draw.rect(self.surface, color = self.player_colors[self.blokusS.grid[row][col][0]-1], rect=rect, width=0) 
                    row_adj = False
                    if (row, col) not in self.hovering.squares(): #fills in border between two vertically adjacent squares from same player. 
                        if 0 < row + 1 < self.size and self.blokusS.grid[row + 1][col] is not None and self.blokusS.grid[row + 1][col][0] == self.blokusS.grid[row][col][0] and (row + 1, col) not in self.hovering.squares():
                            rect = (col * (self.square_size + self.spacer) + self.grid_left_separation + self.spacer, (1 + row) * (self.square_size + self.spacer) + self.grid_top_separation - 1, self.square_size, self.spacer + 2)
                            pygame.draw.rect(self.surface, color = self.player_colors[self.blokusS.grid[row][col][0]-1], rect=rect, width=0)
                            row_adj = True
                        if 0 < col + 1 < self.size and self.blokusS.grid[row][col + 1] is not None and self.blokusS.grid[row][col + 1][0] == self.blokusS.grid[row][col][0] and (row, col + 1) not in self.hovering.squares(): #fills in border between two horizontally adjacent squares from same player, and border dot in squares
                            if row_adj and (row + 1, col + 1) not in self.hovering.squares() and self.blokusS.grid[row + 1][col + 1] is not None and self.blokusS.grid[row + 1][col + 1][0] == self.blokusS.grid[row][col][0]:
                                rect = ((1 + col) * (self.square_size + self.spacer) + self.grid_left_separation - 1, (row) * (self.square_size + self.spacer) + self.spacer + self.grid_top_separation, self.spacer + 2, self.square_size * 2)
                                pygame.draw.rect(self.surface, color = self.player_colors[self.blokusS.grid[row][col][0] - 1], rect=rect, width=0)
                            else:  #only difference is that if there's a square, the rectangle placed over the border is long enough to cover center dot
                                rect = ((1 + col) * (self.square_size + self.spacer) + self.grid_left_separation - 1, (row) * (self.square_size + self.spacer) + self.spacer + self.grid_top_separation, self.spacer + 2, self.square_size)
                                pygame.draw.rect(self.surface, color = self.player_colors[self.blokusS.grid[row][col][0] - 1], rect=rect, width=0)
            hovering_squares = self.hovering.squares()
        for coord in hovering_squares:
            row, col = coord
            rect = (col * (self.square_size + self.spacer) + self.grid_left_separation + self.spacer, (row) * (self.square_size + self.spacer) + self.grid_top_separation + self.spacer, self.square_size, self.square_size)
            pygame.draw.rect(self.surface, color = self.player_colors[4], rect=rect, width=0) 
            row_adj = False
            if (row + 1, col) in hovering_squares: #fills in border between two vertically adjacent squares from same player. 
                rect = (col * (self.square_size + self.spacer) + self.grid_left_separation + self.spacer, (row + 1) * (self.square_size + self.spacer) + self.grid_top_separation - 1, self.square_size, self.spacer + 2)
                pygame.draw.rect(self.surface, color = self.player_colors[4], rect=rect, width=0)
                row_adj = True
            if (row, col + 1) in hovering_squares: #fills in border between two horizontally adjacent squares from same player, and border dot in squares
                if row_adj and (1 + row, 1 + col) in hovering_squares:
                    rect = ((1 + col) * (self.square_size + self.spacer) + self.grid_left_separation - 1, (row) * (self.square_size + self.spacer) + self.spacer + self.grid_top_separation, self.spacer + 2, self.square_size * 2)
                    pygame.draw.rect(self.surface, color = self.player_colors[4], rect=rect, width=0)
                else: #only difference is that if there's a square, the rectangle placed over the border is long enough to cover center dot
                    rect = ((1 + col) * (self.square_size + self.spacer) + self.grid_left_separation - 1, (row) * (self.square_size + self.spacer) + self.spacer + self.grid_top_separation, self.spacer + 2, self.square_size)
                    pygame.draw.rect(self.surface, color = self.player_colors[4], rect=rect, width=0)

    def do_flips(self, key: int) -> None:
        """
        key: button pressed 

        Does flips and rotations 

        Returns None
        """
        if key == pygame.K_r:
            self.hovering.rotate_right()
        elif key == pygame.K_e:
            self.hovering.rotate_left()
        elif key == pygame.K_SPACE:
            self.hovering.flip_horizontally()
    
    def draw_window(self) -> None:
        """
        Draw the window.

        Returns (None): Nothing, draws.
        """
        
        self.surface.fill((128, 128, 128))
        
    def event_loop(self) -> None:
        """
        Handles the interactions. 

        Returns (None): Nothing.

        """
        while True:
            # process Pygame events
            if self.running:
                self.game()
            else:
                self.game_over()
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            pygame.display.update()
            self.clock.tick(24)

    def game(self):
        """
        Runs game and takes in user interactions

        Returns None
        """
        self.draw_window()
        self.draw_board()
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            elif event.type == pygame.MOUSEBUTTONUP:
                if (self.grid_left_separation < pygame.mouse.get_pos()[0] < 21 * 25 + self.grid_left_separation
                and self.grid_top_separation + 523 < pygame.mouse.get_pos()[1] < self.grid_top_separation + 651):
                    self.hovering_piece("None", True, pygame.mouse.get_pos())
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.blokusS.retire()
                    if self.blokusS.game_over:
                        self.draw_board()
                        self.draw_pieces()
                        self.game_over()
                        return None
                    else:
                        self.hovering = list(self.blokusS.available_moves())[0]
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_UP:
                    self.hovering_piece("up", False)
                if event.key == pygame.K_DOWN:
                    self.hovering_piece("down", False)
                if event.key == pygame.K_LEFT:
                    self.hovering_piece("left", False)
                if event.key == pygame.K_RIGHT:
                    self.hovering_piece("right", False)
                if event.key == pygame.K_RETURN:
                    self.hovering_piece("place", False)
                if event.key in {pygame.K_r, pygame.K_e, pygame.K_SPACE}:
                    self.do_flips(event.key)
                if 0 <= event.key < 0x110000: 
                    if chr(event.key) in key_to_shape:
                        shape_kind = key_to_shape[chr(event.key)]
                        if shape_kind in self.blokusS.remaining_shapes(self.blokusS.curr_player):
                            for i in list(self.blokusS.available_moves()):
                                if i.shape.kind == shape_kind:
                                    self.hovering = i
                                    break
        self.draw_pieces()

    def game_over(self):
        """
        changes the running boolean that the game running depends on.

        Returns None
        """
        self.running = False

if __name__ == "__main__":
    main()
