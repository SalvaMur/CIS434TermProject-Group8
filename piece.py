import tkinter as tk

class Piece:
    def __init__(self, pieceRef, type, color, canvasRef, row, col):
        self.pieceRef = pieceRef
        self.type = type
        self.owner = color
        self.canvasRef = canvasRef
        self.row = row
        self.col = col
        self.isFirstMove = True

        self.canvasRef.tag_bind(self.pieceRef, '<ButtonPress-1>', self.onSelect)

    def onSelect(self, event):
        print(f'{self.owner}_{self.type}, Row: {self.row}, Col: {self.col}')