
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
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
from fakes import BlokusStub
from piece import Point, Shape, Piece

class GUI:
    """
    Class for a GUI-based keypad
    """
    width:   int
    height:  int
    border:  int
    number:  int
    buttons: dict[str, tuple[int, int]]
    most_recent: str
    button_side: int
    spacer: int
    duration: int
    font_size: int
    width: int
    height: int
    display_nums: str
    most_recent_timer: str

    #replace with BLOKUS
    def __init__(self, blokusS: BlokusStub):
        """

        """
        #self.grid = blokus.grid
        self.blokusS = blokusS
        self.square_size = 32
        self.spacer = 5
        self.size = self.blokusS.size
        self.width = ((self.size) + 2) * (self.square_size + self.spacer)
        self.height = ((self.size) + 2) * (self.square_size + self.spacer)
        self.player_colors = [(0, 252, 0), (128, 128, 255)]
        self.start_positions = set()
        self.start_positions.add(((self.size//4), self.size//4))
        self.start_positions.add((3 * (self.size//4), 3 * (self.size//4)))

        # initialize Pygame
        pygame.init()
        pygame.display.set_caption("")
        self.font = pygame.font.Font(None, size= self.font_size)
        self.surface = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.event_loop()

    def draw_board(self) -> None:
        """
        """
        board_rect = (self.square_size, self.square_size, self.grid_size * (self.square_size + self.spacer) + self.spacer, self.grid_size * (self.square_size + self.spacer) + self.spacer)
        pygame.draw.rect(self.surface, color=(0, 0, 0), rect=board_rect, width=0)
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                rect = ((1 + col) * (self.square_size + self.spacer), (1 + row) * (self.square_size + self.spacer), self.square_size, self.square_size)
                if (row, col) in start_positions:
                    pygame.draw.rect(self.surface, color=(128, 128, 128), rect=rect, width=0)
                else:
                    pygame.draw.rect(self.surface, color=(255, 222, 173), rect=rect, width=0)

    def draw_pieces(self) -> None:
        """
        """

        for row in range(self.grid_size):
            for col in range(self.grid_size):
                if self.grid[row][col] is not None:
                    rect = ((1 + col) * (self.square_size + self.spacer), (1 + row) * (self.square_size + self.spacer), self.square_size, self.square_size)
                    pygame.draw.rect(self.surface, color = self.player_colors[self.grid[row][col][0]], rect=rect, width=0) #color dict[player]
                    for i in range(2):
                        if 0 < row + (-1) ** i < self.grid_size and self.grid[row + (-1) ** i][col] is not None and self.grid[row + (-1) ** i][col][0] == self.grid[row][col][0]:
                            rect = ((1 + col) * (self.square_size + self.spacer), (2 + row - i) * (self.square_size + self.spacer) - self.spacer, self.square_size, self.spacer)
                            pygame.draw.rect(self.surface, color = self.player_colors[self.grid[row][col][0]], rect=rect, width=0)
                    for j in range(2):
                        if 0 < col + (-1) ** j < self.grid_size and self.grid[row][col + (-1) ** j] is not None and self.grid[row][col + (-1) ** j][0] == self.grid[row][col][0]:
                            rect = ((2 + col - j) * (self.square_size + self.spacer) - self.spacer, (1 + row) * (self.square_size + self.spacer), self.spacer, self.square_size)
                            pygame.draw.rect(self.surface, color = self.player_colors[self.grid[row][col][0]], rect=rect, width=0)

    def draw_window(self) -> None:
        """
        Draw the window.

        Returns (None): Nothing, draws.
        """
        
        self.surface.fill((128, 128, 128))
        
    def event_loop(self) -> None:
        """
        Handle user interaction.

        Returns (None): Nothing.
        """
        while True:
            # process Pygame events
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    pos = event.pos
                    self.click(pos)

            # update the display
            self.draw_window()
            self.draw_board()
            self.draw_pieces()
            pygame.display.update()
            self.clock.tick(24)
        
    def click(self, pos: tuple[int,int]):
        """
        """

if __name__ == "__main__":
    GUI(BlokusStub)