import pytest
from typing import Optional

from base import BlokusBase, Cell, Grid
from piece import Point, Shape, Piece
from shape_definitions import ShapeKind
from blokus import Blokus

def test_inheritance() -> None:
    """Test that Blokus inherits from BlokusBase."""
    assert issubclass(Blokus, BlokusBase), "Blokus must inherit from BlokusBase"

#test initializations
def test_init_blokus_mini_1() -> Blokus:
    """
    Construct an instance of a 1-player Blokus Mini game configuration. Verify
    that properties have been initialized correctly
    """
    blokus_mini_1 = Blokus(1, 5, {(0, 0), (0, 4), (2, 2), (4, 0), (4, 4)})

    assert blokus_mini_1.size == 5
    assert blokus_mini_1.start_positions == {(0, 0), (0, 4), (2, 2), (4, 0),
                                             (4, 4)}
    assert blokus_mini_1.num_players == 1
    assert blokus_mini_1.curr_player == 1

    assert blokus_mini_1.grid == [[None for _ in range(5)] for _ in range(5)]

def test_init_blokus_mini_2() -> Blokus:
    """
    Construct an instance of a 2-player Blokus Mini game configuration. Verify
    that properties have been initialized correctly
    """
    blokus_mini_2 = Blokus(2, 5, {(0, 0), (0, 4), (2, 2), (4, 0), (4, 4)})

    assert blokus_mini_2.size == 5
    assert blokus_mini_2.start_positions == {(0, 0), (0, 4), (2, 2), (4, 0),
                                             (4, 4)}
    assert blokus_mini_2.num_players == 2
    assert blokus_mini_2.curr_player == 1

    assert blokus_mini_2.grid == [[None for _ in range(5)] for _ in range(5)]

def test_init_blokus_mono() -> Blokus:
    """
    Construct an instance of a Blokus Mono game configuration. Verify
    that properties have been initialized correctly
    """
    blokus_mono = Blokus(1, 11, {(5,5)})

    assert blokus_mono.size == 11
    assert blokus_mono.start_positions == {(5,5)}
    assert blokus_mono.num_players == 1
    assert blokus_mono.curr_player == 1

    assert blokus_mono.grid == [[None for _ in range(11)] for _ in range(11)]

def test_init_blokus_duo_2() -> Blokus:
    """
    Construct an instance of a Blokus Duo game configuration. Verify
    that properties have been initialized correctly
    """
    blokus_duo = Blokus(2, 14, {(4, 4), (9, 9)})

    assert blokus_duo.size == 14
    assert blokus_duo.start_positions == {(4, 4), (9, 9)}
    assert blokus_duo.num_players == 2
    assert blokus_duo.curr_player == 1

    assert blokus_duo.grid == [[None for _ in range(14)] for _ in range(14)]

#for testing purposes
def init_blokus_classic() -> Blokus:
    """"Initialize a 2-player Blokus Classic game configuration."""
    return Blokus(2, 20, {(0, 0), (0, 19), (19, 0), (19, 19)})

#test shape loading, flipping, rotating
def test_shapes_loaded() -> None:
    """
    Construct an instance of any Blokus game configuration, and test that the
    shapes dictionary has been correctly initialized with all 21 Blokus shapes.
    """
    blokus = init_blokus_classic()

    #or i can iterate through: for shape in blokus.shapes?
    #actually that would construct an extra data structure, the dict of squares
    #unless can directly import the one minseo makes for piece.py

    shape = blokus.shapes[ShapeKind.ONE]
    assert shape.kind == ShapeKind.ONE
    assert shape.origin == (0, 0)
    assert not shape.can_be_transformed
    assert shape.squares == [(0, 0)]

    shape = blokus.shapes[ShapeKind.TWO]
    assert shape.kind == ShapeKind.TWO
    assert shape.origin == (0, 0)
    assert shape.can_be_transformed
    assert shape.squares == [(0, 0), (0, 1)]

    shape = blokus.shapes[ShapeKind.THREE]
    assert shape.kind == ShapeKind.THREE
    assert shape.origin == (0, 0)
    assert shape.can_be_transformed
    assert shape.squares == [(-1, 0), (0, 0), (0, 1)]

    shape = blokus.shapes[ShapeKind.C]
    assert shape.kind == ShapeKind.C
    assert shape.origin == (0, 0)
    assert shape.can_be_transformed
    assert shape.squares == [(0, 0), (0, 1), (1, 0)]

    shape = blokus.shapes[ShapeKind.FOUR]
    assert shape.kind == ShapeKind.FOUR
    assert shape.origin == (0, 0)
    assert shape.can_be_transformed
    assert shape.squares == [(0, -1), (0, 0), (0, 1), (0, 2)]

    shape = blokus.shapes[ShapeKind.SEVEN]
    assert shape.kind == ShapeKind.SEVEN
    assert shape.origin == (0, 0)
    assert shape.can_be_transformed
    assert shape.squares == [(-1, -1), (-1, 0), (0, 0), (1, 0)]

    shape = blokus.shapes[ShapeKind.S]
    assert shape.kind == ShapeKind.S
    assert shape.origin == (0, 0)
    assert shape.can_be_transformed
    assert shape.squares == [(0, 0), (0, 1), (1, -1), (1, 0)]

    shape = blokus.shapes[ShapeKind.LETTER_O]
    assert shape.kind == ShapeKind.LETTER_O
    assert shape.origin == (0, 0)
    assert not shape.can_be_transformed
    assert shape.squares == [(0, 0), (0, 1), (1, 0), (1, 1)]

    shape = blokus.shapes[ShapeKind.A]
    assert shape.kind == ShapeKind.a
    assert shape.origin == (0, 0)
    assert shape.can_be_transformed
    assert shape.squares == [(-1, 0), (0, -1), (0, 0), (0, 1)]

    shape = blokus.shapes[ShapeKind.F]
    assert shape.kind == ShapeKind.F
    assert shape.origin == (0, 0)
    assert shape.can_be_transformed
    assert shape.squares == [(-1, 0), (-1, 1), (0, -1), (0, 0), (1, 0)]

    shape = blokus.shapes[ShapeKind.FIVE]
    assert shape.kind == ShapeKind.FIVE
    assert shape.origin == (0, 0)
    assert shape.can_be_transformed
    assert shape.squares == [(-2, 0), (-1, 0), (0, 0), (1, 0), (2, 0)]

    shape = blokus.shapes[ShapeKind.L]
    assert shape.kind == ShapeKind.L
    assert shape.origin == (0, 0)
    assert shape.can_be_transformed
    assert shape.squares == [(-2, 0), (-1, 0), (0, 0), (1, 0), (1, 1)]

    # Add minseo's 9 when she's done

    shape = blokus.shapes[ShapeKind.Z]
    assert shape.kind == ShapeKind.Z
    assert shape.origin == (1, 1)
    assert shape.can_be_transformed
    assert shape.squares == [(-1, -1), (-1, 0), (0, 0), (1, 0), (1, 1)]

    shape = blokus.shapes[ShapeKind.V]
    assert shape.kind == ShapeKind.V
    assert shape.origin == (1, 1)
    assert shape.can_be_transformed
    assert shape.squares == [(-1, 1), (0, 1), (1, -1), (1, 0), (1, 1)]

def test_some_flipped_shapes() -> Blokus:
    """
    Construct an instance of any Blokus game configuration, and test that at
    least three kinds of shapes can be flipped correctly via the
    Shape.flip_horizontally method.
    """
    blokus = init_blokus_classic()

    # A few shapes for testing
    piece_two = Piece(blokus.shapes[ShapeKind.TWO])
    piece_five = Piece(blokus.shapes[ShapeKind.FIVE])
    piece_a = Piece(blokus.shapes[ShapeKind.A])
    piece_f = Piece(blokus.shapes[ShapeKind.F])

    piece_two.flip_horizontally()
    assert piece_two.squares == [(0, -1), (0, 0)]

    piece_five.flip_horizontally()
    assert piece_five.squares == [(-2, 0), (-1, 0), (0, 0), (1, 0), (2, 0)]

    piece_a.flip_horizontally()
    assert piece_a.squares == [(-1, 0), (0, -1), (0, 0), (0, 1)]

    piece_f.flip_horizontally()
    assert piece_f.squares == [(-1, -1), (-1, 0), (0, 0), (0, 1), (1, 0)] 

def test_some_left_rotated_shapes() -> Blokus:
    """
    Construct an instance of any Blokus game configuration, and test that at
    least three kinds of shapes can be flipped correctly via the
    Shape.rotate_left method.
    """
    blokus = init_blokus_classic()

    # A few shapes for testing
    piece_two = Piece(blokus.shapes[ShapeKind.TWO])
    piece_five = Piece(blokus.shapes[ShapeKind.FIVE])
    piece_a = Piece(blokus.shapes[ShapeKind.A])
    piece_f = Piece(blokus.shapes[ShapeKind.F])

    # Order assumes rotate_left rotates each (r,c)->(-c,r) in original order
    piece_two.rotate_left()
    assert piece_two.squares == [(0, 0), (-1, 0)]

    piece_five.rotate_left()
    assert piece_five.squares == [(0, 2), (0, 1), (0, 0), (0, -1), (0, -2)]

    piece_a.rotate_left()
    assert piece_a.squares == [(0, -1), (1, 0), (0, 0), (-1, 0)]

    piece_f.rotate_left()
    assert piece_f.squares == [(0, -1), (-1, -1), (1, 0), (0, 0), (0, 1)] 


def test_some_right_rotated_shapes() -> Blokus:
    """
    Construct an instance of any Blokus game configuration, and test that at
    least three kinds of shapes can be flipped correctly via the
    Shape.rotate_right method.
    """
    blokus = init_blokus_classic()

    # A few shapes for testing
    piece_two = Piece(blokus.shapes[ShapeKind.TWO])
    piece_five = Piece(blokus.shapes[ShapeKind.FIVE])
    piece_a = Piece(blokus.shapes[ShapeKind.A])
    piece_f = Piece(blokus.shapes[ShapeKind.F])

    # Order assumes rotate_right rotates each (r,c)->(c,-r) in original order
    piece_two.rotate_right()
    assert piece_two.squares == [(0, 0), (1, 0)]

    piece_five.rotate_right()
    assert piece_five.squares == [(0, -2), (0, -1), (0, 0), (0, 1), (0, 2)]

    piece_a.rotate_right()
    assert piece_a.squares == [(0, -1), (-1, 0), (0, 0), (1, 0)]

    piece_f.rotate_right()
    assert piece_f.squares == [(0, 1), (1, 1), (-1, 0), (0, 0), (0, -1)] 


#test neighbors
def test_some_cardinal_neighbors() -> None:
    """
    Construct an instance of any Blokus game configuration, and test that
    Piece.cardinal_neighbors correctly computes the cardinal neighbors of at
    least three kinds of pieces.
    """

def test_some_intercardinal_neighbors() -> None:
    """
    Construct an instance of any Blokus game configuration, and test that
    Piece.intercardinal_neighbors correctly computes the cardinal neighbors of
    at least three kinds of pieces.
    """

#test game runs
def test_one_player_blokus_mini_game() -> None:
    """
    Construct a 1-player Blokus mini game configuration. Test that the player
    can place two or more pieces before retiring. At each step before game over,
    verify that the values of game_over and curr_player are correct. After game
    over, verify the values of game_over, winners, and get_score(1).
    """

def test_two_player_blokus_mini_game() -> None:
    """
    Construct a 2-player Blokus mini game configuration. Test that each player
    can place two or more pieces before retiring. At each step before game over,
    verify that the values of game_over and curr_player are correct. After game
    over, verify the values of game_over, winners, get_score(1), and
    get_score(2).
    """
