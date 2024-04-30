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
    blokus_mini = Blokus(1, 5, {(0, 0), (4, 4)})

    assert blokus_mini.size == 5
    assert blokus_mini.start_positions == {(0, 0), (4, 4)}
    assert blokus_mini.num_players == 1
    assert blokus_mini.curr_player == 1

    assert blokus_mini.grid #fill in

def test_init_blokus_mini_2() -> Blokus:
    """
    Construct an instance of a 2-player Blokus Mini game configuration. Verify
    that properties have been initialized correctly
    """

def test_init_blokus_mono() -> Blokus:
    """
    Construct an instance of a Blokus Mono game configuration. Verify
    that properties have been initialized correctly
    """

def test_init_blokus_duo_2() -> Blokus:
    """
    Construct an instance of a Blokus Duo game configuration. Verify
    that properties have been initialized correctly
    """

#test shape loading, flipping, rotating
def test_shapes_loaded() -> Blokus:
    """
    Construct an instance of any Blokus game configuration, and test that the
    shapes dictionary has been correctly initialized with all 21 Blokus shapes.
    """

def test_some_flipped_shapes() -> Blokus:
    """
    Construct an instance of any Blokus game configuration, and test that at
    least three kinds of shapes can be flipped correctly via the
    Shape.flip_horizontally method.
    """

def test_some_left_rotated_shapes() -> Blokus:
    """
    Construct an instance of any Blokus game configuration, and test that at
    least three kinds of shapes can be flipped correctly via the
    Shape.rotate_left method.
    """

def test_some_right_rotated_shapes() -> Blokus:
    """
    Construct an instance of any Blokus game configuration, and test that at
    least three kinds of shapes can be flipped correctly via the
    Shape.rotate_right method.
    """

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
