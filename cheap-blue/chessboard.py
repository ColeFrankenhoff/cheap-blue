from enum import Enum, auto
from dataclasses import dataclass
import copy

class Chess_piece(Enum):
    WHITE_PAWN = auto()
    WHITE_KNIGHT = auto()
    WHITE_BISHOP = auto()
    WHITE_ROOK = auto()
    WHITE_QUEEN = auto()
    WHITE_KING = auto()

    BLACK_PAWN = auto()
    BLACK_KNIGHT = auto()
    BLACK_BISHOP = auto()
    BLACK_ROOK = auto()
    BLACK_QUEEN = auto()
    BLACK_KING = auto()

    EMPTY = auto()

WHITE_PAWN = Chess_piece.WHITE_PAWN
WHITE_KNIGHT = Chess_piece.WHITE_KNIGHT
WHITE_BISHOP = Chess_piece.WHITE_BISHOP
WHITE_ROOK = Chess_piece.WHITE_ROOK
WHITE_QUEEN = Chess_piece.WHITE_QUEEN
WHITE_KING = Chess_piece.WHITE_KING

BLACK_PAWN = Chess_piece.BLACK_PAWN
BLACK_KNIGHT = Chess_piece.BLACK_KNIGHT
BLACK_BISHOP = Chess_piece.BLACK_BISHOP
BLACK_ROOK = Chess_piece.BLACK_ROOK
BLACK_QUEEN = Chess_piece.BLACK_QUEEN
BLACK_KING = Chess_piece.BLACK_KING

EMPTY = Chess_piece.EMPTY


class Color(Enum):
    WHITE = auto()
    BLACK = auto()



WHITE = Color.WHITE
BLACK = Color.BLACK

#Creates a square which contains a piece and position
class Square():
    """
    Creates a square, which holds a location and
    a piece

    Attributes
    ----------
    x_pos: int
        the x position of the square
        with the A rank having a value
        0
    y_pos: int
        y position of a square,
        with white starting at 0

    Methods
    -------
    get_color:
        return the color of the
        square's piece, or False if
        the square doesn't have one

    """
    def __init__(self, piece, x, y):
        self.x_pos = x
        self.y_pos = y
        self.piece = piece

    def get_color(self):
        pieces = [piece for piece in Chess_piece]
        w_pieces = pieces[0:6]
        b_pieces = pieces[6:12]

        if self.piece in w_pieces:
            return WHITE
        elif self.piece in b_pieces:
            return BLACK
        else:
            return False



#This is a stupid flex of OOP. Fix later, if bored
@dataclass
class ChessMove:
    """
    Holds two squares and
    overwrites equality to
    compare them correctly
    """

    square1: Square
    square2: Square

    def __eq__(self, other):
        if (not other):
            return False

        if (self.square1.x_pos != other.square1.x_pos):
            return False

        if (self.square1.y_pos != other.square1.y_pos):
            return False

        if (self.square2.x_pos != other.square2.x_pos):
            return False

        if (self.square2.y_pos != other.square2.y_pos):
            return False

        return True

    def is_en_passant(self):

        piece = self.square1.piece
        if (piece == WHITE_PAWN or piece == BLACK_PAWN):
            if (self.square1.x_pos != self.square2.x_pos):
                if (self.square2.piece == EMPTY):
                    return True

        return False

    def __str__(self):

        string = "{}, {} to {}, {}".format(self.square1.x_pos,
        self.square1.y_pos, self.square2.x_pos, self.square2.y_pos)

        return string

#Stores castling rights, player's turns, and last move
@dataclass
class Gamestate():
    turn: Color = WHITE
    white_can_castle_kingside : bool = True
    white_can_castle_queenside : bool = True
    black_can_castle_kingside : bool = True
    black_can_castle_queenside : bool = True

    turn_number : int = 0
    fifty_move_rule : int = 0
    last_move : ChessMove = None


#This class is a bit beefy, but suck it.
class ChessBoard():
    """
    Holds a board, containing both gamestate
    and position

    Attributes
    ----------
    position : Square[]
        The position of all the pieces
    turn: Color()
        Who's turn it is to move
    white_kingside_castle: bool
        True if white has kingside castling
        rights
    white_queenside_castle: bool
        True if white has kingside castling
        rights
    black_kingside_castle: bool
        True if black has kingside castling rights
    black_queenside_castle: bool
        you get the point
    legal_moves: ChessMove[]
        A list of every legal move in the position

    Methods
    -------
        move(square1, square2):
            Move a peice from one square to another
            and update board accordingly
    """
    def __init__(self, data = Gamestate(), position = None):
        """
        Constructs all neccessary attributes for the
        chessboard object, using default board if
        parameters not given

        Optional Paramemeters
        ---------------------
            real: bool
                Is this a board created to check
                move legality or an active board?
            data: Gamestate()
                stores all auxiliary
                board data
            position: Square[]
                position of the board
        """

        self.position = position




        self.gamestate = data

        self.turn = data.turn



        if (self.position == None):
            self.position = self._set_up_board()



    def move(self, square1, square2):
        """
        Move a piece from square1
        to square2

        Returns: Void

        Functionality
        -------------
        Mutates self.position
        to be equal to the position
        after the move. Checks if move was en passant
        or castling, and if so updates position accordingly.
        Also changes turn and castling rights.
        """

        x1 = square1.x_pos
        y1 = square1.y_pos

        x2 = square2.x_pos
        y2 = square2.y_pos

        square1copy = copy.deepcopy(square1)
        square2copy = copy.deepcopy(square2)

        self.gamestate.last_move = ChessMove(square1copy, square2copy)
        self.gamestate.fifty_move_rule += 1

        if (ChessMove(square1, square2).is_en_passant() == True):
            self.position[x2][y1].piece = EMPTY

        piece = self.position[x1][y1].piece
        self.position[x1][y1].piece = EMPTY
        self.position[x2][y2].piece = piece

        if (piece == WHITE_KING or piece == BLACK_KING):
            if (abs(x1 - x2) == 2):

                midpoint = int((x1 + x2)/2)

                if (self.turn == WHITE):
                    self.position[midpoint][y1].piece = WHITE_ROOK
                else:
                    self.position[midpoint][y1].piece = BLACK_ROOK

            if (x2 == 2):
                self.position[0][y1].piece = EMPTY
            else:
                self.position[7][y1].piece = EMPTY

        if (self.turn == WHITE):
            self.gamestate.turn = BLACK
            self.turn = BLACK

        else:
            self.gamestate.turn = WHITE
            self.turn = WHITE

        #Check if pawn moved two squares
        if (piece == WHITE_PAWN or piece == BLACK_PAWN):

            if (y2 == 0):
                self.position[x2][y2].piece = BLACK_QUEEN

            if (y2 == 7):
                self.position[x2][y2].piece = WHITE_QUEEN



    #Initializes with default setup
    def _set_up_board(self):

        rows, cols = (8,8)

        #FUCK YEAH! List comprehension!
        pos = [[Square(Chess_piece.EMPTY, j, i)
        for i in range(cols)]
        for j in range(rows)]

        for square in pos:
            index = pos.index(square)
            pos[index][1].piece = WHITE_PAWN
            pos[index][6].piece = BLACK_PAWN

        pos[0][0].piece = WHITE_ROOK
        pos[7][0].piece = WHITE_ROOK
        pos[1][0].piece = WHITE_KNIGHT
        pos[6][0].piece = WHITE_KNIGHT
        pos[2][0].piece = WHITE_BISHOP
        pos[5][0].piece = WHITE_BISHOP
        pos[3][0].piece = WHITE_QUEEN
        pos[4][0].piece = WHITE_KING

        pos[0][7].piece = BLACK_ROOK
        pos[7][7].piece = BLACK_ROOK
        pos[1][7].piece = BLACK_KNIGHT
        pos[6][7].piece = BLACK_KNIGHT
        pos[2][7].piece = BLACK_BISHOP
        pos[5][7].piece = BLACK_BISHOP
        pos[3][7].piece = BLACK_QUEEN
        pos[4][7].piece = BLACK_KING

        return pos

    def _quasi_legal_moves(self):
        """Return every move that
        would be legal, ignoring check"""
        moves = []

        for row in self.position:
            for square in row:
                if (square.get_color() != self.turn):
                    continue

                list = self._list_moves(square)
                if not list:
                    continue

                for move in list:
                    moves.append(move)

            en_passants = self._legal_en_passants()

            if en_passants:
                for move in en_passants:
                    moves.append(move)


        return moves

    def _list_moves(self, square):
        """Return all moves possible from one square"""
        if (square.piece == Chess_piece.EMPTY):
            return False
        if (square.piece == WHITE_PAWN or square.piece == BLACK_PAWN):
            return self._pawn_moves(square)
        if (square.piece == WHITE_BISHOP or square.piece == BLACK_BISHOP):
            return self._bishop_moves(square)
        if (square.piece == WHITE_KNIGHT or square.piece == BLACK_KNIGHT):
            return self._knight_moves(square)
        if (square.piece == WHITE_ROOK or square.piece == BLACK_ROOK):
            return self._rook_moves(square)
        if (square.piece == WHITE_KING or square.piece == BLACK_KING):
            return self._king_moves(square)
        if (square.piece == WHITE_QUEEN or square.piece == BLACK_QUEEN):
            return self._queen_moves(square)

    def _pawn_moves(self, square):
        """Return every square a pawn can go to"""
        list = []

        if (square.get_color() == WHITE):
            y_increment = 1

        else:
            y_increment = - 1

        if (0 > square.y_pos + y_increment):

            return

        if (7 < square.y_pos + y_increment):

            return

        s2 = self.position[square.x_pos][square.y_pos+y_increment]

        if (s2.get_color() == False):

            list.append(ChessMove(square, s2))

            if ((square.y_pos == 1 and square.get_color() == WHITE) or
              (square.y_pos == 6 and square.get_color() == BLACK)):

                s3 = self.position[square.x_pos][square.y_pos + 2*y_increment]

                if (s3.get_color() == False):

                    list.append(ChessMove(square, s3))


        if (square.x_pos != 7):

            diag1 = self.position[square.x_pos+1][square.y_pos+y_increment]
            col1 = diag1.get_color()

            if (col1 != square.get_color()):

                if (col1):

                    list.append(ChessMove(square, diag1))

        if (square.x_pos != 0):
            diag2 = self.position[square.x_pos-1][square.y_pos+y_increment]
            col2 = diag2.get_color()

            if (col2 != square.get_color()):
                if (col2):
                    list.append(ChessMove(square, diag2))



        return list

    def _bishop_moves(self, square):

        #Store x and y position, and create empty list
        x_pos = square.x_pos
        y_pos = square.y_pos

        #create empty list
        list = []

        #iterate through every possible direction
        for i in (-1, 1):
            for j in (-1, 1):

                #going one square at a time, check legality in direction
                movelength = 1
                while True:

                    test_x = x_pos + movelength * i
                    test_y = y_pos + movelength * j

                    if not (0 <= test_x < 8):
                        break
                    if not(0 <= test_y < 8):
                        break

                    test_square = self.position[test_x][test_y]

                    if (test_square.get_color() == False):

                        list.append(ChessMove(square, test_square))

                    elif (test_square.get_color() != square.get_color()):

                        list.append(ChessMove(square, test_square))
                        break

                    else:
                        break

                    movelength += 1

        return list

    def _knight_moves(self, square):
        list = []
        for x_direction in (-1, 1, -2, 2):

            if (abs(x_direction) == 2):
                y_dist = 1

            else:
                y_dist = 2

            test_x = square.x_pos + x_direction

            if not (-1 < test_x < 8):
                continue

            for y_direction in (y_dist, -y_dist):

                test_y = square.y_pos + y_direction

                if not (-1 < test_y < 8):
                    continue

                test_square = self.position[test_x][test_y]

                if (test_square.get_color() != square.get_color()):
                    list.append(ChessMove(square, test_square))
        return list

    def _rook_moves(self, square):
        """"This is really shit code"""

        moves = []

        x_pos = square.x_pos
        y_pos = square.y_pos

        count = 1

        for i in (-1, 1):
            while True:

                test_x = x_pos + (count * i)

                if not (0 <= test_x < 8):
                    break

                t_square = self.position[test_x][y_pos]

                if (t_square.get_color() == False):
                    moves.append(ChessMove(square, t_square))

                elif (t_square.get_color() != square.get_color()):
                    moves.append(ChessMove(square, t_square))
                    break

                else:
                    break
                count += 1

        for j in (-1, 1):

            count = 1
            while True:

                test_y = y_pos + (count * j)

                if not (0 <= test_y < 8):
                    break

                test_square = self.position[x_pos][test_y]

                if (test_square.get_color() == False):
                    moves.append(ChessMove(square, test_square))

                elif (test_square.get_color() != square.get_color()):

                    moves.append(ChessMove(square, test_square))

                    break

                else:
                    break

                count += 1

        return moves

    def _king_moves(self, square):

        list = []
        x = square.x_pos
        y = square.y_pos

        for i in (-1, 0, 1):
            for j in (-1, 0, 1):

                test_x = x + i
                test_y = y + j

                if not (-1 < test_x < 8):
                    continue

                if not (-1 < test_y < 8):
                    continue

                test_square = self.position[test_x][test_y]

                if (test_square.get_color() != square.get_color()):
                    list.append(ChessMove(square, test_square))
        return list

    def _queen_moves(self, square):

        l1 = self._rook_moves(square)
        l2 = self._bishop_moves(square)

        return l1 + l2

    def _legal_en_passants(self):
        """
        Return every en passant legal in the position
        """


        move = self.gamestate.last_move

        if move is None:
            return False

        square1 = move.square1
        square2 = move.square2


        if not (square1.piece == WHITE_PAWN or square1.piece == BLACK_PAWN):
            return False

        if not (abs(square1.y_pos - square2.y_pos) == 2):
            return False

        list = []

        x = square2.x_pos
        y = square2.y_pos

        for i in (-1, 1):
            if (-1 < x + i < 8):
                adj_square = self.position[x + i][y]
                col = adj_square.get_color()
                if col is not False and (col != square1.get_color()):
                    if (self.turn == WHITE):
                        move = ChessMove(adj_square, self.position[x][y+1])

                    else:
                        move = ChessMove(adj_square, self.position[x][y-1])

                    list.append(move)

        return list

    def _add_castling(self):
        list = []
        white_ks = self.gamestate.white_can_castle_kingside
        white_qs = self.gamestate.white_can_castle_queenside

        black_ks = self.gamestate.white_can_castle_kingside
        black_qs = self.gamestate.white_can_castle_queenside

        if (white_ks and self.turn == WHITE):
            if (self.position[5][0].piece == EMPTY):
                if (self.position[6][0].piece == EMPTY):

                    move = ChessMove(self.position[4][0], self.position[6][0])
                    list.append(move)

        if (white_qs and self.turn == WHITE):
            if (self.position[3][0].piece == EMPTY):
                if (self.position[2][0].piece == EMPTY):

                    move = ChessMove(self.position[4][0], self.position[2][0])
                    list.append(move)

        if (black_ks and self.turn == BLACK):
            if (self.position[5][7].piece == EMPTY):
                if (self.position[6][7].piece == EMPTY):
                    move = ChessMove(self.position[4][7], self.position[6][7])
                    list.append(move)

        if (black_qs and self.turn == BLACK):
            if (self.position[3][7].piece == EMPTY):
                if (self.position[2][7].piece == EMPTY):

                    move = ChessMove(self.position[4][7], self.position[2][7])
                    list.append(move)

        if list is not None:
            return list

        return False

def get_legal_moves(board: ChessBoard):


    turn = board.gamestate.turn
    pos = board.position
    list = []

    king_x = None
    king_y = None

    for row in pos:
        for square in row:
            if (turn == WHITE):
                if (square.piece == WHITE_KING):
                    og_king_x = square.x_pos
                    og_king_y = square.y_pos
                    break
            if (turn == BLACK):
                if (square.piece == BLACK_KING):
                    og_king_x = square.x_pos
                    og_king_y = square.y_pos
                    break

    moves_to_test = board._quasi_legal_moves()
    for move in moves_to_test:

        king_x = og_king_x
        king_y = og_king_y

        sq1 = move.square1
        sq2 = move.square2

        piece = sq1.piece

        if ((piece == BLACK_KING) or (piece == WHITE_KING)):
            king_x = sq2.x_pos
            king_y = sq2.y_pos

        board_copy = copy.deepcopy(board)
        board_copy.move(sq1, sq2)

        test_list = board_copy._quasi_legal_moves()
        move_is_legal = True

        for test_move in test_list:
            if (test_move.square2.x_pos == king_x):
                if (test_move.square2.y_pos == king_y):
                    move_is_legal = False
                    break
        if move_is_legal:
            list.append(move)

    castling_possibilites = board._add_castling()

    for move in castling_possibilites:
        sq1 = move.square1
        sq2 = move.square2

        bd_copy = copy.deepcopy(board)
        if (bd_copy.turn == WHITE):
            bd_copy.turn = BLACK
            bd_copy.gamestate.turn = BLACK
        else:
            bd_copy.turn = WHITE
            bd_copy.gamestate.turn = WHITE

        can_castle = True
        midsquare = ((sq1.x_pos + sq2.x_pos)/2)
        for test_move in bd_copy._quasi_legal_moves():
            if (test_move.square2.x_pos == og_king_x):
                if (test_move.square2.y_pos == og_king_y):
                    can_castle = False
                    break

            if (test_move.square2.x_pos == og_king_x):
                if (test_move.square2.y_pos == og_king_y):
                    can_castle = False
                    break

            if (test_move.square2.x_pos == midsquare):
                if (test_move.square2.y_pos == og_king_y):
                    can_castle = False
                    break

        if can_castle:
            list.append(move)

    return list
