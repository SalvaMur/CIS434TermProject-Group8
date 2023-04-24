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
        for i in board:
            for j in board[i]:
                if (board[i][j]['pieceColor'] == self.color):
                    continue
                
                self.moveTable[board[i][j]['squareTag']] = {'row': i, 'col': j}