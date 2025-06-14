"""
Blokus shapes and pieces.

Modify only the methods marked as TODO.
"""
import copy
import textwrap
from typing import Optional

from shape_definitions import ShapeKind, definitions

# A point is represented by row and column numbers (r, c). The
# top-left corner of a grid is (0, 0). Note that rows/columns
# correspond to vertical/horizontal axes, respectively. So, we
# will typically index into a 2-dimensional grid using
# grid[r][c] (as opposed to grid[y][x]).
#
Point = tuple[int, int]


# We will typically unpack a Point as follows: (r, c) = point
# In other cases, the row and col functions may be helpful.
#
def row(point: Point) -> int:
    """Returns the row value of a point."""
    return point[0]


def col(point: Point) -> int:
    """Returns the column value of a point."""
    return point[1]


class Shape:
    """
    Representing the 21 Blokus shapes, as named and defined by
    the string representations in shape_definitions.py.

    The locations of the squares are relative to the origin.

    The can_be_transformed boolean indicates whether or not
    the origin was explicitly defined in the string
    representation of the shape.

    See shape_definitions.py for more details.

    NOTE: The presence of the origin attribute in this class
    is a design bug. All points in the squares list, which define
    the shape, should be relative to an implicit origin of (0, 0).
    Most string representations in shape_definitions refer to
    origins explicitly (using the 'O' and '@') characters: those
    origins should be used by Shape.from_string to define the
    squares of the shape (relative to an origin of (0, 0)). But
    after doing so, the origin used in the string representation
    is no longer needed anywhere in our design or implementation.
    To remain backwards compatible with the original design, you
    can implement the constructor and Shape.from_string to set the
    Shape object's origin attribute to be the origin used in the
    string representation. But don't refer to this attribute
    elsewhere in your implementation; the information should not
    be necessary.
    """

    kind: ShapeKind
    origin: Point
    can_be_transformed: bool
    squares: list[Point]

    def __init__(
        self,
        kind: ShapeKind,
        origin: Point,
        can_be_transformed: bool,
        squares: list[Point],
    ) -> None:
        """
        Constructor
        """
        self.kind = kind
        self.origin = origin
        self.can_be_transformed = can_be_transformed
        self.squares = squares

    def __str__(self) -> str:
        """
        Returns a complete string representation of the
        shape.
        """
        return f"""
            Shape
                kind = {self.kind}
                origin = {self.origin}
                can_be_transformed = {self.can_be_transformed}
                squares = {list(map(str, self.squares))}
        """

    @staticmethod
    def from_string(kind: ShapeKind, definition: str) -> "Shape":
        """
        Create a Shape based on its string representation
        in shape_definitions.py. See that file for details.
        """
        # Check that entering legal shape
        assert kind in definitions, f"kind: {kind} not in definitions :("

        shape_squares: list[tuple[int]] = []
        shape_def_list = list(textwrap.dedent(definition))
        shape_def_list.remove("\n")
        square_col: int = 0
        square_row: int = 0
        has_origin = False
        origin_index = 0

        if "O" in shape_def_list or "@" in shape_def_list:
            if "O" in shape_def_list:
                origin_index = shape_def_list.index("O")
            if "@" in shape_def_list:
                origin_index = shape_def_list.index("@")
            
            prev_rows: int = shape_def_list[:origin_index].count("\n")
            prev_cols: int = 0
            if prev_rows == 0:
                prev_cols = (shape_def_list[:origin_index].count(" ")
                        + shape_def_list[:origin_index].count("@") + shape_def_list[:origin_index].count("X"))
            else:
                for prev in shape_def_list[:origin_index]:
                    if prev == "\n":
                        prev_cols = 0
                    else:
                        prev_cols += 1
            square_row = -prev_rows
            square_col: int = -prev_cols
            origin = tuple()
            has_origin = True

        for square in shape_def_list:
            if square == "\n" and has_origin:
                square_row += 1
                square_col = -prev_cols
            elif square == "\n" and not has_origin:
                square_row += 1
                square_col = 0
            elif square == " " or square == "@":
                square_col += 1
            elif square == "X":
                shape_squares.append((square_row, square_col))
                square_col += 1
            elif square == "O":
                square_row = 0
                square_col = 0
                shape_squares.append((square_row, square_col))
                origin = (square_row, square_col)
                square_col += 1

        if not has_origin:
            return Shape(kind, (0, 0), False, shape_squares)
        return Shape(kind, origin, True, shape_squares)

    def flip_horizontally(self) -> None:
        """
        Flip the shape horizontally
        (across the vertical axis through its origin),
        by modifying the squares in place.
        """
        for i, point in enumerate(self.squares):
            r, c = point
            self.squares[i] = (r, -c)

    def rotate_left(self) -> None:
        """
        Rotate the shape left by 90 degrees,
        by modifying the squares in place.
        """
        for i, point in enumerate(self.squares):
            r, c = point
            self.squares[i] = (-c, r)

    def rotate_right(self) -> None:
        """
        Rotate the shape right by 90 degrees,
        by modifying the squares in place.
        """
        for i, point in enumerate(self.squares):
            r, c = point
            self.squares[i] = (c, -r)


class Piece:
    """
    A Piece takes a Shape and orients it on the board.

    The anchor point is used to locate the Shape.

    For flips and rotations, rather than storing these
    orientations directly (for example, using two attributes
    called face_up: bool and rotation: int), we modify
    the shape attribute in place. Therefore, it is important
    that each Piece object has its own deep copy of a
    Shape, so that transforming one Piece does not affect
    other Pieces that have the same Shape.
    """

    shape: Shape
    anchor: Optional[Point]

    def __init__(self, shape: Shape, face_up: bool = True, rotation: int = 0):
        """
        Each Piece will get its own deep copy of the given shape
        subject to initial transformations according to the arguments:

            face_up:  If true, the initial Shape will be flipped
                      horizontally.
            rotation: This number, modulo 4, indicates how many
                      times the shape should be right-rotated by
                      90 degrees.
        """
        # Deep copy shape, so that it can be transformed in place
        self.shape = copy.deepcopy(shape)

        # The anchor will be set by set_anchor
        self.anchor = None

        # We choose to flip...
        if not face_up:
            self.shape.flip_horizontally()

        # ... before rotating
        for _ in range(rotation % 4):
            self.shape.rotate_right()

    def set_anchor(self, anchor: Point) -> None:
        """
        Set the anchor point.
        """
        self.anchor = anchor

    def _check_anchor(self) -> None:
        """
        Raises ValueError if anchor is not set.
        Used by the flip and rotate methods below,
        so each of those may raise ValueError.
        """
        if self.anchor is None:
            raise ValueError(f"Piece does not have anchor: {self.shape}")

    def flip_horizontally(self) -> None:
        """
        Flip the piece horizontally.
        """
        self._check_anchor()
        self.shape.flip_horizontally()

    def rotate_left(self) -> None:
        """
        Rotate the shape left by 90 degrees,
        by modifying the squares in place.
        """
        self._check_anchor()
        self.shape.rotate_left()

    def rotate_right(self) -> None:
        """
        Rotate the shape right by 90 degrees,
        by modifying the squares in place.
        """
        self._check_anchor()
        self.shape.rotate_right()

    def squares(self) -> list[Point]:
        """
        Returns the list of points corresponding to the
        current position and orientation of the piece.

        Raises ValueError if anchor is not set.
        """
        self._check_anchor()
        assert self.anchor is not None
        return [
            (row(self.anchor) + r, col(self.anchor) + c)
            for r, c in self.shape.squares
        ]

    def cardinal_neighbors(self) -> set[Point]:
        """
        Returns the combined cardinal neighbors
        (north, south, east, and west)
        corresponding to all of the piece's squares.

        Raises ValueError if anchor is not set.
        """
        self._check_anchor()

        card_nbs = set()
        for (r,c) in self.squares():
            c_directions = {(r - 1, c), (r + 1, c), (r, c + 1), (r, c - 1)}
            for neighbor in c_directions:
                if neighbor not in self.squares():
                    card_nbs.add(neighbor)
        return card_nbs

    def intercardinal_neighbors(self) -> set[Point]:
        """
        Returns the combined intercardinal neighbors
        (northeast, southeast, southwest, and northwest)
        corresponding to all of the piece's squares.

        Raises ValueError if anchor is not set.
        """
        self._check_anchor()

        card_int_nbs = set()
        for (r,c) in self.squares():
            ic_directions = {(r - 1, c + 1), (r + 1, c + 1), (r + 1, c - 1), 
                             (r - 1, c - 1)}
            for int_neighbor in ic_directions:
                if int_neighbor not in self.squares() and (int_neighbor not in
                                                    self.cardinal_neighbors()):
                    card_int_nbs.add(int_neighbor)
        return card_int_nbs
