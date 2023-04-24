class Piece:
    def __init__(self, pieceRef, pieceTag, type, color, canvasRef, row, col):
        self.pieceRef = pieceRef
        self.pieceTag = pieceTag
        self.type = type
        self.color = color
        self.canvasRef = canvasRef
        self.row = row
        self.col = col

        self.isFirstMove = True
        self.moveTable = {}

    def moveTo(self, row, col, xOffset, yOffset, board, pieces): # HANDLE DEFENDEDBY ------------
        # Vacate old square on board
        board[self.row][self.col]['piece'] = None
        board[self.row][self.col]['pieceRef'] = None
        board[self.row][self.col]['pieceTag'] = None
        board[self.row][self.col]['pieceColor'] = None

        # Update piece's properties
        self.row = row
        self.col = col
        self.isFirstMove = False

        # Enemy piece present on square, remove from all references
        if (board[row][col]['piece'] is not None): # HANDLE DEFENDEDBY ------------
            oldPieceTag = board[row][col]['pieceTag']
            self.canvasRef.delete(oldPieceTag)
            del pieces[oldPieceTag]
            
        # Update new square this piece moved to
        board[row][col]['piece'] = self
        board[row][col]['pieceRef'] = self.pieceRef
        board[row][col]['pieceTag'] = self.pieceTag
        board[row][col]['pieceColor'] = self.color

        # Update board render to show piece on new square
        self.canvasRef.coords(self.pieceRef, xOffset, yOffset)

    # WIP -------------------------------------------------
    def makeMoves(self, board):
        self.moveTable.clear()
        if self.color == "white":
            # Check if pawn can move forward 1 square
            if board[self.row - 1][self.col]['piece'] is None:
                self.moveTable[board[self.row - 1][self.col]['squareTag']] = {'row': self.row - 1, 'col': self.col}
                # Check if pawn can move forward 2 squares on first move
                if self.isFirstMove and board[self.row - 2][self.col]['piece'] is None:
                    self.moveTable[board[self.row - 2][self.col]['squareTag']] = {'row': self.row - 2, 'col': self.col}
            # Check if pawn can capture diagonally
            if self.col > 0 and board[self.row - 1][self.col - 1]['pieceColor'] == "black":
                self.moveTable[board[self.row - 1][self.col - 1]['squareTag']] = {'row': self.row - 1, 'col': self.col - 1}
            if self.col < 7 and board[self.row - 1][self.col + 1]['pieceColor'] == "black":
                self.moveTable[board[self.row - 1][self.col + 1]['squareTag']] = {'row': self.row - 1, 'col': self.col + 1}
        else: # for black pawn
            # Check if pawn can move forward 1 square
            if self.row < 7 and board[self.row + 1][self.col]['piece'] is None:
                self.moveTable[board[self.row + 1][self.col]['squareTag']] = {'row': self.row + 1, 'col': self.col}

                self.moveTable[board[self.row + 1][self.col]['squareTag']] = {'row': self.row + 1, 'col': self.col}
                # Check if pawn can move forward 2 squares on first move
                if self.isFirstMove and board[self.row + 2][self.col]['piece'] is None:
                    self.moveTable[board[self.row + 2][self.col]['squareTag']] = {'row': self.row + 2, 'col': self.col}

