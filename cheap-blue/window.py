import sys

#import time

from PyQt5.QtGui import QColor, QPalette, QPixmap
from PyQt5.QtCore import Qt, QSize, pyqtSignal
from PyQt5.QtWidgets import *
#Yes, this is bad practice
#Suck it.

import chessboard
from chessboard import ChessBoard, Chess_piece
#Handles game itself


#Main program window
class MainWindow(QMainWindow):
    """
    Contains every element displayed in
    the gui.

    Class variables- board: DisplayBoard,
    stores current position

    Methods
    innit: Set up screen and draw board
    _draw_board: draws the board
    _size_screen: sets MW dimensions to big square


    """

    board = None

    def __init__(self):

        super().__init__()

        MainWindow.board = DisplayBoard()


        self._size_screen()
        self.setWindowTitle("Cheap Blue")

        self._draw_board()

    #Draws squares and pieces
    def _draw_board(self):

        layout = self.board.layout

        widget = QWidget()
        widget.setLayout(layout)

        self.setCentralWidget(widget)


    #Creates the largest square screen possible
    def _size_screen(self):

        app = QApplication.instance()

        screen = app.primaryScreen()
        geometry = screen.availableGeometry()

        height = geometry.height()
        width = geometry.width()

        self.setFixedSize(QSize(height, height))


class DisplaySquare(QLabel):
    """Converts a square to a DisplaySquare
    object, which can be drawn onscreen
    and take mouse input

    Class variables-
    Selected_Piece: stores a square if
    selected, otherwise stores false

    Instance variables:
    x_pos: x position of square
    y_pos: y position of square
    both assume that the bottom left
    corner of screen is 0,0
    square: the square object this
    DisplaySquare holds


    Methods:
    _set_background_square: changes square
    color to color
    _get_color: uses the square's x and y
    to determine whether the background is
    white or black
    draw_piece: pretty selfevident
    mousePressEvent: decide what to do when
    clicked
    """


    def __init__(self, square):

        super().__init__()

        self.square = square

        self.x_pos = square.x_pos
        self.y_pos = square.y_pos

        color = self._get_color()

        self._set_background_square(color)

        self.piece = square.piece

        self.draw_piece()


    #Draws square background to col
    def _set_background_square(self, col):

        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(col))
        self.setPalette(palette)


    #Finds correct color using x and y coords
    def _get_color(self):

        if ((self.x_pos + self.y_pos) % 2 == 0):
            #Black
            return '#BA8C63'
        else:
            #White
            return '#DEB887'


    #If square selected, move piece. Otherwise select square
    def mousePressEvent(self, event):

        if (DisplayBoard.Selected_Piece):

            MainWindow.board.test_move(DisplayBoard.Selected_Piece, self.square)
            DisplayBoard.Selected_Piece = False

        else:
            self._set_background_square('red')
            DisplayBoard.Selected_Piece = self.square

    def draw_piece(self):

        file = get_file(self.piece)

        if (file):

            pixmap = QPixmap(file)

            pixmap = pixmap.scaled(95, 95, Qt.KeepAspectRatio)

            self.setPixmap(pixmap)
            self.setAlignment(Qt.AlignCenter)

        else:

            self.clear()


class DisplayBoard():
    """
    Stores current position and
    an array of DisplaySquares

    Class vars-
    Selected_Piece: if square selected
    stores that square, otherwise stores False

    Instance variables:

    board: a ChessBoard object containing
    the current position
    layout: QGridLayout to displayed board

    Methods- move: Move piece from one square
    to another, _getarr: Return an array of DisplaySquares
    get_layout: convert array to QGridLayout

    """

    Selected_Piece = False


    def __init__(self, pos = ChessBoard()):

        self.board = pos
        self._board_array = self._getarr()
        self.layout = self.get_layout()

    def _getarr(self):

        current_board = [[None for j in range (8)] for i in range (8)]
        for col in self.board.position:
            for square in col:
                #print("x: {} y: {} piece: {}".format(square.x_pos, square.
                #y_pos, square.piece))
                i = square.x_pos
                j = square.y_pos

                current_board[i][j] = DisplaySquare(square)

        return current_board

    def get_layout(self):

        #Return QGridLayout

        layout = QGridLayout()
        layout.setHorizontalSpacing(0)
        layout.setVerticalSpacing(0)

        for i in range (8):
            for j in range(7, -1, -1):
                layout.addWidget(self._board_array[i][7 - j], j, i)

        return layout

    def test_move(self, square1, square2):
        """
        Tests to see if square1 can move to square2,
        if so, moves the piece from square1 to square2

        Paramemeters
        ------------
            square1: Square, the square moving from
            square2: Square, the square moving to

        Returntype: Void

        Functionality
        -------------
        See if move is legal, if so, make it.
        """
        move = chessboard.ChessMove(square1, square2)

        movelist = chessboard.get_legal_moves(self.board)

        legal = False


        for i in movelist:

            if (i == move):

                legal = True

        if (legal):
            self._move(square1, square2)

        x1 = square1.x_pos
        y1 = square1.y_pos

        x2 = square2.x_pos
        y2 = square2.y_pos

        col = self._board_array[x1][y1]._get_color()
        col2 = self._board_array[x2][y2]._get_color()

        self._board_array[x1][y1]._set_background_square(col)
        self._board_array[x2][y2]._set_background_square(col2)

        self.Selected_Piece = False


    def _move(self, square1, square2):

        self.board.move(square1, square2)
        for x in range(8):
            for y in range(8):
                self._board_array[x][y].piece = self.board.position[x][y].piece
                self._board_array[x][y].draw_piece()



#Returns address of piece file
def get_file(piece):
    if (piece == Chess_piece.WHITE_PAWN):
        return 'pieces/w-pawn.png'

    if (piece == Chess_piece.BLACK_PAWN):
        return 'pieces/b-pawn.png'

    if (piece == Chess_piece.WHITE_KNIGHT):
        return 'pieces/w-knight.png'

    if (piece == Chess_piece.BLACK_KNIGHT):
        return 'pieces/b-knight.png'

    if (piece == Chess_piece.WHITE_BISHOP):
        return 'pieces/w-bishop.png'

    if (piece == Chess_piece.BLACK_BISHOP):
        return 'pieces/b-bishop.png'

    if (piece == Chess_piece.WHITE_ROOK):
        return 'pieces/w-rook.png'

    if (piece == Chess_piece.BLACK_ROOK):
        return 'pieces/b-rook.png'

    if (piece == Chess_piece.WHITE_KING):
        return 'pieces/w-king.png'

    if (piece == Chess_piece.BLACK_KING):
        return 'pieces/b-king.png'

    if (piece == Chess_piece.WHITE_QUEEN):
        return 'pieces/w-queen.png'

    if (piece == Chess_piece.BLACK_QUEEN):
        return 'pieces/b-queen.png'

    return False
