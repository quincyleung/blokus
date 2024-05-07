"""
Fake implementations of BlokusBase.

We provide a BlokusStub implementation, and
you must provide a BlokusFake implementation.
"""
from typing import Optional
import textwrap

from shape_definitions import ShapeKind, definitions
from piece import Point, Shape, Piece
from base import BlokusBase, Grid


class BlokusStub(BlokusBase):
    """
    Stub implementation of BlokusBase.

    This stub implementation behaves according to the following rules:

    - It only supports two players.
    - Only three of the 21 Blokus shapes are available:
      the one-square, two-square, and three-square straight pieces.
    - Players are allowed to place pieces in any position of the board
      they want, even if the piece collides with any squares of
      previously played pieces (squares of the new piece replace any
      conflicting ones).
    - Board positions are not validated. If a method is called with
      a position outside the board, it will likely cause an exception.
    - There is no consideration of start positions for a player's
      first move.
    - The constructor simulates two initial moves: placing
      Player 1's "1" piece in the top-left corner and
      Player 2's "2" piece in the bottom-right corner.
    - The game ends after six moves. The player, if any, who has a
      piece occupying the top-right corner of the board wins.
      Otherwise, the players tie.
    - The `remaining_shapes` method always says all three shapes remain.
    - The only shape that is considered available by `available_moves`
      is the one-square shape, and it is considered available everywhere
      on the board regardless of whether the corresponding positions are
      available or occupied.
    - Several methods return simple, unhelpful results (as opposed to
      raising NotImplementedErrors).
    """

    _shapes: dict[ShapeKind, Shape]
    _size: int
    _num_players: int
    _curr_player: int
    _grid: Grid
    _num_moves: int

    def __init__(
        self,
        num_players: int,
        size: int,
        start_positions: set[Point],
    ) -> None:
        """
        Constructor (See BlokusBase)

        This stub initializes a counter for number of moves
        in order to implement a simple game_over condition.

        Once everything is initialized, this stub implementation
        "simulates" two moves.
        """
        super().__init__(num_players, size, start_positions)
        self._shapes = self._load_shapes()
        self._size = size
        self._num_players = 2
        self._curr_player = 1
        self._grid = [[None] * size for _ in range(size)]
        self._num_moves = 0
        self._simulate_two_moves()

    def _load_shapes(self) -> dict[ShapeKind, Shape]:
        """
        Rather than reading in the representations of shapes
        from shape_definitions.py, this method manually builds
        three of the 21 kinds of shapes.

        See shape_definitions.py for more details.
        """
        # See shape_definitions.definitions[ShapeKind.ONE]
        shape_1 = Shape(ShapeKind.ONE, (0, 0), False, [(0, 0)])

        # See shape_definitions.definitions[ShapeKind.TWO]
        shape_2 = Shape(ShapeKind.TWO, (0, 0), True, [(0, 0), (0, 1)])

        # See shape_definitions.definitions[ShapeKind.THREE]
        shape_3 = Shape(
            ShapeKind.THREE, (0, 1), True, [(0, -1), (0, 0), (0, 1)]
        )

        return {
            ShapeKind.ONE: shape_1,
            ShapeKind.TWO: shape_2,
            ShapeKind.THREE: shape_3,
        }

    def _simulate_two_moves(self) -> None:
        """
        Simulates two moves:

        - Player 1 places their ShapeKind.ONE piece in the top-left corner.
        - Player 2 places their ShapeKind.TWO piece in the bottom-right corner.

        This drives the game into a state where four more pieces
        can be played before entering the game_over condition
        (six moves total).
        """
        piece_1 = Piece(self.shapes[ShapeKind.ONE])
        piece_1.set_anchor((0, 0))
        self.maybe_place(piece_1)

        # This anchor position accounts for the origin of
        # ShapeKind.TWO as specified in shape_definitions.py.
        piece_2 = Piece(self.shapes[ShapeKind.TWO])
        piece_2.set_anchor((self.size - 1, self.size - 2))
        self.maybe_place(piece_2)

    @property
    def shapes(self) -> dict[ShapeKind, Shape]:
        """
        See BlokusBase
        """
        return self._shapes

    @property
    def size(self) -> int:
        """
        See BlokusBase
        """
        return self._size

    @property
    def start_positions(self) -> set[Point]:
        """
        See BlokusBase
        """
        return set()

    @property
    def num_players(self) -> int:
        """
        See BlokusBase
        """
        return self._num_players

    @property
    def curr_player(self) -> int:
        """
        See BlokusBase
        """
        return self._curr_player

    @property
    def retired_players(self) -> set[int]:
        """
        See BlokusBase
        """
        return set()

    @property
    def grid(self) -> Grid:
        """
        See BlokusBase
        """
        return self._grid

    @property
    def game_over(self) -> bool:
        """
        See BlokusBase
        """
        return self._num_moves == 6

    @property
    def winners(self) -> list[int]:
        """
        See BlokusBase
        """
        top_right_cell = self.grid[0][self.size - 1]
        if top_right_cell is None:
            return [1, 2]
        else:
            winner = top_right_cell[0]
            return [winner]

    def remaining_shapes(self, player: int) -> list[ShapeKind]:
        """
        See BlokusBase
        """
        return [ShapeKind.ONE, ShapeKind.TWO, ShapeKind.THREE]

    def any_wall_collisions(self, piece: Piece) -> bool:
        """
        See BlokusBase
        """
        return False

    def any_collisions(self, piece: Piece) -> bool:
        """
        See BlokusBase
        """
        return False

    def legal_to_place(self, piece: Piece) -> bool:
        """
        See BlokusBase
        """
        return True

    def maybe_place(self, piece: Piece) -> bool:
        """
        See BlokusBase
        """
        for r, c in piece.squares():
            self._grid[r][c] = (self.curr_player, piece.shape.kind)
        self._curr_player = (self.curr_player % self.num_players) + 1
        self._num_moves += 1
        return True

    def retire(self) -> None:
        """
        See BlokusBase
        """
        pass

    def get_score(self, player: int) -> int:
        """
        See BlokusBase
        """
        return -999

    def available_moves(self) -> set[Piece]:
        """
        See BlokusBase
        """
        pieces = set()
        for r in range(self.size):
            for c in range(self.size):
                piece = Piece(self.shapes[ShapeKind.ONE])
                piece.set_anchor((r, c))
                pieces.add(piece)

        return pieces


#
# Your BlokusFake implementation goes here
#
class BlokusFake(BlokusBase):
    """
    Class for Fake Blokus game logic.
    
    num_players: Number of players
    size: Number of squares on each side of the board
    start_positions: Positions for players' first moves

    Raises ValueError...
    if num_players is less than 1 or more than 4,
    if the size is less than 5,
    if not all start_positions are on the board, or
    if there are fewer start_positions than num_players.    
    """

    _shapes: dict[ShapeKind, Shape]
    _size: int
    _num_players: int
    _curr_player: int
    _grid: Grid
    _num_moves: int
    _retired_players: set[int]

    def __init__(self, num_players: int, size: int, start_positions: set[tuple[int, int]]) -> None:
        if not (1 <= num_players <= 2) or size < 5 or len(start_positions) < num_players:
            raise ValueError
        for x, y in start_positions:
            if not (0 <= x < size) or not (0 <= y < size):
                raise ValueError("Not all start positions are on the board")
        super().__init__(num_players, size, start_positions)
        self._shapes = {}
        self._curr_player = 1
        self._grid = [[None] * size for _ in range(size)]
        self._num_moves = 0
        self._retired_players = set()

        # load 21 shapes
        for kind, definition in definitions.items():
            cur_shape = Shape.from_string(kind, definition)
            self._shapes[kind] = cur_shape

    #
    # PROPERTIES
    #

    @property
    def shapes(self) -> dict[ShapeKind, Shape]:
        """
        Returns all 21 Blokus shapes, as named and defined by
        the string representations in shape_definitions.py.

        The squares and origin, if any, of each shape should
        correspond to the locations and orientations defined
        in shape_definitions. For example, the five-square
        straight piece is called ShapeKind.FIVE, defined as a
        vertical line (as opposed to horizontal), and has its
        origin at the middle (third) square.

        See shape_definitions.py for more details.
        """
        return self._shapes

    @property
    def size(self) -> int:
        """
        Returns the board size (the number of squares per side).
        """
        return self._size
    
    @property
    def start_positions(self) -> set[Point]:
        """
        Returns the start positions.
        """
        return self._start_positions

    @property
    def num_players(self) -> int:
        """
        Returns the number of players. Players are numbered
        consecutively, starting from 1.
        """
        return self._num_players
    
    @property
    def curr_player(self) -> int:
        """
        Returns the player number for the player who must make
        the next move (i.e., "Whose turn is it?"). While the
        game is ongoing, this property never refers to a player
        that has played all of their pieces or that retired
        before playing all of their pieces. If the game is over,
        this property will not return a meaningful value.
        """
        return self._curr_player
    
    @property
    def retired_players(self) -> set[int]:
        """
        Returns the set of players who have retired. These
        players do not get any more turns; they are skipped
        over during subsequent gameplay.
        """
        return self._retired_players
    
    @property
    def grid(self) -> Grid:
        """
        Returns the current state of the board (i.e. Grid).
        There are two values tracked for each square (i.e. Cell)
        in the grid: the player number (an int) who has played
        a piece that occupies this square; and the shape kind
        of that piece. If no played piece occupies this square,
        then the Cell is None.
        """
        return self._grid

    @property
    def game_over(self) -> bool:
        """
        Returns whether or not the game is over. A game is over
        when every player is either retired or has played all
        their pieces.
        """
        if len(self.retired_players) == self.num_players:
            return True
        for i in range(self.num_players):
            if len(self.remaining_shapes(i)) != 0:
                return False
        return True

    @property
    def winners(self) -> Optional[list[int]]:
        """
        Returns the (one or more) players who have the highest
        score. Returns None if the game is not over.
        """
        highest_score: int = float('-inf')
        highest_player: list[int] = []

        for i in range(1, self.num_players + 1):
            # if greater than tracker
            if self.get_score(i) > highest_score:
                highest_score = self.get_score(i)
                highest_player.append(i)
            elif self.get_score(i) == highest_score:
                highest_player.append(i)
        return highest_player

    #
    # METHODS
    #

    def set_curr_player(self, value: int):
        """
        Updates the player number for the player who must 
        make the next move.
        """
        if value < 1 or value > self.num_players:
            raise ValueError("Invalid player number")
        self._curr_player = value

    def remaining_shapes(self, player: int) -> list[ShapeKind]:
        """
        Returns a list of shape kinds that a particular
        player has not yet played.
        """
        shape_kinds = set(self.shapes.keys())

        for row in self.grid:
            for cell in row:
                if cell is not None:
                    p, shape = cell
                    if player == p:
                        shape_kinds.discard(shape)
        return shape_kinds

    def any_wall_collisions(self, piece: Piece) -> bool:
        """
        Returns a boolean indicating whether or not the
        given piece (not yet played on the board) would
        collide with a wall. For the purposes of this
        predicate, a "wall collision" occurs when at
        least one square of the piece would be located
        beyond the bounds of the (size x size) board.

        Raises ValueError if the player has already
        played a piece with this shape.

        Raises ValueError if the anchor of the piece
        is None.
        """
        if piece.shape.kind not in self.remaining_shapes(self.curr_player):
            raise ValueError("Player has already played a piece with this shape")
        if piece.anchor is None:
            raise ValueError("Anchor of the piece is None")

        for point in piece.squares():
            r, c = point
            if (r < 0 or r >= self.size) or (c < 0 or c >= self.size):
                print("WALL COLLISION! r:", r, "c:", c )
                return True
        return False

    def any_collisions(self, piece: Piece) -> bool:
        """
        Returns a boolean indicating whether or not the
        given piece (not yet played on the board) would
        collide with a wall or with any played pieces.
        A "collision" between pieces occurs when they
        overlap.

        Raises ValueError if the player has already
        played a piece with this shape.

        Raises ValueError if the anchor of the piece
        is None.
        """
        if piece.shape.kind not in self.remaining_shapes(self.curr_player):
            raise ValueError("Player has already played a piece with this shape")
        if piece.anchor is None:
            raise ValueError("Anchor of the piece is None")
        
        for point in piece.squares():
            r, c = point
            if self.grid[r][c] is not None:
                print("piece already exists at ", "(", r, c, ")")
                return True
        print("wall collision:", self.any_wall_collisions(piece))
        return self.any_wall_collisions(piece)

    def legal_to_place(self, piece: Piece) -> bool:
        """
        If the current player has not already played
        this shape, this method returns a boolean
        indicating whether or not the given piece is
        legal to place. This requires that:

         - if the player has not yet played any pieces,
           this piece would cover a start position;
         - the piece would not collide with a wall or any
           previously played pieces; and
         - the piece shares one or more corners but no edges
           with the player's previously played pieces.

        Raises ValueError if the player has already
        played a piece with this shape.

        Raises ValueError if the anchor of the piece
        is None.
        """
        print("piece anchor:", piece.anchor)

        if piece.shape.kind not in self.remaining_shapes(self.curr_player):
            raise ValueError("Player has already played a piece with this shape")
        if piece.anchor is None:
            raise ValueError("Anchor of the piece is None")

        if self.any_collisions(piece):
            return False
        
        if len(self.remaining_shapes(self.curr_player)) == 21:
            for point in piece.squares():
                #print("start positions:", self.start_positions)
                #if point in self.start_positions:
                return True

    def maybe_place(self, piece: Piece) -> bool:
        """
        If the piece is legal to place, this method
        places the piece on the board, updates the
        current player and other relevant game state,
        and returns True.

        If not, this method leaves the board and current
        game state unmodified, and returns False.

        Note that the game does not necessarily end right
        away when a player places their last piece; players
        who have not retired and have remaining pieces
        should still get their turns.

        Raises ValueError if the player has already
        played a piece with this shape.

        Raises ValueError if the anchor of the piece
        is None.
        """
        if piece.shape.kind not in self.remaining_shapes(self.curr_player):
            raise ValueError("Player has already played piece with this shape")
        if piece.anchor is None:
            raise ValueError("Anchor of the piece is None")
        
        if self.legal_to_place(piece):
            print("---legal to place!---")
            for point in piece.squares():
                r, c = point
                self.grid[r][c] = (self.curr_player, piece.shape.kind)

            if self.curr_player == self.num_players:
                if 1 not in self.retired_players:
                    self.set_curr_player(1) 
            else:
                if (self.curr_player + 1) not in self.retired_players:
                    self.set_curr_player(self.curr_player + 1)
            return True
        return False

    def retire(self) -> None:
        """
        The current player, who has not played all their pieces,
        may choose to retire. This player does not get any more
        turns; they are skipped over during subsequent gameplay.
        """
        self._retired_players.add(self.curr_player)
        if self.curr_player == self.num_players:
                self.set_curr_player(1)
        else:
            self.set_curr_player(self.curr_player + 1)

    def get_score(self, player: int) -> int:
        """
        Returns the score for a given player. A player's score
        can be computed at any time during gameplay or at the
        completion of a game.
        """
        total: int = 0
        remaining = self.remaining_shapes(player)
        for shapekind in remaining:
            cur_shape = Shape.from_string(shapekind, definitions[shapekind])
            total += len(cur_shape.squares)
        return -(total)

    def available_moves(self) -> set[Piece]:
        """
        Returns the set of all possible moves that the current
        player may make. As with the arguments to the maybe_place
        method, a move is determined by a Piece, namely, one of
        the 21 Shapes plus a location and orientation.

        Notice there may be many different Pieces corresponding
        to a single Shape that are considered available moves
        (because they may differ in location and orientation).
        """
        available_moves: set[Piece] = set()
    
        for remaining_shape in self.remaining_shapes(self.curr_player):
            for r in range(self.size):
                for c in range(self.size):
                    piece = Piece(self.shapes[remaining_shape])
                    piece.set_anchor((r, c)) # Testing different locations
                    # Check different orientations
                    for _ in range(4):
                        piece.rotate_left() 
                        if self.legal_to_place(piece):
                            available_moves.add(piece)
                    # Now check mirrored version and different orientations
                    piece.flip_horizontally() 
                    for _ in range(4):
                        piece.rotate_left() 
                        if self.legal_to_place(piece):
                            available_moves.add(piece)

        return available_moves
    
"""
FOR CHECKING CORNERS AND EDGES
        for point in piece.squares():
            r, c = point
            print("row:", r, "col", c)
            for row_index in range(r - 1, r + 2):
                for col_index in range(c - 1, r + 2):
                    grid_value = self.grid[row_index][col_index]
                    print("row index: ", row_index, "col index:", col_index)
                    print("grid val:", grid_value)
                    index = (row_index, col_index)
                    if index == (0,0) or index == (0,2) or index == (2,0) or index == (2,2) and grid_value is not None:
                        print("has corner case!", index)
                        print("grid val", grid_value[0], "player:", self.curr_player)
                        if grid_value[0] == self.curr_player:
                            return True
                    elif grid_value is not None and grid_value[0] == self.curr_player:
                        return False
""" 