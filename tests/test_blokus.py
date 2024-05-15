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
    blokus_mini_1 = Blokus(1, 5, {(0, 0), (4, 4)})

    assert blokus_mini_1.size == 5
    assert blokus_mini_1.start_positions == {(0, 0), (4, 4)}
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
    blokus_mini_2 = Blokus(2, 5, {(0, 0), (4, 4)})

    assert blokus_mini_2.size == 5
    assert blokus_mini_2.start_positions == {(0, 0), (4, 4)}
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
        ShapeKind.W: {"can_be_transformed": True, "squares": {(-1, 1), (0, 0),
                                                    (0, 1), (1, -1), (1, 0)}},
        ShapeKind.X: {"can_be_transformed": True, "squares": {(-1, 0), (0, 0),
                                                    (1, 0), (0, -1), (0, 1)}}, 
        ShapeKind.Y: {"can_be_transformed": True, "squares": {(-1, 0), (0, -1),
                                                    (0, 0), (1, 0), (2, 0)}}, 
        ShapeKind.Z: {"can_be_transformed": True, "squares": {(-1, -1), (-1, 0),
                                                    (0, 0), (1, 0), (1, 1)}}                                                                                                                                                                                                                                                                                                                                             
    }

    for kind, exp in expected_shapes.items():
        shape = blokus.shapes[kind]
        assert shape.kind == kind, (
            f"shape.kind: {shape.kind} should be same as kind: [{kind}]"
        )
        assert shape.can_be_transformed == exp["can_be_transformed"], (
            f"{shape.can_be_transformed} should be {exp['can_be_transformed']}"
        )
        for square in shape.squares:
            assert square in exp["squares"], (
                f"for shape.kind: {shape.kind}"
                f"square: {square} should be in expected squares:"
                f"{exp['squares']}"
            )
## Test pieces to reduce repeated code
def test_pieces_two_five_a_f() -> list[Piece]:
    """A few shapes for testing: TWO, FIVE, A, F"""
    blokus = init_blokus_classic()
    return [
       Piece(blokus.shapes[ShapeKind.TWO]),
       Piece(blokus.shapes[ShapeKind.FIVE]),
       Piece(blokus.shapes[ShapeKind.A]),
       Piece(blokus.shapes[ShapeKind.F])
    ]

# Test 6  
def test_some_flipped_shapes() -> Blokus:
    """
    Construct an instance of any Blokus game configuration, and test that at
    least three kinds of shapes can be flipped correctly via the
    Shape.flip_horizontally method.
    """
    # Expected squares in order TWO, FIVE, A, and F
    expected_squares: list[set[Point]] = [
        {(0, -1), (0, 0)}, # for TWO
        {(-2, 0), (-1, 0), (0, 0), (1, 0), (2, 0)}, # for FIVE
        {(-1, 0), (0, -1), (0, 0), (0, 1)}, # for A
        {(-1, -1), (-1, 0), (0, 0), (0, 1), (1, 0)}, # for F
    ]

    for i, piece in enumerate(test_pieces_two_five_a_f()):
        piece.set_anchor((0, 0))
        piece.flip_horizontally()
        for square in piece.squares():
            assert square in expected_squares[i]

# Test 7
def test_some_left_rotated_shapes() -> Blokus:
    """
    Construct an instance of any Blokus game configuration, and test that at
    least three kinds of shapes can be flipped correctly via the
    Shape.rotate_left method.
    """
    # Expected squares in order TWO, FIVE, A, and F
    expected_squares: list[set[Point]] = [
        {(0, 0), (-1, 0)}, # for TWO
        {(0, 2), (0, 1), (0, 0), (0, -1), (0, -2)}, # for FIVE
        {(0, -1), (1, 0), (0, 0), (-1, 0)}, # for A
        {(0, -1), (-1, -1), (1, 0), (0, 0), (0, 1)}, # for F
    ]
    for i, piece in enumerate(test_pieces_two_five_a_f()):
        piece.set_anchor((0, 0))
        piece.rotate_left()
        for square in piece.squares():
            assert square in expected_squares[i]

# Test 8
def test_some_right_rotated_shapes() -> Blokus:
    """
    Construct an instance of any Blokus game configuration, and test that at
    least three kinds of shapes can be flipped correctly via the
    Shape.rotate_right method.
    """
    # Expected squares in order TWO, FIVE, A, and F
    expected_squares: list[set[Point]] = [
        {(0, 0), (1, 0)}, # for TWO
        {(0, -2), (0, -1), (0, 0), (0, 1), (0, 2)}, # for FIVE
        {(0, 1), (-1, 0), (0, 0), (1, 0)}, # for A
        {(0, 1), (1, 1), (-1, 0), (0, 0), (0, -1)}, # for F
    ]
    for i, piece in enumerate(test_pieces_two_five_a_f()):
        piece.set_anchor((0, 0))
        piece.rotate_right()
        for square in piece.squares():
            assert square in expected_squares[i]

### Test neighbors ###
# Test 9
def test_some_cardinal_neighbors() -> None:
    """
    Construct an instance of any Blokus game configuration, and test that
    Piece.cardinal_neighbors correctly computes the cardinal neighbors of at
    least three kinds of pieces.
    """
    # Expected neighbors in order TWO, FIVE, A, and F
    expected_nbs: list[set[Point]] = [
        {(-1, 0), (-1, 1), (0, 2), (1, 0), (1, 1), (0, -1)}, # for TWO
        {(-3, 0), (3, 0), # for FIVE, above and below
        (-2, -1), (-1, -1), (0, -1), (1, -1), (2, -1), #L
            (-2, 1), (-1, 1), (0, 1), (1, 1), (2, 1)}, # R
        {(-2, 0), (-1, -1), (-1, 1), (0, -2), (0, 2),
                            (1, -1), (1, 0), (1, 1)}, # for A
        {(-2, 0), (-2, 1), (-1, -1), (-1, 2), (0, -2), (0, 1),
                            (1, -1), (2, 0), (1, 1)}, # for F
    ]
    for i, piece in enumerate(test_pieces_two_five_a_f()):
        piece.set_anchor((0, 0))
        assert piece.cardinal_neighbors() == expected_nbs[i]

# Test 10
def test_some_intercardinal_neighbors() -> None:
    """
    Construct an instance of any Blokus game configuration, and test that
    Piece.intercardinal_neighbors correctly computes the cardinal neighbors of
    at least three kinds of pieces.
    """
    # Expected neighbors in order TWO, FIVE, A, and F
    expected_nbs: list[set[Point]] = [
        {(-1, -1), (-1, 2), (1, -1), (1, 2)}, # for TWO
        {(-3, -1), (-3, 1), (3, -1), (3, 1)}, # for FIVE,
        {(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2)}, # for A
        {(-2, -1), (-2, 2), (-1, -2), (0, 2), (1, -2), (2, -1), (2, 1)}, #for F
    ]
    for i, piece in enumerate(test_pieces_two_five_a_f()):
        piece.set_anchor((0, 0))
        assert piece.intercardinal_neighbors() == expected_nbs[i]

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
    assert blokus.get_score(1) == -86, "Score should be -86 for P1"

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

    # Piece 1: P1 plays ONE at (0, 0)
    piece_one = Piece(blokus.shapes[ShapeKind.ONE])
    piece_one.set_anchor((0, 0))
    assert blokus.curr_player == 1, "curr_player should be 1"
    assert blokus.maybe_place(piece_one), "P1 can play ONE at (0, 0)"
    assert blokus.curr_player == 2, "curr_player should be 2"
    assert not blokus.game_over, "game should not be over"

    # Piece 2: P2 plays ONE at (4, 4)
    piece_one.set_anchor((4, 4))
    assert blokus.curr_player == 2, "curr_player should be 2"
    assert blokus.maybe_place(piece_one), "P2 can play ONE at (4, 4)"
    assert blokus.curr_player == 1, "curr_player should be 1"
    assert not blokus.game_over, "game should not be over"

    # Piece 3: P1 plays TWO at (1, 1)
    piece_two = Piece(blokus.shapes[ShapeKind.TWO])
    piece_two.set_anchor((1, 1))
    assert blokus.curr_player == 1, "curr_player should be 1"
    assert blokus.maybe_place(piece_two), "P1 can play TWO at (1, 1)"
    assert blokus.curr_player == 2, "curr_player should be 2"
    assert not blokus.game_over, "game should not be over"

    # Piece 4: P2 plays THREE at (3, 2)
    piece_three = Piece(blokus.shapes[ShapeKind.THREE])
    piece_three.set_anchor((3, 2))
    assert blokus.curr_player == 2, "curr_player should be 2"
    assert blokus.maybe_place(piece_three), "P2 can play THREE at (3, 2)"
    assert blokus.curr_player == 1, "curr_player should be 1"
    assert not blokus.game_over, "game should not be over"

    # Test retiring
    blokus.retire() # P1 retires
    assert blokus.curr_player == 2, "curr_player should be 2"
    blokus.retire() # P2 retires

    assert blokus.game_over, "game should be over"
    assert blokus.winners == [2], "winner should be P2"
    assert blokus.get_score(1) == -86, "P1 score should be -86"
    assert blokus.get_score(2) == -85, "P2 score should be -85"

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
    piece_two = Piece(blokus.shapes[ShapeKind.TWO])
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
    piece_four.set_anchor((5, 5))
    piece_four.flip_horizontally()
    expected_squares = {(5, 3), (5, 4), (5, 5), (5, 6)}
    for square in piece_four.squares():
        assert square in expected_squares, (
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
    piece_four.set_anchor((5, 5))
    piece_four.rotate_right()
    expected_squares = {(4, 5), (5, 5), (6, 5), (7, 5)}
    for square in piece_four.squares():
        assert square in expected_squares, (
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
    piece_four.set_anchor((5, 5))
    piece_four.rotate_right()
    piece_four.rotate_right() # Rotate R twice
    expected_squares = {(5, 3), (5, 4), (5, 5), (5, 6)}
    for square in piece_four.squares():
        assert square in expected_squares, (
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
    piece_four.set_anchor((5, 5))
    piece_four.flip_horizontally() # Flip first
    for _ in range(3): # Then rotate R three times
        piece_four.rotate_right()
    expected_squares = {(4, 5), (5, 5), (6, 5), (7, 5)}
    for square in piece_four.squares():
        assert square in expected_squares, (
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
    piece_four.set_anchor((5, 5))
    piece_four.flip_horizontally()
    piece_four.flip_horizontally() # Flipping twice will go back to OG
    for _ in range(4): # Rotate R four times will go back to OG
        piece_four.rotate_right()
    expected_squares = {(5, 4), (5, 5), (5, 6), (5, 7)} #same as OG
    for square in piece_four.squares():
        assert square in expected_squares, (
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
    assert blokus.available_moves() != {}, "available_moves should not be empty"
    cur_length = len(blokus.available_moves()) #initialize cur_length

    # Piece 1: P1 plays ONE at (5, 5)
    piece_one = Piece(blokus.shapes[ShapeKind.ONE])
    piece_one.set_anchor((5, 5))
    assert blokus.maybe_place(piece_one), (
        "P1 should be able to play ONE at (5, 5)"
    )
    assert len(blokus.available_moves()) < cur_length, (
        "available_moves should be decreasing after playing piece ONE"
    )
    cur_length = len(blokus.available_moves()) #update cur_length

    # Piece 2: P1 plays TWO at (6, 6)
    piece_two = Piece(blokus.shapes[ShapeKind.TWO])
    piece_two.set_anchor((6, 6))
    assert blokus.maybe_place(piece_two), (
        "P1 should be able to play TWO at (6, 6)"
    )
    assert len(blokus.available_moves()) < cur_length, (
        "available_moves should be decreasing after playing piece TWO"
    )
    cur_length = len(blokus.available_moves()) #update cur_length

    # Piece 3: P1 plays THREE at (7, 8)
    piece_three = Piece(blokus.shapes[ShapeKind.THREE])
    piece_three.set_anchor((7, 8))
    assert blokus.maybe_place(piece_three), (
        "P1 should be able to play THREE at (7, 8)"
    )
    assert len(blokus.available_moves()) < cur_length, (
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
    piece_three.set_anchor((3, 4))
    piece_three.rotate_right()
    assert blokus.maybe_place(piece_three), (
        "P1 should be able to play rotated R THREE at (3, 4)"
    )

    # Rotate R TWO then P1 places TWO at (3, 0)
    piece_two = Piece(blokus.shapes[ShapeKind.TWO])
    piece_two.set_anchor((3, 0))
    piece_two.rotate_right()
    assert blokus.maybe_place(piece_two), (
        "P1 should be able to play rotated R TWO at (3, 0)"
    )

    # There should be no more legal moves logically
    assert blokus.available_moves() == set(), "Should be no available moves left"

### Test X points ###
## Helper to avoid repeated code for Tests 30 and 31
def fill_grid_except_last_two() -> Blokus:
    """
    Constructs an instance of Blokus Duo. Each player places pieces until P1 has
    placed 19 pieces and is about to play their last two pieces and win.
    """
    blokus = test_init_blokus_duo_2()

    # Piece 1: P1 plays flipped F at (4, 4)
    assert blokus.curr_player == 1
    piece_f = Piece(blokus.shapes[ShapeKind.F])
    piece_f.set_anchor((4, 4))
    piece_f.flip_horizontally()
    assert blokus.maybe_place(piece_f), "Issue with piece 1"

    # Piece 2: P2 plays flipped W at (8, 9)
    assert blokus.curr_player == 2
    piece_w = Piece(blokus.shapes[ShapeKind.W])
    piece_w.set_anchor((8, 9))
    piece_w.flip_horizontally()
    assert blokus.maybe_place(piece_w), "Issue with piece 2"

    # Piece 3: P1 plays rotated R twice + flipped N at (7, 6)
    assert blokus.curr_player == 1
    piece_n = Piece(blokus.shapes[ShapeKind.N])
    piece_n.set_anchor((7, 6))
    piece_n.rotate_right()
    piece_n.rotate_right()
    piece_n.flip_horizontally()
    assert blokus.maybe_place(piece_n), "Issue with piece 3"

    # Piece 4: P2 plays Y at (4, 7)
    assert blokus.curr_player == 2
    piece_y = Piece(blokus.shapes[ShapeKind.Y])
    piece_y.set_anchor((4, 7))
    assert blokus.maybe_place(piece_y), "Issue with piece 4"

    # Piece 5: P1 plays X at (2, 6)
    assert blokus.curr_player == 1
    piece_x = Piece(blokus.shapes[ShapeKind.X])
    piece_x.set_anchor((2, 6))
    assert blokus.maybe_place(piece_x), "Issue with piece 5"

    # Piece 6: P2 plays rotated L + flipped S at (6, 5)
    assert blokus.curr_player == 2
    piece_s = Piece(blokus.shapes[ShapeKind.S])
    piece_s.set_anchor((6, 5))
    piece_s.rotate_left()
    piece_s.flip_horizontally()
    assert blokus.maybe_place(piece_s), "Issue with piece 6"

    # Piece 7: P1 plays rotated L T at (8, 4)
    assert blokus.curr_player == 1
    piece_t = Piece(blokus.shapes[ShapeKind.T])
    piece_t.set_anchor((8, 4))
    piece_t.rotate_left()
    assert blokus.maybe_place(piece_t), "Issue with piece 7"

    # Piece 8: P2 plays X at (9, 6)
    assert blokus.curr_player == 2
    piece_x = Piece(blokus.shapes[ShapeKind.X]) #Not essential to re-initialize
    piece_x.set_anchor((9, 6))
    assert blokus.maybe_place(piece_x), "Issue with piece 8"

    # Piece 9: P1 plays rotated R twice + flipped L at (4, 8)
    assert blokus.curr_player == 1
    piece_l = Piece(blokus.shapes[ShapeKind.L])
    piece_l.set_anchor((4, 8))
    piece_l.rotate_right()
    piece_l.rotate_right()
    piece_l.flip_horizontally() 
    assert blokus.maybe_place(piece_l), "Issue with piece 9"

    # Piece 10: P2 plays rotated R THREE at (5, 9)
    assert blokus.curr_player == 2
    piece_three = Piece(blokus.shapes[ShapeKind.THREE])
    piece_three.set_anchor((5, 9))
    piece_three.rotate_right()
    assert blokus.maybe_place(piece_three), "Issue with piece 10"

    # Piece 11: P1 plays rotated R twice Y at (6, 10)
    assert blokus.curr_player == 1
    piece_y = Piece(blokus.shapes[ShapeKind.Y])
    piece_y.set_anchor((6, 10))
    piece_y.rotate_right()
    piece_y.rotate_right()
    assert blokus.maybe_place(piece_y), "Issue with piece 11"

    # Piece 12: P2 plays rotated L SEVEN at (11, 8)
    assert blokus.curr_player == 2
    piece_seven = Piece(blokus.shapes[ShapeKind.SEVEN])
    piece_seven.set_anchor((11, 8))
    piece_seven.rotate_left()
    assert blokus.maybe_place(piece_seven), "Issue with piece 12"

    # Piece 13: P1 plays rotated R U at (11, 1)
    assert blokus.curr_player == 1
    piece_u = Piece(blokus.shapes[ShapeKind.U])
    piece_u.set_anchor((11, 1))
    piece_u.rotate_right()
    assert blokus.maybe_place(piece_u), "Issue with piece 13"

    # Piece 14: P2 plays rotated L U at (11, 4)
    assert blokus.curr_player == 2
    piece_u = Piece(blokus.shapes[ShapeKind.U])
    piece_u.set_anchor((11, 4))
    piece_u.rotate_left()
    assert blokus.maybe_place(piece_u), "Issue with piece 14"

    # Piece 15: P1 plays LETTER O at (11, 5)
    assert blokus.curr_player == 1
    piece_letter_o = Piece(blokus.shapes[ShapeKind.LETTER_O])
    piece_letter_o.set_anchor((11, 5))
    assert blokus.maybe_place(piece_t), "Issue with piece 15"

    # Piece 16: P2 plays flipped N at (7, 2)
    assert blokus.curr_player == 1
    piece_n = Piece(blokus.shapes[ShapeKind.N])
    piece_n.set_anchor((7, 2))
    piece_n.flip_horizontally()
    assert blokus.maybe_place(piece_n), "Issue with piece 16"

    # Piece 17: P1 plays FIVE at (7, 0)
    assert blokus.curr_player == 1
    piece_five = Piece(blokus.shapes[ShapeKind.FIVE])
    piece_five.set_anchor((7, 0))
    assert blokus.maybe_place(piece_five), "Issue with piece 17"

    # Piece 18: P2 plays rotated R F at (8, 12)
    assert blokus.curr_player == 2
    piece_f = Piece(blokus.shapes[ShapeKind.F])
    piece_f.set_anchor((8, 12))
    piece_f.rotate_right()
    assert blokus.maybe_place(piece_f), "Issue with piece 18"

    # Piece 19: P1 plays rotated L N at (10, 12)
    assert blokus.curr_player == 1
    piece_n = Piece(blokus.shapes[ShapeKind.N])
    piece_n.set_anchor((10, 12))
    piece_n.rotate_left()
    assert blokus.maybe_place(piece_n), "Issue with piece 19"

    # Piece 20: P2 plays flipped N at (7, 2)
    assert blokus.curr_player == 1
    piece_n = Piece(blokus.shapes[ShapeKind.N])
    piece_n.set_anchor((7, 2))
    piece_n.flip_horizontally()
    assert blokus.maybe_place(piece_n), "Issue with piece 20"

    # Piece 21: P1 plays flipped + rotated R Z at (10, 9)
    assert blokus.curr_player == 1
    piece_z = Piece(blokus.shapes[ShapeKind.Z])
    piece_z.set_anchor((10, 9))
    piece_z.flip_horizontally()
    piece_z.rotate_right()
    assert blokus.maybe_place(piece_z), "Issue with piece 21"

    # Piece 22: P2 plays TWO at (13, 5)
    assert blokus.curr_player == 2
    piece_two = Piece(blokus.shapes[ShapeKind.TWO])
    piece_two.set_anchor((13, 5))
    assert blokus.maybe_place(piece_two), "Issue with piece 22"

    # Piece 23: P1 plays rotated R P at (12, 9)
    assert blokus.curr_player == 1
    piece_p = Piece(blokus.shapes[ShapeKind.P])
    piece_p.set_anchor((12, 9))
    piece_p.rotate_right()
    assert blokus.maybe_place(piece_p), "Issue with piece 23"

    # Piece 24: P2 plays rotated R V at (12, 1)
    assert blokus.curr_player == 2
    piece_v = Piece(blokus.shapes[ShapeKind.V])
    piece_v.set_anchor((12, 1))
    piece_v.rotate_right()
    assert blokus.maybe_place(piece_v), "Issue with piece 24"

    # Piece 25: P1 plays rotated L S at (4, 1)
    assert blokus.curr_player == 1
    piece_s = Piece(blokus.shapes[ShapeKind.S])
    piece_s.set_anchor((4, 1))
    piece_s.rotate_left()
    assert blokus.maybe_place(piece_s), "Issue with piece 25"

    # Piece 26: P2 plays ONE at (3, 5)
    assert blokus.curr_player == 2
    piece_one = Piece(blokus.shapes[ShapeKind.ONE])
    piece_one.set_anchor((3, 5))
    assert blokus.maybe_place(piece_one), "Issue with piece 26"

    # Piece 27: P1 plays A at (0, 8)
    assert blokus.curr_player == 1
    piece_a = Piece(blokus.shapes[ShapeKind.A])
    piece_a.set_anchor((0, 8))
    assert blokus.maybe_place(piece_a), "Issue with piece 27"

    # Piece 28: P2 plays LETTER O at (1, 3)
    assert blokus.curr_player == 2
    piece_o = Piece(blokus.shapes[ShapeKind.LETTER_O])
    piece_o.set_anchor((1, 3))
    assert blokus.maybe_place(piece_o), "Issue with piece 28"

    # Piece 29: P1 plays rotated R twice V at (1, 3)
    assert blokus.curr_player == 1
    piece_v = Piece(blokus.shapes[ShapeKind.V])
    piece_v.set_anchor((1, 3))
    piece_v.rotate_right()
    piece_v.rotate_right()
    assert blokus.maybe_place(piece_v), "Issue with piece 29"

    # P2 retires
    assert blokus.curr_player == 2
    blokus.retire()

    # Piece 30: P1 plays rotated R THREE at (1, 0)
    assert blokus.curr_player == 1
    piece_three = Piece(blokus.shapes[ShapeKind.THREE])
    piece_three.set_anchor((1, 0))
    piece_three.rotate_right()
    assert blokus.maybe_place(piece_three), "Issue with piece 30"

    # Piece 31: P1 plays TWO at (13, 3)
    piece_two = Piece(blokus.shapes[ShapeKind.TWO])
    piece_two.set_anchor((13, 3))
    assert blokus.maybe_place(piece_two), "Issue with piece 31"

    # Piece 32: P1 plays rotates L C at (13, 12)
    piece_c = Piece(blokus.shapes[ShapeKind.C])
    piece_c.set_anchor((13, 12))
    piece_c.rotate_left()
    assert blokus.maybe_place(piece_c), "Issue with piece 32"

    # Piece 33: P2 plays rotated L SEVEN at (1, 11)
    piece_seven = Piece(blokus.shapes[ShapeKind.SEVEN])
    piece_seven.set_anchor((1, 11))
    piece_seven.rotate_left()
    assert blokus.maybe_place(piece_seven), "Issue with piece 33"

    return blokus # P2 retired, P1 has ONE and FOUR left to play

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
    blokus = fill_grid_except_last_two()

    # Piece 34: P1 plays ONE at (3, 11)
    piece_one = Piece(blokus.shapes[ShapeKind.ONE])
    piece_one.set_anchor((3, 11))
    assert blokus.maybe_place(piece_one), "Issue with piece 34"

    # Piece 35: P1 plays rotated R FOUR at (3, 13)
    piece_four = Piece(blokus.shapes[ShapeKind.FOUR])
    piece_four.set_anchor((3, 13))
    piece_four.rotate_right()
    assert blokus.maybe_place(piece_four), "Issue with piece 35"

    assert blokus.game_over, "P2 retired and P1 played all pieces"
    assert blokus.winners == 1, "P1 should have won"
    assert blokus.get_score(1) == 15, "P1's score should be 15"
    assert blokus.get_score(2) == -33, "P2's score should be -33"
    assert blokus.remaining_shapes(1) == [], "P1 should have no shapes left"
    for shape in blokus.remaining_shapes(2):
        assert shape in {ShapeKind.T, ShapeKind.L, ShapeKind.FIVE, ShapeKind.A,
                         ShapeKind.Z, ShapeKind.P, ShapeKind.FOUR}

# Test 31
def test_20_points():
    """
    Same as above, but where a player scores 20 points, that is, plays all 21
    pieces with ONE as the last piece played.
    Note: The sequence of moves in this test can be very similar to the previous
    test. If so, factor your code in a way that avoids a giant amount of
    copy-pasted code.
    """
    blokus = fill_grid_except_last_two()

    # Piece 34: P1 plays rotated R FOUR at (3, 13)
    piece_four = Piece(blokus.shapes[ShapeKind.FOUR])
    piece_four.set_anchor((3, 13))
    piece_four.rotate_right()
    assert blokus.maybe_place(piece_four), "Issue with piece 34"

    # Piece 35: P1 plays ONE at (3, 11)
    piece_one = Piece(blokus.shapes[ShapeKind.ONE])
    piece_one.set_anchor((3, 11))
    assert blokus.maybe_place(piece_one), "Issue with piece 35"

    assert blokus.game_over, "P2 retired and P1 played all pieces"
    assert blokus.winners == 1, "P1 should have won"
    assert blokus.get_score(1) == 20, "P1's score should be 20"
    assert blokus.get_score(2) == -33, "P2's score should be -33"
    assert blokus.remaining_shapes(1) == [], "P1 should have no shapes left"
    for shape in blokus.remaining_shapes(2):
        assert shape in {ShapeKind.T, ShapeKind.L, ShapeKind.FIVE, ShapeKind.A,
                         ShapeKind.Z, ShapeKind.P, ShapeKind.FOUR}
