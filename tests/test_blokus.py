import pytest
from typing import Optional

from base import BlokusBase, Cell, Grid
from piece import Point, Shape, Piece
from shape_definitions import ShapeKind
from blokus import Blokus

########## Milestone 1 #########
# Test 0
def test_inheritance() -> None:
    """Test that Blokus inherits from BlokusBase."""
    assert issubclass(Blokus, BlokusBase), "Blokus must inherit from BlokusBase"

### Test initializations ###
# Test 1
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

    return blokus_mini_1

# Test 2
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

    return blokus_mini_2

# Test 3
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

    return blokus_mono

# Test 4
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

    return blokus_duo

## For testing purposes
def init_blokus_classic() -> Blokus:
    """"Initialize a 2-player Blokus Classic game configuration."""
    return Blokus(2, 20, {(0, 0), (0, 19), (19, 0), (19, 19)})

### Test shape loading, flipping, rotating ###
# Test 5
def test_shapes_loaded() -> None:
    """
    Construct an instance of any Blokus game configuration, and test that the
    shapes dictionary has been correctly initialized with all 21 Blokus shapes.
    """
    blokus = init_blokus_classic()

    # Creating dict to track expected attributes of each shape
    # Expected squares based on origin (0, 0) and string representations
    expected_shapes: dict[ShapeKind, 
                    dict[str, bool | set[Point]]] = {
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

# Test 6  
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

# Test 7
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

# Test 8
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

### Test neighbors ###
# Test 9
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

# Test 10
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

### Test game runs ###
# Test 11
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
    assert blokus.curr_player == 1, "curr_player should be 1"
    assert blokus.maybe_place(piece_one) # P1 plays ONE at (0, 0)
    assert blokus.curr_player == 1, "curr_player should be 1" 
    assert not blokus.game_over, "game should not be over"

    # Test playing 2nd piece
    piece_two = Piece(blokus.shapes[ShapeKind.TWO])
    piece_two.set_anchor((1, 1)) 
    assert blokus.curr_player == 1, "curr_player should be 1"
    assert blokus.maybe_place(piece_two) # P1 plays TWO at (1, 1)
    assert blokus.curr_player == 1, "curr_player should be 1"
    assert not blokus.game_over, "game should not be over"

    # Test retiring
    blokus.retire()
    assert blokus.game_over, "game should be over"
    assert blokus.winners == [1], "P1 should've won"
    assert blokus.get_score(1) == -88, "Score should be -88 for P1"

# Test 12
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
    assert blokus.curr_player == 1, "curr_player should be 1"
    assert blokus.maybe_place(piece_one) # P1 plays ONE at (0, 0)
    assert blokus.curr_player == 2, "curr_player should be 2"
    assert not blokus.game_over, "game should not be over"

    # Test playing 2nd piece
    piece_two = Piece(blokus.shapes[ShapeKind.TWO])
    # P2 cannot play TWO at (0, 0)
    piece_two.set_anchor((0, 0))
    assert not blokus.maybe_place(piece_two), "P2 cannot play TWO at (0, 0)"
    # P2 can play TWO at (0, 1)
    piece_two.set_anchor((0, 1))
    assert blokus.curr_player == 2, "curr_player should be 2"
    assert blokus.maybe_place(piece_two) # P2 plays TWO at (0, 1)
    assert blokus.curr_player == 1, "curr_player should be 1"
    assert not blokus.game_over, "game should not be over"

    # Test retiring
    blokus.retire() # P1 retires
    assert blokus.curr_player == 2, "curr_player should be 2"
    blokus.retire() # P2 retires

    assert blokus.game_over, "game should be over"
    assert blokus.winners == [2], "winner should be P2"
    assert blokus.get_score(1) == -88, "P1 score should be -88"
    assert blokus.get_score(2) == -87, "P2 score should be -87"

######### Milestone 2 #########

### Test exceptions ###
# Test 13
def test_exception_init():
    """
    Verify that four calls to the Blokus constructor each raise a ValueError,
    one for each of the four situations described in the docstring
    """ 
    with pytest.raises(ValueError):
        Blokus(0, 11, {(5,5)})  # num_players is less than 1
    with pytest.raises(ValueError):
        Blokus(5, 11, {(5,5)})  # num_players is more than 4

    with pytest.raises(ValueError):
        Blokus(1, 4, {(5,5)})  # size is less than 5
    
    with pytest.raises(ValueError):
        Blokus(1, 11, {(12,12)})  # not all start_positions are on the board

    with pytest.raises(ValueError):
        Blokus(2, 11, {(5,5)})  # fewer start_positions than num_players

# Test 14
def test_exception_place_already_played():
    """
    Create an instance of any Blokus game configuration. Verify that maybe_place
    raises a ValueError when trying to place an already played piece.
    """
    blokus = init_blokus_classic()
    piece_one = Piece(blokus.shapes[ShapeKind.ONE])
    piece_one.set_anchor((0, 0)) 
    blokus.maybe_place(piece_one) # P1 places ONE at (0, 0)

    piece_one.set_anchor((19, 19))
    blokus.maybe_place(piece_one) # P2 places ONE at (19, 19)

    piece_one.set_anchor((1, 1)) 
    with pytest.raises(ValueError): # P1 can't place ONE again
       blokus.maybe_place(piece_one) 

# Test 15
def test_exception_place_without_anchor():
    """
    Create an instance of any Blokus game configuration. Verify that maybe_place
    raises a ValueError when trying to place a piece without an anchor.
    """
    blokus = init_blokus_classic()
    with pytest.raises(ValueError): # no call to set_anchor
       blokus.maybe_place(Piece(blokus.shapes[ShapeKind.THREE])) 

### Test start positions ###
# Test 16
def test_start_positions_1():
    """
    Create an instance of any 1-player Blokus game configuration with one start
    position. Verify that maybe_place will not place a piece that does not cover
    the start position. Then verify that maybe_place will place a piece that
    does cover the start position, and that the player can place a second piece
    on the board.
    """
    blokus = test_init_blokus_mono() # (5, 5) is the only start position
    piece_one = Piece(blokus.shapes[ShapeKind.ONE])
    piece_one.set_anchor((0, 0)) # not valid start position
    assert not blokus.maybe_place(piece_one), "Can't play piece not at start"
    
    piece_one.set_anchor((5, 5))
    assert blokus.maybe_place(piece_one), "Should be able to play piece at strt"

    piece_two = Piece(blokus.shapes[ShapeKind.TWO])
    piece_two.set_anchor((6, 6))
    assert blokus.maybe_place(piece_two), "Should be able to play 2nd piece"

# Test 17
def test_start_positions_2():
    """
    Create an instance of any 2-player Blokus game configuration with two start
    positions. Verify that Player 1 cannot place a piece which does not cover a
    start position, before then playing a piece which does. Then verify that
    Player 2 cannot place a piece that does not cover a start position nor one
    that covers only the already covered start position. Then verify that Player
    2 can cover the remaining start position. After all that, verify that Player
    1 and Player 2 can each play another piece.
    (This sequence involves four placed pieces in total.)
    """
    blokus = test_init_blokus_duo_2()
    piece_one = Piece(blokus.shapes[ShapeKind.ONE])
    piece_one.set_anchor((1, 1)) # Not valid start position
    assert blokus.curr_player == 1
    assert not blokus.maybe_place(piece_one), "P1 can't play piece not at start"
    
    piece_one.set_anchor((4, 4))
    assert blokus.maybe_place(piece_one), (
        "P1 should be able to play piece at start position (4, 4)"
    )
    # P1 played ONE at (4, 4)
    
    assert blokus.curr_player == 2
    assert not blokus.maybe_place(piece_one), "P2 can't cover alr covered strt"
    piece_one.set_anchor((1, 1))
    assert not blokus.maybe_place(piece_one), "P2 can't play piece not at start"

    piece_one.set_anchor((9, 9))
    assert blokus.maybe_place(piece_one), (
        "P2 should be able to play piece at start position (9, 9)"
    )
    # P2 played ONE at (9, 9)
    assert blokus.curr_player == 1 
    piece_two = Piece(blokus.shapes[ShapeKind.TWO])
    piece_two.set_anchor((5, 5))
    assert blokus.maybe_place(piece_two), "P1 should be able to play 2nd piece"
    # P1 played TWO at (5, 5)

    assert blokus.curr_player == 2
    piece_two.set_anchor((8, 7))
    assert blokus.maybe_place(piece_two), "P2 should be able to play 2nd piece"
    # P2 played TWO at (8, 7)

# Test 18
def test_start_positions_3():
    """
    Same as the previous test, except the game board has four start positions
    rather than two.
    """
    blokus = init_blokus_classic()
    piece_one = Piece(blokus.shapes[ShapeKind.ONE])
    piece_one.set_anchor((1, 1)) # Not valid start position
    assert blokus.curr_player == 1
    assert not blokus.maybe_place(piece_one), "P1 can't play piece not at start"
    
    piece_one.set_anchor((0, 0))
    assert blokus.maybe_place(piece_one), (
        "P1 should be able to play piece at start position (0, 0)"
    )
    # P1 played ONE at (0, 0)
    
    assert blokus.curr_player == 2
    assert not blokus.maybe_place(piece_one), "P2 can't cover alr covered strt"
    piece_one.set_anchor((1, 1))
    assert not blokus.maybe_place(piece_one), "P2 can't play piece not at start"

    piece_one.set_anchor((19, 19))
    assert blokus.maybe_place(piece_one), (
        "P2 should be able to play piece at start position (19, 19)"
    )
    # P2 played ONE at (19, 19)
    assert blokus.curr_player == 1 
    piece_two = Piece(blokus.shapes[ShapeKind.TWO])
    piece_two.set_anchor((1, 1))
    assert blokus.maybe_place(piece_two), "P1 should be able to play 2nd piece"
    # P1 played TWO at (1, 1)

    assert blokus.curr_player == 2
    piece_two.set_anchor((18, 17))
    assert blokus.maybe_place(piece_two), "P2 should be able to play 2nd piece"
    # P2 played TWO at (18, 17)

### Test shape flips and rotations ###
# Test 19
def test_place_flipped_shape_1():
    """
    Create an instance of any 1-player Blokus game config. Choose a piece,
    anchor it somewhere, flip it, and verify that its squares() are correct.
    Then place the piece, and verify that grid stores the correct values for
    every cell in the matrix.
    """
    blokus = test_init_blokus_mono()
    piece_four = Piece(blokus.shapes[ShapeKind.FOUR])
    piece_four.set_anchor(5, 5)
    piece_four.flip_horizontally()
    expected_squares = [(5, 3), (5, 4), (5, 5), (5, 6)]
    assert piece_four.squares() == expected_squares, (
        "Squares of piece_four incorrect after flipping"
    )

    blokus.maybe_place(piece_four)
    # Check grid stores correct values for cells filled by FOUR
    for r, c in expected_squares:
        assert blokus.grid[r][c] == (1, ShapeKind.FOUR), (
            f"Grid at ({r}, {c}) should be (1, ShapeKind.FOUR)"
        )
    # Check grid correctly stores None for all other cells
    for r in range(len(blokus.grid)):
        for c in range(len(blokus.grid[0])):
            if (r, c) not in expected_squares:
                assert blokus.grid[r][c] is None, (
                    f"Grid at ({r}, {c}) should be empty"
                )

# Test 20
def test_rotated_shape_1():
    """
    Same as the previous, except for a shape that is rotated once (90 degrees)
    to the right.
    """
    blokus = test_init_blokus_mono()
    piece_four = Piece(blokus.shapes[ShapeKind.FOUR])
    piece_four.set_anchor(5, 5)
    piece_four.rotate_right()
    expected_squares = [(4, 5), (5, 5), (6, 5), (7, 5)]
    assert piece_four.squares() == expected_squares, (
        "Squares of piece_four incorrect after rotating R once"
    )

    blokus.maybe_place(piece_four)
    # Check grid stores correct values for cells filled by FOUR
    for r, c in expected_squares:
        assert blokus.grid[r][c] == (1, ShapeKind.FOUR), (
            f"Grid at ({r}, {c}) should be (1, ShapeKind.FOUR)"
        )
    # Check grid correctly stores None for all other cells
    for r in range(len(blokus.grid)):
        for c in range(len(blokus.grid[0])):
            if (r, c) not in expected_squares:
                assert blokus.grid[r][c] is None, (
                    f"Grid at ({r}, {c}) should be empty"
                )

# Test 21
def test_rotated_shape_2():
    """
    Same as the previous, except for a shape that is rotated twice (180 degrees)
    to the right.
    """
    blokus = test_init_blokus_mono()
    piece_four = Piece(blokus.shapes[ShapeKind.FOUR])
    piece_four.set_anchor(5, 5)
    piece_four.rotate_right()
    piece_four.rotate_right() # Rotate R twice
    expected_squares = [(5, 3), (5, 4), (5, 5), (5, 6)]
    assert piece_four.squares() == expected_squares, (
        "Squares of piece_four incorrect after rotating R twice"
    )

    blokus.maybe_place(piece_four)
    # Check grid stores correct values for cells filled by FOUR
    for r, c in expected_squares:
        assert blokus.grid[r][c] == (1, ShapeKind.FOUR), (
            f"Grid at ({r}, {c}) should be (1, ShapeKind.FOUR)"
        )
    # Check grid correctly stores None for all other cells
    for r in range(len(blokus.grid)):
        for c in range(len(blokus.grid[0])):
            if (r, c) not in expected_squares:
                assert blokus.grid[r][c] is None, (
                    f"Grid at ({r}, {c}) should be empty"
                )

# Test 22
def test_flipped_and_rotated_shape_1():
    """
    Same as the previous, except for a shape that is flipped and then rotated
    three times (270 degrees) to the right.
    """
    blokus = test_init_blokus_mono()
    piece_four = Piece(blokus.shapes[ShapeKind.FOUR])
    piece_four.set_anchor(5, 5)
    piece_four.flip_horizontally() # Flip first
    for _ in range(3): # Then rotate R three times
        piece_four.rotate_right()
    expected_squares = [(4, 5), (5, 5), (6, 5), (7, 5)]
    assert piece_four.squares() == expected_squares, (
        "Squares of piece_four incorrect after flipping and rotating R 3 times"
    )

    blokus.maybe_place(piece_four)
    # Check grid stores correct values for cells filled by FOUR
    for r, c in expected_squares:
        assert blokus.grid[r][c] == (1, ShapeKind.FOUR), (
            f"Grid at ({r}, {c}) should be (1, ShapeKind.FOUR)"
        )
    # Check grid correctly stores None for all other cells
    for r in range(len(blokus.grid)):
        for c in range(len(blokus.grid[0])):
            if (r, c) not in expected_squares:
                assert blokus.grid[r][c] is None, (
                    f"Grid at ({r}, {c}) should be empty"
                )

# Test 23
def test_flipped_and_rotated_shape_2():
    """
    Same as the previous, except for a shape that is flipped twice and then
    rotated four times (360 degrees) to the right.
    """
    blokus = test_init_blokus_mono()
    piece_four = Piece(blokus.shapes[ShapeKind.FOUR])
    piece_four.set_anchor(5, 5)
    piece_four.flip_horizontally()
    piece_four.flip_horizontally() # Flipping twice will go back to OG
    for _ in range(4): # Rotate R four times will go back to OG
        piece_four.rotate_right()
    expected_squares = [(5, 4), (5, 5), (5, 6), (5, 7)] #same as OG
    assert piece_four.squares() == expected_squares, (
        "Squares of piece_four incorrect after flipping twice and rotating R"
        "four times"
    )

    blokus.maybe_place(piece_four)
    # Check grid stores correct values for cells filled by FOUR
    for r, c in expected_squares:
        assert blokus.grid[r][c] == (1, ShapeKind.FOUR), (
            f"Grid at ({r}, {c}) should be (1, ShapeKind.FOUR)"
        )
    # Check grid correctly stores None for all other cells
    for r in range(len(blokus.grid)):
        for c in range(len(blokus.grid[0])):
            if (r, c) not in expected_squares:
                assert blokus.grid[r][c] is None, (
                    f"Grid at ({r}, {c}) should be empty"
                )

### Test edges and corners ###
# Test 24
def test_prevent_own_edges_1():
    """
    Create an instance of any 1-player Blokus game configuration. After placing
    a piece, verify that the player cannot place another piece that shares an
    edge with their first played piece.
    """
    blokus = test_init_blokus_mono()

    assert blokus.curr_player == 1
    piece_one = Piece(blokus.shapes[ShapeKind.ONE])
    piece_one.set_anchor((5, 5))
    assert blokus.maybe_place(piece_one), (
        "P1 should be able to play ONE at (5, 5)"
    )

    piece_two = Piece(blokus.shapes[ShapeKind.TWO])
    piece_two.set_anchor((5, 6)) # Touching edge of ONE
    assert not blokus.maybe_place(piece_two), (
        "P1 should not be able to play TWO touching edge of ONE"
    )

# Test 25
def test_prevent_own_edges_2():
    """
    Create an instance of any 2-player Blokus game configuration. After Player 1
    and Player 2 each play a piece, verify that Player 1 cannot play a piece
    that shares an edge with their first played piece; Player 1 should then play
    a legal piece. Verify that Player 2 cannot play a piece that shares an edge
    with their first played piece; Player 2 should then play a legal piece.
    Verify that Player 1 can play a piece that shares one or more edges with
    Player 2s pieces, and vice versa. (This sequence involves six placed pieces
    in total.)
    """
    blokus = test_init_blokus_duo_2()

    # Piece 1: P1 plays ONE at (4, 4)
    assert blokus.curr_player == 1
    piece_one = Piece(blokus.shapes[ShapeKind.ONE])
    piece_one.set_anchor((4, 4))
    assert blokus.maybe_place(piece_one), (
        "P1 should be able to play ONE at (4, 4)"
    )

    # Piece 2: P2 plays ONE at (9, 9)
    assert blokus.curr_player == 2
    piece_one.set_anchor((9, 9))
    assert blokus.maybe_place(piece_one), (
        "P2 should be able to play ONE at (9, 9)"
    )

    # P1 cannot play TWO at (4, 5)
    piece_two = Piece(blokus.shapes[ShapeKind.TWO])
    piece_two.set_anchor((4, 5)) # Touching edge of ONE
    assert not blokus.maybe_place(piece_two), (
        "P1 should not be able to play TWO touching edge of ONE"
    )

    # Piece 3: P1 plays TWO at (5, 5)
    piece_two.set_anchor((5, 5)) # Touching edge of ONE
    assert blokus.maybe_place(piece_two), (
        "P1 should be able to play TWO at (5, 5)"
    )

    # P2 cannot play TWO at (8, 8)
    assert blokus.curr_player == 2
    piece_two.set_anchor((8, 8))
    assert not blokus.maybe_place(piece_two), (
        "P2 should not be able to play TWO touching edge of ONE"
    )

    # Piece 4: P2 plays TWO at (8, 7)
    piece_two.set_anchor((8, 7)) # Touching edge of ONE
    assert blokus.maybe_place(piece_two), (
        "P1 should be able to play TWO at (8, 7)"
    )

    # Piece 5: P1 plays U at (7, 8) touching P2's TWO
    assert blokus.curr_player == 1
    piece_u = Piece(blokus.shapes[ShapeKind.U])
    piece_u.set_anchor((7, 8))
    assert blokus.maybe_place(piece_u), (
        "P1 should be able to play U at (7, 8) touching P2's TWO"
    )

    # Piece 6: P2 plays FIVE at (6, 10) touching P1's U
    assert blokus.curr_player == 2
    piece_five = Piece(blokus.shapes[ShapeKind.FIVE])
    piece_five.set_anchor((6, 10))
    assert blokus.maybe_place(piece_five), (
        "P2 should be able to play U at (6, 10) touching P1's U"
    )

# Test 26
def test_require_own_corners_1():
    """
    Analogous to above but requiring own-corners rather than preventing
    own-edges:
    Create an instance of any 1-player Blokus game configuration. After placing
    a piece, verify that the player cannot place another piece that shares zero
    corners with their first played piece.
    """
    blokus = test_init_blokus_mono()

    piece_one = Piece(blokus.shapes[ShapeKind.ONE])
    piece_one.set_anchor((5, 5))
    assert blokus.maybe_place(piece_one), (
        "P1 should be able to play ONE at (5, 5)"
    )

    piece_two = Piece(blokus.shapes[ShapeKind.TWO])
    piece_two.set_anchor((7, 7))
    assert not blokus.maybe_place(piece_two), (
        "P1 cannot play TWO that shares zero corners with ONE"
    )

# Test 27
def test_require_own_corners_2():
    """
    Analogous to above but requiring own-corners rather than preventing
    own-edges:
    Create an instance of any 2-player Blokus game configuration. After Player 1
    and Player 2 each play a piece, verify that Player 1 cannot play a piece
    that shares zero corners with their first played piece; Player 1 should then
    play a legal piece. Verify that Player 2 cannot play a piece that shares
    zero corners with their first played piece; Player 2 should then play a
    legal piece. Verify that Player 1 can play a piece that shares zero corners
    with Player 2s pieces, and vice versa. (In sum, this sequence involves six
    placed pieces.)
    """
    blokus = test_init_blokus_duo_2()

    # Piece 1: P1 plays ONE at (4, 4)
    assert blokus.curr_player == 1
    piece_one = Piece(blokus.shapes[ShapeKind.ONE])
    piece_one.set_anchor((4, 4))
    assert blokus.maybe_place(piece_one), (
        "P1 should be able to play ONE at (4, 4)"
    )

    # Piece 2: P2 plays ONE at (9, 9)
    assert blokus.curr_player == 2
    piece_one.set_anchor((9, 9))
    assert blokus.maybe_place(piece_one), (
        "P2 should be able to play ONE at (9, 9)"
    )

    # P1 cannot play TWO at (6, 6)
    piece_two = Piece(blokus.shapes[ShapeKind.TWO])
    piece_two.set_anchor((6, 6)) # No corners with ONE
    assert not blokus.maybe_place(piece_two), (
        "P1 should not be able to play TWO sharing zero corners with ONE"
    )

    # Piece 3: P1 plays TWO at (5, 5)
    piece_two.set_anchor((5, 5)) # Touching edge of ONE
    assert blokus.maybe_place(piece_two), (
        "P1 should be able to play TWO at (5, 5)"
    )

    # P2 cannot play TWO at (7, 7)
    assert blokus.curr_player == 2
    piece_two.set_anchor((7, 7))
    assert not blokus.maybe_place(piece_two), (
        "P2 should not be able to play TWO sharing zero corners with ONE"
    )

    # Piece 4: P2 plays TWO at (8, 7)
    piece_two.set_anchor((8, 7)) # Touching edge of ONE
    assert blokus.maybe_place(piece_two), (
        "P1 should be able to play TWO at (8, 7)"
    )

    # Piece 5: P1 plays T at (3, 7), no corners with P2
    assert blokus.curr_player == 1
    piece_t = Piece(blokus.shapes[ShapeKind.T])
    piece_t.set_anchor((3, 7))
    assert blokus.maybe_place(piece_t), (
        "P1 should be able to play T at (3, 7) w/o sharing corners w/ P2"
    )

    # Piece 6: P2 plays T at (9, 11), no corners with P1
    assert blokus.curr_player == 2
    piece_t.set_anchor((9, 11))
    assert blokus.maybe_place(piece_t), (
        "P2 should be able to play T at (9, 11)w/o sharing corners w/ P1"
    )

### Test available moves ###
# Test 28
def test_some_available_moves():
    """
    Create an instance of any Blokus game configuration. Verify that
    available_moves is non-empty. Play a few pieces, and verify that the number
    of available_moves decreases after each step.
    """
    blokus = test_init_blokus_mono()
    assert blokus.available_moves != {}, "available_moves should not be empty"
    cur_length = len(blokus.available_moves) #initialize cur_length

    # Piece 1: P1 plays ONE at (5, 5)
    piece_one = Piece(blokus.shapes[ShapeKind.ONE])
    piece_one.set_anchor((5, 5))
    assert blokus.maybe_place(piece_one), (
        "P1 should be able to play ONE at (5, 5)"
    )
    assert len(blokus.available_moves) < cur_length, (
        "available_moves should be decreasing after playing piece ONE"
    )
    cur_length = len(blokus.available_moves) #update cur_length

    # Piece 2: P1 plays TWO at (6, 6)
    piece_two = Piece(blokus.shapes[ShapeKind.TWO])
    piece_two.set_anchor((6, 6))
    assert blokus.maybe_place(piece_two), (
        "P1 should be able to play TWO at (6, 6)"
    )
    assert len(blokus.available_moves) < cur_length, (
        "available_moves should be decreasing after playing piece TWO"
    )
    cur_length = len(blokus.available_moves) #update cur_length

    # Piece 3: P1 plays THREE at (7, 8)
    piece_three = Piece(blokus.shapes[ShapeKind.THREE])
    piece_three.set_anchor((7, 8))
    assert blokus.maybe_place(piece_three), (
        "P1 should be able to play THREE at (7, 8)"
    )
    assert len(blokus.available_moves) < cur_length, (
        "available_moves should be decreasing after playing piece THREE"
    )

# Test 29
def test_no_available_moves():
    """
    Create an instance of any Blokus game configuration. Play pieces until there
    are no more available moves, and verify that available_moves is empty.
    """
    blokus = test_init_blokus_mini_1()
    assert blokus.available_moves(), (
        "available_moves should not be empty at game start"
    )
    # P1 places Z at (1, 1)
    piece_z = Piece(blokus.shapes[ShapeKind.Z])
    piece_z.set_anchor((1, 1))
    assert blokus.maybe_place(piece_z), (
        "P1 should be able to play Z at (1, 1)"
    )

    # P1 places C at (0, 3)
    piece_c = Piece(blokus.shapes[ShapeKind.C])
    piece_c.set_anchor((0, 3))
    assert blokus.maybe_place(piece_c), (
        "P1 should be able to play C at (0, 3)"
    )

    # Rotate R THREE then P1 places THREE at (3, 4)
    piece_three = Piece(blokus.shapes[ShapeKind.THREE])
    piece_three.rotate_right()
    piece_three.set_anchor((3, 4))
    assert blokus.maybe_place(piece_three), (
        "P1 should be able to play rotated R THREE at (3, 4)"
    )

    # Rotate R TWO then P1 places TWO at (3, 0)
    piece_two = Piece(blokus.shapes[ShapeKind.TWO])
    piece_two.rotate_right()
    piece_two.set_anchor((3, 0))
    assert blokus.maybe_place(piece_two), (
        "P1 should be able to play rotated R TWO at (3, 0)"
    )

    # There should be no more legal moves logically
    assert not blokus.available_moves(), "Should be no available moves left"

### Test X points ###
# Test 30
def test_15_points():
    """
    Simulate a game where a player scores 15 points, that is, plays all 21 of
    their pieces! You can do this for any game configuration you like. After all
    21 pieces are played, then — either right away, or after other players, if
    any, continue playing — verify the expected values for get_score(),
    game_over, winners, and remaining_shapes.

    Note: The last three tests in test_fake.py may provide some inspiration for
    strategizing how to test such long sequences of moves.
    """

# Test 31
def test_20_points():
    """
    Same as above, but where a player scores 20 points, that is, plays all 21
    pieces with ONE as the last piece played.
    Note: The sequence of moves in this test can be very similar to the previous
    test. If so, factor your code in a way that avoids a giant amount of
    copy-pasted code.
    """
