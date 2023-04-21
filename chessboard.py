import tkinter as tk
from copy import deepcopy
from piece import createPiece

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
PURPLE = '#e807ce'

class Chessboard(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self['width'] = 819
        self['bg'] = GRAY

        self.board = {} # Board for logic
        self.boardTK = {} # Board for GUI

        self.boardCanvas = tk.Canvas(master=self, width=712, height=712, bg=GREEN, borderwidth=0, highlightthickness=0)
        self.boardCanvas.pack(expand=True)
        self.boardCanvas.bind('<Button-1>', self.onClick)
        
        self.pieces = [] # Direct references to pieces
        self.piecesTK = {} # References to pieces on board for GUI
        self.squares = {} # References to squares on board with canvas tag for GUI
        self.w_King = None # Reference to white king
        self.b_King = None # Reference to black king
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
            self.boardTK[i+1] = {}

            for j in range(8): # Column
                xLeft = j * SQUARE_SIZE
                yTop = i * SQUARE_SIZE
                xRight = xLeft + SQUARE_SIZE
                yBottom = yTop + SQUARE_SIZE

                squareTag = self.boardCanvas.create_rectangle(xLeft, yTop, xRight, yBottom, outline='')
                square = self.boardCanvas.find_withtag(squareTag)[0]

                # Create board entry
                self.board[i+1][j+1] = {
                    'squareID': f'{i+1}x{j+1}', # Use this instead of 'squareTag' in 'self.boardTK'?
                    'piece': None,
                    'pieceColor': None
                }

                # Create TK board entry
                self.boardTK[i+1][j+1] = {
                    'square': square,
                    'squareTag': squareTag,
                    'center': {'x': (xRight-xLeft)/2 + xLeft, 'y': (yBottom-yTop)/2 + yTop},
                    'pieceRef': None,
                    'pieceTag': None
                }

                # Add square reference to 'self.squares'
                self.squares[squareTag] = {
                    'squareID': f'{i+1}x{j+1}',
                    'square': square
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
                    self.boardTK[i][j]['center']['x'], self.boardTK[i][j]['center']['y'], 
                    image=self.pieceImage[len(self.pieceImage) - 1]
                )
                pieceRef = self.boardCanvas.find_withtag(pieceTag)[0]

                piece = createPiece(startPos[i][j], color, i, j)

                self.pieces.append(piece)
                self.piecesTK[pieceTag] = piece

                self.board[i][j]['piece'] = piece
                self.board[i][j]['pieceColor'] = color

                self.boardTK[i][j]['pieceRef'] = pieceRef
                self.boardTK[i][j]['pieceTag'] = pieceTag

                if (startPos[i][j] == 'King' and color == 'W'):
                    self.w_King = piece

                elif (startPos[i][j] == 'King' and color == 'B'):
                    self.b_King = piece

        for piece in self.pieces:
            piece.makeMoves(self.board)

    def onClick(self, event):
        tag = self.boardCanvas.find_withtag('current')[0]

        # If player selected a piece
        if (tag in self.piecesTK):
            newPiece = self.piecesTK[tag]
        else:
            newPiece = None

        # If player selected a square
        if (tag in self.squares):
            selSquare = self.squares[tag]['squareID']
        else:
            selSquare = None

        # New player piece selected
        if (newPiece is not None and newPiece is not self.selPiece and 
            newPiece.color == ('W' if self.isPlayerTurn else 'B')):

            if (self.selPiece is not None): # Dehighlight previous piece
                self.clearSelection()
                row = self.selPiece.row
                col = self.selPiece.col
                oldSquare = self.boardTK[row][col]['square']
                self.boardCanvas.itemconfig(oldSquare, fill= DARK_WHITE if ((row + col) % 2 == 0) else BLUE)

            self.selPiece = newPiece
            newSquare = self.boardTK[self.selPiece.row][self.selPiece.col]['square']
            self.boardCanvas.itemconfig(newSquare, fill=LIME) # Highlight piece selected
            
            moveTable = self.selPiece.moveTable

            for move in moveTable:
                row = moveTable[move]['row']
                col = moveTable[move]['col']

                square = self.boardTK[row][col]['square']
                piece = self.board[row][col]['piece']

                # An enemy piece is present on square
                if (piece is not None):
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
        elif (self.selPiece is not None and (selSquare in self.selPiece.moveTable or 
                                            (newPiece is not None and self.board[newPiece.row][newPiece.col]['squareID'] in self.selPiece.moveTable))):
            
            if (selSquare in self.selPiece.moveTable):
                row = self.selPiece.moveTable[selSquare]['row']
                col = self.selPiece.moveTable[selSquare]['col']

            else:
                row = newPiece.row
                col = newPiece.col

            # MAYBE TURN BELOW INTO A METHOD?
            # ADD MORE HERE --------------------------------------------------------

            self.clearSelection()

            # FOR TEST ####################################################
            if (self.isPlayerTurn):
                if (self.b_King is self.board[row][col]['piece']):
                    self.b_King = None

            else:
                if (self.w_King is self.board[row][col]['piece']):
                    self.w_King = None

            ###############################################################

            x = self.boardTK[row][col]['center']['x']
            y = self.boardTK[row][col]['center']['y']

            self.movePiece(self.selPiece, row, col, x, y)
            self.selPiece = None

            self.transistionTurn()

            print('An available square was selected!')

        # Old player piece selected again, or unavailbe square selected
        else:
            if (self.selPiece is not None): # Dehighlight current selection
                self.clearSelection()
            
            self.selPiece = None
            print('Selected empty square')

    def movePiece(self, piece, newRow, newCol, x, y):
        oldRow = piece.row
        oldCol = piece.col
        piece.moveTo(newRow, newCol) # Update piece properties

        pieceRef = self.boardTK[oldRow][oldCol]['pieceRef']
        pieceTag = self.boardTK[oldRow][oldCol]['pieceTag']

        # Vacate old square on board and boardTK
        self.board[oldRow][oldCol]['piece'] = None
        self.board[oldRow][oldCol]['pieceColor'] = None
        self.boardTK[oldRow][oldCol]['pieceRef'] = None
        self.boardTK[oldRow][oldCol]['pieceTag'] = None

        # Enemy piece present on square, remove from all references
        if (self.board[newRow][newCol]['piece'] is not None):
            oldPieceTag = self.boardTK[newRow][newCol]['pieceTag']
            self.boardCanvas.delete(oldPieceTag)
            del self.piecesTK[oldPieceTag]
            
            oldPiece = self.board[newRow][newCol]['piece']
            self.pieces.remove(oldPiece)
            
        # Update new square this piece moved to
        self.board[newRow][newCol]['piece'] = piece
        self.board[newRow][newCol]['pieceColor'] = piece.color

        self.boardTK[newRow][newCol]['pieceRef'] = pieceRef
        self.boardTK[newRow][newCol]['pieceTag'] = pieceTag

        # Update board render to show piece on new square
        self.boardCanvas.coords(pieceRef, x, y)

    # Used for clearing selection highlight
    def clearSelection(self):
        row = self.selPiece.row
        col = self.selPiece.col
        square = self.boardTK[row][col]['square']
        self.boardCanvas.itemconfig(square, fill= DARK_WHITE if ((row + col) % 2 == 0) else BLUE)

        moveTable = self.selPiece.moveTable
        for key in moveTable:
            row = moveTable[key]['row']
            col = moveTable[key]['col']
            square = self.boardTK[row][col]['square']
            if ((row + col) % 2 == 0):
                self.boardCanvas.itemconfig(square, fill=DARK_WHITE)
            else:
                self.boardCanvas.itemconfig(square, fill=BLUE)

    # When turn ends
    def transistionTurn(self):

        # FOR TEST #####################################################
        if (self.isPlayerTurn):
            if (self.b_King is None):
                print('WHITE WINS')
                self.master.updateWinner('player1', 'player2')

        else:
            if (self.w_King is None):
                print('BLACK WINS')
                self.master.updateWinner('player2', 'player1')

        ###############################################################

        # Generate moves for current player first, then next player
        nextPieces = []
        for piece in self.pieces:
            if (self.isPlayerTurn and piece.color == 'W'):
                piece.makeMoves(self.board)
            
            elif (not self.isPlayerTurn and piece.color == 'B'):
                piece.makeMoves(self.board)

            else:
                nextPieces.append(piece)

        nextKing = self.b_King if (self.isPlayerTurn) else self.w_King
        for piece in nextPieces:
            piece.makeMoves(self.board) # Generate general moves

            # Restrict illegal moves
            enemies = list(filter(lambda enemy: enemy.color != nextKing.color, deepcopy(self.pieces)))
            piece.checkMoves(deepcopy(self.board), enemies, nextKing)

        self.isPlayerTurn = not self.isPlayerTurn # Transition turn
