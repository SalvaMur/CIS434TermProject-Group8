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
LIME = '#9fe04f'
RED = '#e81a3c'
BLUE = '#3f59b5'

class Chessboard(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self['width'] = 819
        self['bg'] = GRAY
        
        self.board = {}
        self.boardCanvas = tk.Canvas(master=self, width=712, height=712, bg=GREEN, borderwidth=0, highlightthickness=0)
        self.boardCanvas.pack(expand=True)
        
        self.pieces = {}
        
        self.createBoard()
        self.createPieces()

    # Construct 8x8 chessboard
    def createBoard(self):
        SQUARE_SIZE = 89
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

        self.imageRef = []
        for i in startPos:
            color = 'B' if (i <= 2) else 'W'
            for j in startPos[i]:
                self.imageRef.append(tk.PhotoImage(file=f'img/{color}_{startPos[i][j]}.png'))
                pieceTag = self.boardCanvas.create_image(
                    self.board[i][j]['center']['x'], self.board[i][j]['center']['y'], 
                    image=self.imageRef[len(self.imageRef) - 1]
                )
                piece = self.boardCanvas.find_withtag(pieceTag)[0]

                self.board[i][j]['piece'] = Piece(piece, startPos[i][j], color, self.boardCanvas, i, j)
                self.board[i][j]['pieceRef'] = piece
                self.board[i][j]['pieceName'] = startPos[i][j]
                self.board[i][j]['pieceColor'] = color

                if (startPos[i][j] == 'Rook'):
                    self.board[i][j]['defendedByBlack'] = False
                    self.board[i][j]['defendedByWhite'] = False