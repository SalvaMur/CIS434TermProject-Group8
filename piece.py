class Piece:
    def __init__(self, pieceRef, type, color, canvasRef, row, col):
        self.pieceRef = pieceRef
        self.type = type
        self.color = color
        self.canvasRef = canvasRef
        self.row = row
        self.col = col

        self.isFirstMove = True
        self.moveTable = {}

    def moveTo(self):
        None

    # WIP -------------------------------------------------
    def makeMoves(self, board):
        self.moveTable.clear()
        for i in board:
            for j in board[i]:
                if (board[i][j]['pieceColor'] == self.color):
                    continue
                
                self.moveTable[board[i][j]['squareTag']] = {'row': i, 'col': j}