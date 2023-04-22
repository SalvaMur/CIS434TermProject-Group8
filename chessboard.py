import tkinter as tk
from copy import deepcopy
from stockfishBot import Bot
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
    def __init__(self, master, playBot, botDiff):
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
        
        self.turn = 1 # The turn number. When player starts turn, increment turn number
        self.isPlayerTurn = True # Keep track of player turns
        self.playBot = playBot # Is player playing against bot?
        self.botDiff = botDiff # Difficulty chosen for bot

        # Initialize AI engine if playing against bot
        self.bot = Bot(self.botDiff) if (self.playBot) else None

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

    #######################################################################################################################################################################################
    # BOARD INTERACTION METHODS ###########################################################################################################################################################
    #######################################################################################################################################################################################

    def onClick(self, event):
        tag = self.boardCanvas.find_withtag('current')[0] # Get GUI tag for object clicked

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

            print(f'[INPUT]: Selected {self.selPiece.color}_{self.selPiece.type} at {self.selPiece.row}x{self.selPiece.col}')
        
        # Selected available square, or enemy piece on available square
        elif (self.selPiece is not None and (selSquare in self.selPiece.moveTable or 
                                            (newPiece is not None and self.board[newPiece.row][newPiece.col]['squareID'] in self.selPiece.moveTable))):
            
            if (selSquare in self.selPiece.moveTable):
                row = self.selPiece.moveTable[selSquare]['row']
                col = self.selPiece.moveTable[selSquare]['col']

            else:
                row = newPiece.row
                col = newPiece.col

            self.clearSelection() # Dehighlight selectable squares

            x = self.boardTK[row][col]['center']['x']
            y = self.boardTK[row][col]['center']['y']

            self.movePiece(self.selPiece, row, col, x, y) # Handle piece movement
            self.selPiece = None # Deselect piece

            self.transistionTurn() # Handle end of turn

            print(f'[INPUT]: Selected square at {row}x{col}')

        # Old player piece selected again, or unavailbe square selected
        else:
            if (self.selPiece is not None): # Dehighlight current selection
                self.clearSelection()
            
            self.selPiece = None
            print('[INPUT]: Selected empty square')

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

        # Generate moves for current player first, then next player
        nextPieces = []
        nextKing = self.b_King if (self.isPlayerTurn) else self.w_King
        nextKingSquare = self.board[nextKing.row][nextKing.col]['squareID']
        for piece in self.pieces:
            if (self.isPlayerTurn and piece.color == 'W'):
                piece.makeMoves(self.board)

                if (nextKingSquare in piece.moveTable):
                    nextKing.inCheck = True
            
            elif (not self.isPlayerTurn and piece.color == 'B'):
                piece.makeMoves(self.board)

                if (nextKingSquare in piece.moveTable):
                    nextKing.inCheck = True

            else:
                nextPieces.append(piece)

        canMove = []
        for piece in nextPieces:
            piece.makeMoves(self.board) # Generate general moves

            # Restrict illegal moves
            enemies = list(filter(lambda enemy: enemy.color != nextKing.color, deepcopy(self.pieces)))
            piece.checkMoves(deepcopy(self.board), enemies, nextKing)

            # If piece has moves, put piece into 'canMove' list
            if (len(piece.moveTable) != 0):
                canMove.append(piece)

        # If next player can't move any of their pieces, check for tie or loss
        if (len(canMove) == 0):

            # Find out who the winner, loser, and players are
            if (self.playBot):
                result = ('player1', 'bot') if (self.isPlayerTurn) else ('bot', 'player1')
            else:
                result = ('player1', 'player2') if (self.isPlayerTurn) else ('player2', 'player1')

            # Next player's king is currently in check
            if (nextKing.inCheck):
                print('[RESULT]: ', 'White Wins!' if (self.isPlayerTurn) else 'Black Wins!')
                self.master.updateWinner(result[0], result[1], False)

            # It is a draw
            else:
                print('[RESULT]: It is a draw!')
                self.master.updateWinner(result[0], result[1], True)

        self.isPlayerTurn = not self.isPlayerTurn # Transition turn

        # Increase turn number when player's turn starts
        if (self.isPlayerTurn):
            self.turn += 1

        # If playing against bot, handle bot's turn
        if (self.playBot and not self.isPlayerTurn):

            # [0][0] - Row, [0][1] - Col, [1][0] - newRow, [1][1] - newCol
            botMove = self.bot.getMove(self.board, self.turn)

            botPiece = self.board[botMove[0][0]][botMove[0][1]]['piece']
            newRow = botMove[1][0]
            newCol = botMove[1][1]

            x = self.boardTK[newRow][newCol]['center']['x'] 
            y = self.boardTK[newRow][newCol]['center']['y'] 

            # Move bot's piece to its selection
            self.movePiece(botPiece, newRow, newCol, x, y)

            # Transition turn back to player after bot is done
            self.transistionTurn()