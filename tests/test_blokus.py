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

    # Creating dict to track expected attributes of each shape
    # Expected squares based on origin (0, 0) and string representations
    expected_shapes: dict[ShapeKind, 
                    dict[str, bool | set[tuple[int, int]]]] = {
        ShapeKind.ONE: {"can_be_transformed": False, "squares": {(0, 0)}},
        ShapeKind.TWO: {"can_be_transformed": True, "squares": {(0, 0), 
                                                                (0, 1)}},
        ShapeKind.THREE: {"can_be_transformed": True, "squares": {(0, -1),
                                                        (0, 0), (0, 1)}},
        ShapeKind.C: {"can_be_transformed": True, "squares": {(0, 0), (0, 1),
                                                                    (1, 0)}}, 
        ShapeKind.FOUR: {"can_be_transformed": True, "squares": {(0, -1), 
                                                (0, 0), (0, 1), (0, 2)}}, 
        ShapeKind.SEVEN: {"can_be_transformed": True, "squares": {(-1, -1),
                                                    (-1, 0), (0, 0), (1, 0)}}, 
        ShapeKind.S: {"can_be_transformed": True, "squares": {(0, 0), (0, 1),
                                                            (1, -1), (1, 0)}}, 
        ShapeKind.LETTER_O: {"can_be_transformed": False, "squares": {(0, 0),
                                                    (0, 1), (1, 0), (1, 1)}}, 
        ShapeKind.A: {"can_be_transformed": True, "squares": {(-1, 0), (0, -1),
                                                            (0, 0), (0, 1)}}, 
        ShapeKind.F: {"can_be_transformed": True, "squares": {(-1, 0), (-1, 1),
                                                    (0, -1), (0, 0), (1, 0)}}, 
        ShapeKind.FIVE: {"can_be_transformed": True, "squares": {(-2, 0),
                                        (-1, 0), (0, 0), (1, 0), (2, 0)}},
        ShapeKind.L: {"can_be_transformed": True, "squares": {(-2, 0), (-1, 0),
                                                    (0, 0), (1, 0), (1, 1)}}, 
        ShapeKind.N: {"can_be_transformed": True, "squares": {(-1, 1), (0, 0),
                                                    (0, 1), (1, 0), (2, 0)}},                                                 
        ShapeKind.P: {"can_be_transformed": True, "squares": {(-1, -1), (-1, 0),
                                                    (0, -1), (0, 0), (1, -1)}}, 
        ShapeKind.T: {"can_be_transformed": True, "squares": {(-1, -1), (-1, 0),
                                                    (-1, 1), (0, 0), (1, 0)}}, 
        ShapeKind.U: {"can_be_transformed": True, "squares": {(-1, -1), (0, -1),
                                                    (0, 0), (0, 1), (-1, 1)}}, 
        ShapeKind.V: {"can_be_transformed": True, "squares": {(-1, 1), (0, 1),
                                                    (1, -1), (1, 0), (1, 1)}}, 
        ShapeKind.W: {"can_be_transformed": True, "squares": {(0, 2), (1, 1),
                                                    (1, 2), (2, 0), (2, 1)}},
        ShapeKind.X: {"can_be_transformed": True, "squares": {(-1, 1), (0, 0),
                                                    (0, 1), (1, -1), (1, 0)}}, 
        ShapeKind.Y: {"can_be_transformed": True, "squares": {(-1, 0), (0, -1),
                                                    (0, 0), (1, 0), (2, 0)}}, 
        ShapeKind.Z: {"can_be_transformed": True, "squares": {(-1, -1), (-1, 0),
                                                    (0, 0), (1, 0), (1, 1)}}                                                                                                                                                                                                                                                                                                                                             
    }

    for kind, exp in expected_shapes.items():
        shape = blokus.shapes[kind]
        assert shape.kind == kind
        assert shape.can_be_transformed == exp["can_be_transformed"]
        for square in shape.squares:
            assert square in exp["squares"]
    
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
    blokus = init_blokus_classic()

    # A few shapes for testing
    piece_two = Piece(blokus.shapes[ShapeKind.TWO])
    piece_five = Piece(blokus.shapes[ShapeKind.FIVE])
    piece_a = Piece(blokus.shapes[ShapeKind.A])
    piece_f = Piece(blokus.shapes[ShapeKind.F])

    neighbors_two = piece_two.cardinal_neighbors()
    assert neighbors_two == {(-1, 0), (-1, 1), (0, 2), (1, 0), (1, 1)
                             }, "Wrong cardinal neighbors for TWO"

    neighbors_five = piece_five.cardinal_neighbors()
    assert neighbors_five == {(-3, 0), (3, 0), # above and below
                              (-2, -1), (-1, -1), (0, -1), (1, -1), (2, -1), #L
                              (-2, 1), (-1, 1), (0, 1), (1, 1), (2, 1) #R
                              }, "Wrong cardinal neighbors for FIVE"

    neighbors_a = piece_a.cardinal_neighbors()
    assert neighbors_a == {(-2, 0), (1, -1), (1, 1), (0, -2), (0, 2)
                           },"Wrong cardinal neighbors for A" 

    neighbors_f = piece_f.cardinal_neighbors()
    assert neighbors_f == {(-2, 0), (-2, 1), # above 
                              (2, 0), 
                              (-1, -1), (0, -2), (1, -1), #L
                              (0, 1), (1, 1) #R
                              }, "Wrong cardinal neighbors for F"

def test_some_intercardinal_neighbors() -> None:
    """
    Construct an instance of any Blokus game configuration, and test that
    Piece.intercardinal_neighbors correctly computes the cardinal neighbors of
    at least three kinds of pieces.
    """
    blokus = init_blokus_classic()

    # A few shapes for testing
    piece_two = Piece(blokus.shapes[ShapeKind.TWO])
    piece_five = Piece(blokus.shapes[ShapeKind.FIVE])
    piece_a = Piece(blokus.shapes[ShapeKind.A])
    piece_f = Piece(blokus.shapes[ShapeKind.F])

    neighbors_two = piece_two.intercardinal_neighbors()
    assert neighbors_two == {(-1, -1), (-1, 1), (1, -1), (1, 1)
                             }, "Wrong intercardinal neighbors for TWO"

    neighbors_five = piece_five.intercardinal_neighbors()
    assert neighbors_five == {(-3, -1), (-3, 1), (3, -1), (3, 1)
                              }, "Wrong intercardinal neighbors for FIVE"

    neighbors_a = piece_a.intercardinal_neighbors()
    assert neighbors_a == {(-1, -1), (-1, 2), (1, 0)
                           },"Wrong intercardinal neighbors for A" 

    neighbors_f = piece_f.intercardinal_neighbors()
    assert neighbors_f == {(-2, 1), (-2, 2), (2, -1), (2, 1)
                              }, "Wrong intercardinal neighbors for F"

#test game runs
def test_one_player_blokus_mini_game() -> None:
    """
    Construct a 1-player Blokus mini game configuration. Test that the player
    can place two or more pieces before retiring. At each step before game over,
    verify that the values of game_over and curr_player are correct. After game
    over, verify the values of game_over, winners, and get_score(1).
    """
    blokus = test_init_blokus_mini_1()

    # Test playing 1st piece
    piece_one = Piece(blokus.shapes[ShapeKind.ONE])
    piece_one.set_anchor((0, 0)) 
    assert blokus.curr_player == 1
    assert blokus.maybe_place(piece_one) # P1 plays ONE at (0, 0)
    assert blokus.curr_player == 1
    assert not blokus.game_over

    # Test playing 2nd piece
    piece_two = Piece(blokus.shapes[ShapeKind.TWO])
    piece_two.set_anchor((1, 1)) 
    assert blokus.curr_player == 1
    assert blokus.maybe_place(piece_two) # P1 plays TWO at (1, 1)
    assert blokus.curr_player == 1
    assert not blokus.game_over

    # Test retiring
    blokus.retire()
    assert blokus.game_over
    assert blokus.winners == [1]
    assert blokus.get_score(1) == -88 # Starting with -89, played 1

def test_two_player_blokus_mini_game() -> None:
    """
    Construct a 2-player Blokus mini game configuration. Test that each player
    can place two or more pieces before retiring. At each step before game over,
    verify that the values of game_over and curr_player are correct. After game
    over, verify the values of game_over, winners, get_score(1), and
    get_score(2).
    """
    blokus = test_init_blokus_mini_2()

    # Test playing 1st piece
    piece_one = Piece(blokus.shapes[ShapeKind.ONE])
    piece_one.set_anchor((0, 0))
    assert blokus.curr_player == 1
    assert blokus.maybe_place(piece_one) # P1 plays ONE at (0, 0)
    assert blokus.curr_player == 2
    assert not blokus.game_over

    # Test playing 2nd piece
    piece_two = Piece(blokus.shapes[ShapeKind.TWO])
    # P2 cannot play TWO at (0, 0)
    piece_two.set_anchor((0, 0))
    assert not blokus.maybe_place(piece_two)
    # P2 can play TWO at (0, 1)
    piece_two.set_anchor((0, 1))
    assert blokus.curr_player == 2
    assert blokus.maybe_place(piece_two) # P2 plays TWO at (0, 1)
    assert blokus.curr_player == 1
    assert not blokus.game_over

    # Test retiring
    blokus.retire() # P1 retires
    assert blokus.curr_player == 2
    blokus.retire() # P2 retires

    assert blokus.game_over
    assert blokus.winners == [2]
    assert blokus.get_score(1) == -88
    assert blokus.get_score(2) == -87
