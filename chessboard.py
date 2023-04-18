import tkinter as tk
from piece import Piece

# Font styles
LARGE_FONT = 'Arial 40 bold'
BUTTON_FONT = 'Arial 14'
LIST_FONT = 'Arial 16'

# Colors
BLACK = '#000000'
GRAY = '#474747'
GREEN = '#6ba649'
WHITE = '#f0f1ff'
DARK_WHITE = '#e6e6e6'
MUSTARD = '#e0d79b'
LIME = '#9fe04f'
RED = '#e81a3c'
DARK_RED = '#ab132c'
BLUE = '#3f59b5'
PUKE_GREEN = '#84b53f'

class Chessboard(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self['width'] = 819
        self['bg'] = GRAY
        
        self.board = {}
        self.boardCanvas = tk.Canvas(master=self, width=712, height=712, bg=GREEN, borderwidth=0, highlightthickness=0)
        self.boardCanvas.pack(expand=True)
        self.boardCanvas.bind('<Button-1>', self.onClick)
        
        self.pieces = {}
        self.selPiece = None # Keeps track on what piece is selected. Modified by piece class
        
        self.createBoard()
        self.createPieces()

    # Construct 8x8 chessboard
    def createBoard(self):
        SQUARE_SIZE = 89
        self.markImage = []

        for i in range(8): # Row
            self.board[i+1] = {}

            for j in range(8): # Column
                xLeft = j * SQUARE_SIZE
                yTop = i * SQUARE_SIZE
                xRight = xLeft + SQUARE_SIZE
                yBottom = yTop + SQUARE_SIZE

                squareTag = self.boardCanvas.create_rectangle(xLeft, yTop, xRight, yBottom, outline='')
                square = self.boardCanvas.find_withtag(squareTag)[0]

                self.board[i+1][j+1] = {
                    'square': square,
                    'center': {'x': (xRight-xLeft)/2 + xLeft, 'y': (yBottom-yTop)/2 + yTop},
                    'piece': None,
                    'pieceRef': None,
                    'pieceName': None,
                    'pieceColor': None,
                    'defendedByBlack': True if (i + 1 <= 3) else False,
                    'defendedByWhite': True if (i + 1 >= 6) else False
                }

                # Color board square if row and column sum is even
                if ((i + j) % 2 == 0):
                    self.boardCanvas.itemconfig(square, fill=DARK_WHITE)
                else:
                    self.boardCanvas.itemconfig(square, fill=BLUE)

    # Initialize chess pieces on board
    def createPieces(self):
        startPos = {
            1:{1:'Rook', 2:'Knight', 3:'Bishop', 4:'Queen', 5:'King', 6:'Bishop', 7:'Knight', 8:'Rook'},
            2:{1:'Pawn', 2: 'Pawn', 3:'Pawn', 4:'Pawn', 5:'Pawn', 6:'Pawn', 7:'Pawn', 8:'Pawn'},
            7:{1:'Pawn', 2: 'Pawn', 3:'Pawn', 4:'Pawn', 5:'Pawn', 6:'Pawn', 7:'Pawn', 8:'Pawn'},
            8:{1:'Rook', 2:'Knight', 3:'Bishop', 4:'Queen', 5:'King', 6:'Bishop', 7:'Knight', 8:'Rook'}
        }

        self.pieceImage = []
        for i in startPos:
            color = 'B' if (i <= 2) else 'W'
            for j in startPos[i]:
                self.pieceImage.append(tk.PhotoImage(file=f'img/{color}_{startPos[i][j]}.png'))
                pieceTag = self.boardCanvas.create_image(
                    self.board[i][j]['center']['x'], self.board[i][j]['center']['y'], 
                    image=self.pieceImage[len(self.pieceImage) - 1]
                )
                pieceRef = self.boardCanvas.find_withtag(pieceTag)[0]
                piece = Piece(pieceRef, startPos[i][j], color, self.boardCanvas, i, j)

                self.pieces[pieceTag] = piece

                self.board[i][j]['piece'] = piece
                self.board[i][j]['pieceRef'] = pieceRef
                self.board[i][j]['pieceName'] = startPos[i][j]
                self.board[i][j]['pieceColor'] = color

                if (startPos[i][j] == 'Rook'):
                    self.board[i][j]['defendedByBlack'] = False
                    self.board[i][j]['defendedByWhite'] = False

    def onClick(self, event):
        tag = self.boardCanvas.find_withtag('current')[0]

        if (tag in self.pieces and self.pieces[tag] is not self.selPiece and 
            self.pieces[tag].color is 'W'):

            if (self.selPiece is not None):
                row = self.selPiece.row
                col = self.selPiece.col
                oldSquare = self.board[row][col]['square']
                self.boardCanvas.itemconfig(oldSquare, fill=WHITE if ((row + col) % 2 == 0) else BLUE)

            self.selPiece = self.pieces[tag]

            # WIP ---------------------------------------------------------------------------
            for i in self.board:
                for j in self.board:
                    square = self.board[i][j]['square']
                    piece = self.board[i][j]['piece']

                    if (piece is not None and self.selPiece is piece):
                        self.boardCanvas.itemconfig(square, fill=LIME)

                    # A piece is present on square
                    elif (piece is not None and piece.color == 'B'):
                        if ((i + j) % 2 == 0):
                            self.boardCanvas.itemconfig(square, fill=RED)

                        else:
                            self.boardCanvas.itemconfig(square, fill=DARK_RED)

                    elif (piece is None):
                        if ((i + j) % 2 == 0):
                            self.boardCanvas.itemconfig(square, fill=MUSTARD)

                        else:
                            self.boardCanvas.itemconfig(square, fill=PUKE_GREEN)

            print(f'{self.selPiece.color}_{self.selPiece.type}, Row: {self.selPiece.row}, Col: {self.selPiece.col}')
        
        else:
            self.selPiece = None

            for i in self.board:
                for j in self.board[i]:
                    square = self.board[i][j]['square']
                    if ((i + j) % 2 == 0):
                            self.boardCanvas.itemconfig(square, fill=DARK_WHITE)
                    else:
                            self.boardCanvas.itemconfig(square, fill=BLUE)

            print('Selected empty square')