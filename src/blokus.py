from abc import ABC, abstractmethod
from typing import Optional

from base import BlokusBase, Grid
from piece import Point, Shape, Piece
from shape_definitions import ShapeKind, definitions

# Can remove docstrings for methods defined in BlokusBase

class Blokus(BlokusBase):
    """
    Class for Blokus game logic.
    """

    _shapes: dict[ShapeKind, Shape]
    _size: int
    _num_players: int
    _curr_player: int
    _grid: Grid
    _num_moves: int
    _retired_players: set[int]
    _last_move: Piece

    def __init__(self, num_players: int, size: int, start_positions: set[tuple[int, int]]) -> None:
        """
        Constructor

        num_players: Number of players
        size: Number of squares on each side of the board
        start_positions: Positions for players' first moves

        Raises ValueError...
        if num_players is less than 1 or more than 4,
        if the size is less than 5,
        if not all start_positions are on the board, or
        if there are fewer start_positions than num_players.    
        """

        if not (1 <= num_players <= 4) or size < 5 or len(start_positions) < num_players:
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
        self._last_move = None

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

        for i in range(1, self.num_players + 1):
            if i not in self.retired_players and len(self.remaining_shapes(i)) != 0:
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
            if self.get_score(i) > highest_score and len(highest_player) == 0:
                highest_player.append(i)
                highest_score = self.get_score(i)
            elif self.get_score(i) > highest_score:
                highest_player.pop()
                highest_player.append(i)
                highest_score = self.get_score(i)
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
        return list(shape_kinds)

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
        
        if self.any_wall_collisions(piece):
            return True
        
        for point in piece.squares():
            r, c = point
            if self.grid[r][c] is not None:
                return True
        return False

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
        if piece.shape.kind not in self.remaining_shapes(self.curr_player):
            raise ValueError("Player has already played a piece with this shape")
        if piece.anchor is None:
            raise ValueError("Anchor of the piece is None")

        if self.any_collisions(piece):
            #print("HAS COLLISION")
            return False
        
        if len(self.remaining_shapes(self.curr_player)) == 21:
            for point in piece.squares():
                r, c = point
                if point in self.start_positions and self.grid[r][c] is None:
                    return True
        else:
            corner_case = False
            for point in piece.squares():
                r, c = point
                #print("point row:", r, "point col:", c)
                for row_index in range(r - 1, r + 2):
                    for col_index in range(c - 1, c + 2):
                        if (0 <= row_index < self.size) and (0 <= col_index < self.size):
                            grid_value = self.grid[row_index][col_index]
                            #print("checking row index: ", row_index, "col index:", col_index, "grid val:", grid_value)
                            index = (row_index, col_index)
                            
                            if grid_value is not None:
                                if index == (r-1, c-1) or index == (r-1, c+1) or index == (r+1, c-1) or index == (r+1, c+1):
                                    #print("has corner case at", index)
                                    #print("grid val", grid_value[0], "player:", self.curr_player)
                                    if grid_value[0] == self.curr_player:
                                        corner_case = True
                                elif grid_value[0] == self.curr_player:
                                    #print("index:", index, "already has piece!")
                                    return False
            #print("corner case:", corner_case)
            return corner_case

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
            #print("Legal to place!")
            for point in piece.squares():
                r, c = point
                self.grid[r][c] = (self.curr_player, piece.shape.kind)

            # updates last move and current player to next player
            self._last_move = piece
            all_players: list[int] = list(range(1, self.num_players + 1))

            while self.num_players != 1 and not self.game_over:
                cur_index = self.curr_player % len(all_players) - 1
                self.set_curr_player(all_players[cur_index + 1])
                if all_players[cur_index + 1] not in self.retired_players:
                    break
            return True
        return False

    def retire(self) -> None:
        """
        The current player, who has not played all their pieces,
        may choose to retire. This player does not get any more
        turns; they are skipped over during subsequent gameplay.
        """
        self._retired_players.add(self.curr_player)
        all_players: list[int] = list(range(1, self.num_players + 1))
        print("retiring player:", self.curr_player, "all players:", all_players)

        while self.num_players != 1 and not self.game_over:
            cur_index = self.curr_player % len(all_players) - 1
            #print("cur index:", cur_index)
            self.set_curr_player(all_players[cur_index + 1])
            #print("setting player to", all_players[cur_index + 1])
            if all_players[cur_index + 1] not in self.retired_players:
                #print(all_players[cur_index + 1], "not in retired, breaking!!!")
                break

    def get_score(self, player: int) -> int:
        """
        Returns the score for a given player. A player's score
        can be computed at any time during gameplay or at the
        completion of a game.
        """
        total: int = 0
        remaining: list[ShapeKind] = self.remaining_shapes(player)
        for shapekind in remaining:
            cur_shape = Shape.from_string(shapekind, definitions[shapekind])
            total += len(cur_shape.squares)
        if len(self.remaining_shapes(player)) == 0 and self._last_move.shape.kind == ShapeKind.ONE:
            return 20
        elif len(self.remaining_shapes(player)) == 0:
            return 15
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
            # traverse grid
            for r in range(self.size):
                for c in range(self.size):
                    piece = Piece(self.shapes[remaining_shape])
                    piece.set_anchor((r, c)) # Testing different locations
                    if self.legal_to_place(piece):
                        available_moves.add(piece)

                    # # Check different orientations
                    # for _ in range(4):
                    #     piece.rotate_left() 
                    #     if self.legal_to_place(piece):
                    #         available_moves.add(piece)
                    # # Now check mirrored version and different orientations
                    # piece.flip_horizontally() 
                    # for _ in range(4):
                    #     piece.rotate_left() 
                    #     if self.legal_to_place(piece):
                    #         available_moves.add(piece)
        return available_moves