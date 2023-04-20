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
        self.defenses = []
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

        # Remove defenses
        print(self.defenses)
        for defense in self.defenses:
            print(defense)

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

# Child classes of Piece class

class Pawn(Piece):
    def __init__(self, pieceRef, pieceTag, color, canvasRef, row, col):
        super().__init__(pieceRef, pieceTag, 'Pawn', color, canvasRef, row, col)

    # Pawn's Move Generation =================================================================
    def makeMoves(self, board):
        self.moveTable.clear() # Clear old moves
        if (self.color == 'W'):
            # White pawn can move one up if no piece is blocking it
            # and if there is a square above it
            row = self.row - 1
            col = self.col
            
            if (row >= 1 and 
                board[row][col]['piece'] is None):

                squareTag = board[row][col]['squareTag']
                self.moveTable[squareTag] = {
                    'row': row,
                    'col': col
                }

            # White pawn can move two up on first move if nothing is blocking it
            if (self.isFirstMove):
                row = self.row - 2
                col = self.col

                if (board[self.row - 1][col]['piece'] is None and
                    board[row][col]['piece'] is None):

                    squareTag = board[row][col]['squareTag']
                    self.moveTable[squareTag] = {
                        'row': row,
                        'col': col
                    }

            # Handle white pawn attacking moves

            row = self.row - 1
            col = self.col - 1
            if (row >= 1 and col >= 1): # Left diagonal attack

                # Increase and set defenses
                board[row][col]['defensesByWhite'] += 1
                self.defenses.append(f'{row}x{col}')

                if (board[row][col]['pieceColor'] == 'B'): # Valid attack?

                    squareTag = board[row][col]['squareTag']
                    self.moveTable[squareTag] = {
                        'row': row,
                        'col': col
                    }

            
            row = self.row - 1
            col = self.col + 1
            if (row >= 1 and col <= 8): # Right diagonal attack

                # Increase and set defenses
                board[row][col]['defensesByWhite'] += 1
                self.defenses.append(f'{row}x{col}')

                if (board[row][col]['pieceColor'] == 'B'): # Valid attack?

                    squareTag = board[row][col]['squareTag']
                    self.moveTable[squareTag] = {
                        'row': row,
                        'col': col
                    }

        else: # Color is 'B'
            # Black pawn can move down one if no piece is blocking it
            # and if there is a square below it
            row = self.row + 1
            col = self.col

            if (row <= 8 and 
                board[row][col]['piece'] is None):

                squareTag = board[row][col]['squareTag']
                self.moveTable[squareTag] = {
                    'row': row,
                    'col': col
                }

            # Black pawn can move two down on first move if nothing is blocking it
            if (self.isFirstMove):
                row = self.row + 2
                col = self.col

                if (board[self.row + 1][col]['piece'] is None and 
                    board[row][col]['piece'] is None):

                    squareTag = board[row][col]['squareTag']
                    self.moveTable[squareTag] = {
                        'row': row,
                        'col': col
                    }

            # Handle black pawn attacking moves

            row = self.row + 1
            col = self.col - 1
            if (row <= 8 and col >= 1): # Left diagonal attack
                
                # Increase and set defenses
                board[row][col]['defensesByBlack'] += 1
                self.defenses.append(f'{row}x{col}')

                if (board[row][col]['pieceColor'] == 'W'): # Valid attack?

                    squareTag = board[row][col]['squareTag']
                    self.moveTable[squareTag] = {
                        'row': row,
                        'col': col
                    }

            row = self.row + 1
            col = self.col + 1
            if (row <= 8 and col <= 8): # Right diagonal attack

                # Increase and set defenses
                board[row][col]['defensesByBlack'] += 1
                self.defenses.append(f'{row}x{col}')
                print(self.defenses)

                if (board[row][col]['pieceColor'] == 'W'): # Valid attack?

                    squareTag = board[row][col]['squareTag']
                    self.moveTable[squareTag] = {
                        'row': row,
                        'col': col
                    }

class Knight(Piece):
    def __init__(self, pieceRef, pieceTag, color, canvasRef, row, col):
        super().__init__(pieceRef, pieceTag, 'Knight', color, canvasRef, row, col)

    # Knights's Move Generation ==============================================================
    def makeMoves(self, board):
        self.moveTable.clear()

class Rook(Piece):
    def __init__(self, pieceRef, pieceTag, color, canvasRef, row, col):
        super().__init__(pieceRef, pieceTag, 'Rook', color, canvasRef, row, col)

    # Rook's Move Generation =================================================================
    def makeMoves(self, board):
        self.moveTable.clear()

class Bishop(Piece):
    def __init__(self, pieceRef, pieceTag, color, canvasRef, row, col):
        super().__init__(pieceRef, pieceTag, 'Bishop', color, canvasRef, row, col)

    # Bishop's Move Generation ===============================================================
    def makeMoves(self, board):
        self.moveTable.clear()

class Queen(Piece):
    def __init__(self, pieceRef, pieceTag, color, canvasRef, row, col):
        super().__init__(pieceRef, pieceTag, 'Queen', color, canvasRef, row, col)

    # Queen's Move Generation ================================================================
    def makeMoves(self, board):
        self.moveTable.clear()
        for i in board:
            for j in board[i]:
                if (board[i][j]['pieceColor'] == self.color):
                    continue
                
                self.moveTable[board[i][j]['squareTag']] = {'row': i, 'col': j}

class King(Piece):
    def __init__(self, pieceRef, pieceTag, color, canvasRef, row, col):
        super().__init__(pieceRef, pieceTag, 'King', color, canvasRef, row, col)

    # King's Move Generation =================================================================
    def makeMoves(self, board):
        self.moveTable.clear()

    # Check if King is in check
    def inCheck(self):
        None

# Function that returns a piece based on parameters
def createPiece(pieceRef, pieceTag, type, color, canvasRef, row, col):
    if (type == 'Pawn'):
        return Pawn(pieceRef, pieceTag, color, canvasRef, row, col)

    elif (type == 'Knight'):
        return Knight(pieceRef, pieceTag, color, canvasRef, row, col)

    elif (type == 'Rook'):
        return Rook(pieceRef, pieceTag, color, canvasRef, row, col)

    elif (type == 'Bishop'):
        return Bishop(pieceRef, pieceTag, color, canvasRef, row, col)
        
    elif (type == 'Queen'):
        return Queen(pieceRef, pieceTag, color, canvasRef, row, col)

    elif (type == 'King'):
        return King(pieceRef, pieceTag, color, canvasRef, row, col)

    else:
        return