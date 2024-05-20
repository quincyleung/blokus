######### Milestone 3: Grids To and From Strings ##########
import pytest
#from typing import Optional
from textwrap import dedent

from base import Grid
from piece import Piece # Point, Shape,
from shape_definitions import ShapeKind
#from blokus import Blokus
from tests import test_blokus

def grid_to_string(grid: Grid) -> str:
    """
    Convert a Blokus grid into a string representation that indicates board size
    with an explicit border, occupied cells with a string indicating which
    player's piece is covering it (P1 = X, P2 = O)
    """
    # Column indices: 2 spaces, 0, space, 1, space, ..., n, 3 spaces 
    str_result = "  " + " ".join(str(i % 10) for i in range(len(grid[0]))) + "   \n"
    str_result += "||" + "||" * len(grid[0]) + "||\n" #top border

    for i, row in enumerate(grid):
        str_result += "||" #start new rows with left border
        for cell in row:
            if cell == None:
                str_result += "  " #2 spaces for unoccupied cells
            else:
                player, shape = cell
                if player == 1:
                    str_result += f"{shape.value} " #occupies L side
                if player == 2:
                    str_result += f" {shape.value}" #occupies R side
        str_result += f"|| {i}\n" # end rows with right border and row index

    str_result += "||" + "||" * len(grid[0]) + "||" #bottom border
    return str_result

def string_to_grid(s: str) -> Grid:
    """
    Coverts a string representation as defined in grid_to_string back into a
    Grid
    """
    lines = s.strip().split('\n') # split by newlines to get rows
    lines = lines[2:-1] # remove column indices, top and bottom borders
    #print(f"lines: {lines}")
    grid_result = []

    for line in lines:
        line = line[line.find('||')+2:line.rfind('||')] #remove row indices, R and L borders
        grid_row = []
        for i in range(0, len(line), 2): #process each cell in pairs
            cell = line[i:i+2]
            if cell == '  ':
                grid_row.append(None) #two spaces mean empty cell
            elif cell[0] == ' ': #first space empty means P2
                grid_row.append((2, ShapeKind(cell[1])))
            elif cell[1] == ' ': #second space empty means P1
                grid_row.append((1, ShapeKind(cell[0])))
        grid_result.append(grid_row)
    return grid_result

# Test Blokus Mini, P1 places ONE at (0, 0) and P2 places ONE at (4, 4)
def test_grid_1() -> None:
    blokus = test_blokus.test_init_blokus_mini_2()

    # P1 plays ONE at (0, 0)
    piece_one = Piece(blokus.shapes[ShapeKind.ONE])
    piece_one.set_anchor((0, 0))
    blokus.maybe_place(piece_one)

    # P2 plays ONE at (4, 4)
    piece_one.set_anchor((4, 4))
    blokus.maybe_place(piece_one)

    grid = blokus.grid
    s = """
          0 1 2 3 4   
        ||||||||||||||
        ||1         || 0
        ||          || 1
        ||          || 2
        ||          || 3
        ||         1|| 4
        ||||||||||||||
        """

    assert '  ' + dedent(s).strip() == grid_to_string(grid)
    assert grid == string_to_grid(grid_to_string(grid))

# Test Blokus Mini, P1 places C at (0, 0) and P2 places TWO at (4, 3)
def test_grid_2() -> None:
    blokus = test_blokus.test_init_blokus_mini_2()

    # P1 plays C at (0, 0)
    piece_c = Piece(blokus.shapes[ShapeKind.C])
    piece_c.set_anchor((0, 0))
    blokus.maybe_place(piece_c)

    # P2 plays TWO at (4, 3)
    piece_two = Piece(blokus.shapes[ShapeKind.TWO])
    piece_two.set_anchor((4, 3))
    blokus.maybe_place(piece_two)

    grid = blokus.grid
    s = """
          0 1 2 3 4   
        ||||||||||||||
        ||C C       || 0
        ||C         || 1
        ||          || 2
        ||          || 3
        ||       2 2|| 4
        ||||||||||||||
        """

    assert '  ' + dedent(s).strip() == grid_to_string(grid)
    assert grid == string_to_grid(grid_to_string(grid))

# Test Blokus Duo, P1 places ONE at (4, 4) and P2 places ONE at (9, 9)
def test_grid_3() -> None:
    blokus = test_blokus.test_init_blokus_duo_2()

    # P1 plays ONE at (4, 4)
    piece_one = Piece(blokus.shapes[ShapeKind.ONE])
    piece_one.set_anchor((4, 4))
    blokus.maybe_place(piece_one)

    # P2 plays ONE at (9, 9)
    piece_one.set_anchor((9, 9))
    blokus.maybe_place(piece_one)

    grid = blokus.grid
    s = """
          0 1 2 3 4 5 6 7 8 9 0 1 2 3   
        ||||||||||||||||||||||||||||||||
        ||                            || 0
        ||                            || 1
        ||                            || 2
        ||                            || 3
        ||        1                   || 4
        ||                            || 5
        ||                            || 6
        ||                            || 7
        ||                            || 8
        ||                   1        || 9
        ||                            || 10
        ||                            || 11
        ||                            || 12
        ||                            || 13
        ||||||||||||||||||||||||||||||||
        """

    assert '  ' + dedent(s).strip() == grid_to_string(grid)
    assert grid == string_to_grid(grid_to_string(grid).strip())

# Test Blokus Duo, P1 places C at (4, 4) and P2 places TWO at (9, 9)
def test_grid_4() -> None:
    blokus = test_blokus.test_init_blokus_duo_2()

    # P1 plays C at (4, 4)
    piece_c = Piece(blokus.shapes[ShapeKind.C])
    piece_c.set_anchor((4, 4))
    blokus.maybe_place(piece_c)

    # P2 plays TWO at (9, 9)
    piece_two = Piece(blokus.shapes[ShapeKind.TWO])
    piece_two.set_anchor((9, 9))
    blokus.maybe_place(piece_two)

    grid = blokus.grid
    s = """
          0 1 2 3 4 5 6 7 8 9 0 1 2 3   
        ||||||||||||||||||||||||||||||||
        ||                            || 0
        ||                            || 1
        ||                            || 2
        ||                            || 3
        ||        C C                 || 4
        ||        C                   || 5
        ||                            || 6
        ||                            || 7
        ||                            || 8
        ||                   2 2      || 9
        ||                            || 10
        ||                            || 11
        ||                            || 12
        ||                            || 13
        ||||||||||||||||||||||||||||||||
        """

    assert '  ' + dedent(s).strip() == grid_to_string(grid)
    assert grid == string_to_grid(grid_to_string(grid).strip())

# Test Blokus Mono, P1 places ONE at (5, 5)
def test_grid_5() -> None:
    blokus = test_blokus.test_init_blokus_mono()

    # P1 plays ONE at (5, 5)
    piece_one = Piece(blokus.shapes[ShapeKind.ONE])
    piece_one.set_anchor((5, 5))
    blokus.maybe_place(piece_one)

    grid = blokus.grid
    s = """
          0 1 2 3 4 5 6 7 8 9 0   
        ||||||||||||||||||||||||||
        ||                      || 0
        ||                      || 1
        ||                      || 2
        ||                      || 3
        ||                      || 4
        ||          1           || 5
        ||                      || 6
        ||                      || 7
        ||                      || 8
        ||                      || 9
        ||                      || 10
        ||||||||||||||||||||||||||
        """

    assert '  ' + dedent(s).strip() == grid_to_string(grid)
    assert grid == string_to_grid(grid_to_string(grid).strip())
