class Piece:
    def __init__(self, pieceRef, type, color, canvasRef, row, col):
        self.pieceRef = pieceRef
        self.type = type
        self.color = color
        self.canvasRef = canvasRef
        self.row = row
        self.col = col
        self.isFirstMove = True

    def moveTo(self):
        None