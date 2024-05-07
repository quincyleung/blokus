
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
from fakes import BlokusStub, BlokusFake
from piece import Point, Shape, Piece
from shape_definitions import definitions, ShapeKind

BOARD_SIZE = int(sys.argv[1])

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
    square_size: int
    spacer: int
    duration: int
    font_size: int
    width: int
    height: int
    display_nums: str
    most_recent_timer: str

    #replace with BLOKUS
    def __init__(self, blokusS: BlokusFake):
        """

        """
        self.font_size = 30
        self.blokusS = blokusS
        self.square_size = 32
        self.spacer = 5
        self.size = BOARD_SIZE  
        self.width = ((self.size) + 2) * (self.square_size + self.spacer)
        self.height = ((self.size) + 4) * (self.square_size + self.spacer)
        self.player_colors = [(0, 252, 0), (128, 128, 255), (0, 252, 0)]
        self.start_positions = set()
        self.start_positions.add(((self.size//4), self.size//4))
        self.start_positions.add((3 * (self.size//4), 3 * (self.size//4)))
        self.hovering = None

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
        board_rect = (self.square_size, self.square_size, self.size * (self.square_size + self.spacer) + self.spacer, self.size * (self.square_size + self.spacer) + self.spacer)
        pygame.draw.rect(self.surface, color=(0, 0, 0), rect=board_rect, width=0)
        for row in range(self.size):
            for col in range(self.size):
                rect = ((1 + col) * (self.square_size + self.spacer), (1 + row) * (self.square_size + self.spacer), self.square_size, self.square_size)
                if (row, col) in self.start_positions:
                    pygame.draw.rect(self.surface, color=(128, 128, 128), rect=rect, width=0)
                else:
                    pygame.draw.rect(self.surface, color=(255, 222, 173), rect=rect, width=0)
                if self.blokusS.grid[row][col] is not None:
                    if self.blokusS.grid[row][col][0] == 3:
                        self.blokusS.grid[row][col] = None
        remaining_1 = ""
        for i in range(2):
            for j in self.blokusS.remaining_shapes(i+1):
                remaining_1 += str(ShapeKind(j))
        remaining_2 = (self.square_size, (self.size + 1) * (self.square_size + self.spacer) + self.spacer, self.size * (self.square_size + self.spacer) + self.spacer, self.square_size * 2)
        pygame.draw.rect(self.surface, color=(0, 0, 0), rect=remaining_2, width=0)
        pieces_remaining_text_1 = self.font.render(remaining_1, True, (255,255,255))
        pieces_remaining_text_2 = self.font.render(remaining_1, True, (255,255,255))
        self.surface.blit(pieces_remaining_text_1, (self.square_size, (self.size + 1) * (self.square_size + self.spacer) + self.spacer))
        self.surface.blit(pieces_remaining_text_2, (self.square_size, (self.size + 2) * (self.square_size + self.spacer) + self.spacer))

    def hovering_piece(self, direction, switch) -> None:
        if self.hovering == None:
            self.hovering = list(self.blokusS.available_moves())[0]
        elif switch:
            return None
        else:
            new_squares = []
            for temp in self.hovering.shape.squares:
                r, c = temp
                new_squares.append((r,c+1))
            self.hovering.shape.squares = new_squares
        if self.hovering in self.blokusS.available_moves():
            self.blokusS.maybe_place(self.hovering)
            for square in self.hovering.shape.squares:
                r, c = square
                self.grid[r][c][0] = 3
        print(self.hovering.shape)
        print(self.blokusS.grid)


        """
            self.hovering.face_up = face_up
            self.hovering.rotation = rotation
            self.hovering.shape.kind = kind
            self.hovering.shape.origin = origin
            self.hovering.shape.can_be_transformed = can_be_transformed
            self.hovering.shape.squares = squares
            if direction == "up":
                print(self.hovering)
                valid = True
                new_squares = []
                for i in squares:
                    r , c = i
                    new_squares.append((r-1, c))
                    if r - 1 < 0 or self.blokusS.grid[r-1][c] != None:
                        valid = False
                if valid:
                    self.hovering = Piece(Shape(kind, origin, can_be_transformed, new_squares), rotation, face_up)
                    for square in new_squares:
                        r, c = square
                        self.blokusS.grid[r][c] = (3, kind)
        """
                

        """
        events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    pos = event.pos
                    self.click(pos)
        """

    def draw_pieces(self) -> None:
        """
        """

        for row in range(self.size):
            for col in range(self.size):
                if self.blokusS.grid[row][col] is not None:
                    rect = ((1 + col) * (self.square_size + self.spacer), (1 + row) * (self.square_size + self.spacer), self.square_size, self.square_size)
                    pygame.draw.rect(self.surface, color = self.player_colors[self.blokusS.grid[row][col][0]-1], rect=rect, width=0) #color dict[player
                    for i in range(2):
                        if 0 < row + (-1) ** i < self.size and self.blokusS.grid[row + (-1) ** i][col] is not None and self.blokusS.grid[row + (-1) ** i][col][0] == self.blokusS.grid[row][col][0]:
                            rect = ((1 + col) * (self.square_size + self.spacer), (2 + row - i) * (self.square_size + self.spacer) - self.spacer, self.square_size, self.spacer)
                            pygame.draw.rect(self.surface, color = self.player_colors[self.blokusS.grid[row][col][0]-1], rect=rect, width=0)
                    for j in range(2):
                        if 0 < col + (-1) ** j < self.size and self.blokusS.grid[row][col + (-1) ** j] is not None and self.blokusS.grid[row][col + (-1) ** j][0] == self.blokusS.grid[row][col][0]:
                            rect = ((2 + col - j) * (self.square_size + self.spacer) - self.spacer, (1 + row) * (self.square_size + self.spacer), self.spacer, self.square_size)
                            pygame.draw.rect(self.surface, color = self.player_colors[self.blokusS.grid[row][col][0]-1], rect=rect, width=0)

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
            self.draw_window()
            self.draw_board()
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYUP:
                    self.hovering_piece("up", False)
            self.draw_pieces()
            pygame.display.update()
            self.clock.tick(24)
        
    def click(self, pos: tuple[int,int]):
        """
        """

if __name__ == "__main__":
    blokus : BlokusStub = BlokusStub(num_players=0, size=BOARD_SIZE, start_positions=set())
    GUI(blokus)