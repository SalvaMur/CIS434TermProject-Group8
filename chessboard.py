import tkinter as tk
from piece import Piece

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
        
        self.isPlayerTurn = True

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
                    'squareTag': squareTag,
                    'center': {'x': (xRight-xLeft)/2 + xLeft, 'y': (yBottom-yTop)/2 + yTop},
                    'piece': None,
                    'pieceRef': None,
                    'pieceTag': None,
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
                piece = Piece(pieceRef, pieceTag, startPos[i][j], color, self.boardCanvas, i, j)

                self.pieces[pieceTag] = piece

                self.board[i][j]['piece'] = piece
                self.board[i][j]['pieceRef'] = pieceRef
                self.board[i][j]['pieceTag'] = pieceTag
                self.board[i][j]['pieceName'] = startPos[i][j]
                self.board[i][j]['pieceColor'] = color

                if (startPos[i][j] == 'Rook'):
                    self.board[i][j]['defendedByBlack'] = False
                    self.board[i][j]['defendedByWhite'] = False

        for piece in self.pieces:
            if (self.pieces[piece].color == 'W'): # WIP -----------------------------
                self.pieces[piece].makeMoves(self.board)

    def onClick(self, event):
        tag = self.boardCanvas.find_withtag('current')[0]

        if (tag in self.pieces):
            newPiece = self.pieces[tag]
        else:
            newPiece = None

        # New player piece selected
        if (newPiece is not None and newPiece is not self.selPiece and 
            newPiece.color == ('W' if self.isPlayerTurn else 'B')):

            if (self.selPiece is not None): # Dehighlight previous piece
                row = self.selPiece.row
                col = self.selPiece.col
                oldSquare = self.board[row][col]['square']
                self.boardCanvas.itemconfig(oldSquare, fill= WHITE if ((row + col) % 2 == 0) else BLUE)

            self.selPiece = newPiece
            newSquare = self.board[self.selPiece.row][self.selPiece.col]['square']
            self.boardCanvas.itemconfig(newSquare, fill=LIME) # Highlight piece selected
            
            moveTable = self.selPiece.moveTable

            for key in moveTable:
                row = moveTable[key]['row']
                col = moveTable[key]['col']

                square = self.board[row][col]['square']
                piece = self.board[row][col]['piece']

                # An enemy piece is present on square
                if (piece is not None and piece.color == ('B' if self.isPlayerTurn else 'W')):
                    if ((row + col) % 2 == 0):
                        self.boardCanvas.itemconfig(square, fill=RED)

                    else:
                        self.boardCanvas.itemconfig(square, fill=DARK_RED)

                elif (piece is None):
                    if ((row + col) % 2 == 0):
                        self.boardCanvas.itemconfig(square, fill=MUSTARD)

                    else:
                        self.boardCanvas.itemconfig(square, fill=PUKE_GREEN)

            print(f'{self.selPiece.color}_{self.selPiece.type}, Row: {self.selPiece.row}, Col: {self.selPiece.col}')
        
        # Selected available square, or enemy piece on available square
        elif (self.selPiece is not None and 
            (tag in self.selPiece.moveTable or 
            newPiece is not None and self.board[newPiece.row][newPiece.col]['squareTag'] in self.selPiece.moveTable)):
            
            if (tag in self.selPiece.moveTable):
                row = self.selPiece.moveTable[tag]['row']
                col = self.selPiece.moveTable[tag]['col']

            else:
                row = newPiece.row
                col = newPiece.col

            # ADD MORE HERE --------------------------------------------------------

            self.clearSelection()

            xOffset = self.board[row][col]['center']['x']
            yOffset = self.board[row][col]['center']['y']
            self.selPiece.moveTo(row, col, xOffset, yOffset, self.board, self.pieces)
            self.selPiece = None

            self.transistionTurn()

            print('An available square was selected!')

        # Old player piece selected again, or unavailbe square selected
        else:
            if (self.selPiece is not None): # Dehighlight current selection
                self.clearSelection()
            
            self.selPiece = None
            print('Selected empty square')

    # Used for clearing selection highlight
    def clearSelection(self):
        row = self.selPiece.row
        col = self.selPiece.col
        square = self.board[row][col]['square']
        self.boardCanvas.itemconfig(square, fill= WHITE if ((row + col) % 2 == 0) else BLUE)

        moveTable = self.selPiece.moveTable
        for key in moveTable:
            row = moveTable[key]['row']
            col = moveTable[key]['col']
            square = self.board[row][col]['square']
            if ((row + col) % 2 == 0):
                self.boardCanvas.itemconfig(square, fill=DARK_WHITE)
            else:
                self.boardCanvas.itemconfig(square, fill=BLUE)

    def transistionTurn(self):
        self.isPlayerTurn = not self.isPlayerTurn

        for piece in self.pieces:
            if (self.pieces[piece].color == ('W' if self.isPlayerTurn else 'B')):
                self.pieces[piece].makeMoves(self.board)