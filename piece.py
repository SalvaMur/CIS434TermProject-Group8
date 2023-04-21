class Piece:
    def __init__(self, type, color, row, col):
        self.type = type
        self.color = color
        self.row = row
        self.col = col

        self.isFirstMove = True
        self.moveTable = {}

    def makeMoves(self, board):
        self.moveTable.clear() # Clear old moves

    # Simulate moves and check if move will put 'myKing' in check
    def checkMoves(self, board, pieces, myKing):
        kingSquare = board[myKing.row][myKing.col]['squareID']
        oldRow = self.row
        oldCol = self.col

        toDel = [] # Keep a list of moves to remove from 'self.moveTable'
        for move in self.moveTable:
            newRow = self.moveTable[move]['row']
            newCol = self.moveTable[move]['col']

            oldPiece = board[newRow][newCol]['piece']
            oldColor = board[newRow][newCol]['pieceColor']

            # Vacate old square
            board[oldRow][oldCol]['piece'] = None
            board[oldRow][oldCol]['pieceColor'] = None

            # Update new square
            board[newRow][newCol]['piece'] = self
            board[newRow][newCol]['pieceColor'] = self.color

            # Check if an enemy piece can check 'myKing' after simulated move
            for piece in pieces:
                if (newRow == piece.row and newCol == piece.col): # If piece was taken by simulated move, skip it
                    print(f'[SIM]: {piece.color}_{piece.type} can be taken by {self.color}_{self.type} at {newRow}x{newCol}.')
                    continue

                piece.makeMoves(board) # Simulate enemy moves

                if (kingSquare in piece.moveTable):
                    toDel.append(move)
                    print(f'[SIM]: {piece.color}_{piece.type} can check {myKing.color}_King from {self.color}_{self.type}\'s move to {newRow}x{newCol}!')

            # Revert potential move spot back for further simulations
            board[newRow][newCol]['piece'] = oldPiece
            board[newRow][newCol]['pieceColor'] = oldColor

            # Revert old square back for further simulations
            board[oldRow][oldCol]['piece'] = self
            board[oldRow][oldCol]['pieceColor'] = self.color

        for move in toDel:
            del self.moveTable[move]

    def addMove(self, board, row, col):
        squareID = board[row][col]['squareID']
        self.moveTable[squareID] = {
            'row': row,
            'col': col
        }

    def moveTo(self, row, col):
        # Update piece's properties
        self.row = row
        self.col = col
        self.isFirstMove = False

# Child classes of Piece class

class Pawn(Piece):
    def __init__(self, color, row, col):
        super().__init__('Pawn', color, row, col)

    # Pawn's Move Generation ===========================================================================================================
    def makeMoves(self, board):
        super().makeMoves(board) # General handler for creating moves

        if (self.color == 'W'):
            # White pawn can move one up if no piece is blocking it
            # and if there is a square above it
            row = self.row - 1
            col = self.col
            
            if (row >= 1 and board[row][col]['piece'] is None):
                self.addMove(board, row, col) # Add move to move table

            # White pawn can move two up on first move if nothing is blocking it
            if (self.isFirstMove):
                row = self.row - 2
                col = self.col

                if (board[self.row - 1][col]['piece'] is None and board[row][col]['piece'] is None):
                    self.addMove(board, row, col) # Add move to move table

            # Handle white pawn attacking moves

            row = self.row - 1
            col = self.col - 1
            if (row >= 1 and col >= 1): # Left diagonal attack
                if (board[row][col]['pieceColor'] == 'B'): # Valid attack?
                    self.addMove(board, row, col) # Add move to move table
            
            row = self.row - 1
            col = self.col + 1
            if (row >= 1 and col <= 8): # Right diagonal attack
                if (board[row][col]['pieceColor'] == 'B'): # Valid attack?
                    self.addMove(board, row, col) # Add move to move table

        else: # Color is 'B'
            # Black pawn can move down one if no piece is blocking it
            # and if there is a square below it
            row = self.row + 1
            col = self.col

            if (row <= 8 and board[row][col]['piece'] is None):
                self.addMove(board, row, col) # Add move to move table

            # Black pawn can move two down on first move if nothing is blocking it
            if (self.isFirstMove):
                row = self.row + 2
                col = self.col

                if (board[self.row + 1][col]['piece'] is None and board[row][col]['piece'] is None):
                    self.addMove(board, row, col) # Add move to move table

            # Handle black pawn attacking moves

            row = self.row + 1
            col = self.col - 1
            if (row <= 8 and col >= 1): # Left diagonal attack
                if (board[row][col]['pieceColor'] == 'W'): # Valid attack?
                    self.addMove(board, row, col) # Add move to move table

            row = self.row + 1
            col = self.col + 1
            if (row <= 8 and col <= 8): # Right diagonal attack
                if (board[row][col]['pieceColor'] == 'W'): # Valid attack?
                    self.addMove(board, row, col) # Add move to move table

class Knight(Piece):
    def __init__(self, color, row, col):
        super().__init__('Knight', color, row, col)

    # Knights's Move Generation ========================================================================================================
    def makeMoves(self, board):
        super().makeMoves(board) # General handler for creating moves

        row = self.row - 2 # Two squares up
        col = self.col - 1 # One square left
        if (row >= 1 and col >= 1):
            if (board[row][col]['pieceColor'] != self.color): # Valid move if empty square or enemy piece
                self.addMove(board, row, col) # Add move to move table

        row = self.row - 2 # Two squares up
        col = self.col + 1 # One square right
        if (row >= 1 and col <= 8):
            if (board[row][col]['pieceColor'] != self.color): # Valid move if empty square or enemy piece
                self.addMove(board, row, col) # Add move to move table

        row = self.row + 2 # Two squares down
        col = self.col + 1 # One square right
        if (row <= 8 and col <= 8):
            if (board[row][col]['pieceColor'] != self.color): # Valid move if empty square or enemy piece
                self.addMove(board, row, col) # Add move to move table

        row = self.row + 2 # Two squares down
        col = self.col - 1 # One square left
        if (row <= 8 and col >= 1):
            if (board[row][col]['pieceColor'] != self.color): # Valid move if empty square or enemy piece
                self.addMove(board, row, col) # Add move to move table

        row = self.row - 1 # One square up
        col = self.col - 2 # Two squares left
        if (row >= 1 and col >= 1):
            if (board[row][col]['pieceColor'] != self.color): # Valid move if empty square or enemy piece
                self.addMove(board, row, col) # Add move to move table

        row = self.row - 1 # One square up
        col = self.col + 2 # Two squares right
        if (row >= 1 and col <= 8):
            if (board[row][col]['pieceColor'] != self.color): # Valid move if empty square or enemy piece
                self.addMove(board, row, col) # Add move to move table

        row = self.row + 1 # One square down
        col = self.col - 2 # Two squares left
        if (row <= 8 and col >= 1):
            if (board[row][col]['pieceColor'] != self.color): # Valid move if empty square or enemy piece
                self.addMove(board, row, col) # Add move to move table

        row = self.row + 1 # One square down
        col = self.col + 2 # Two squares right
        if (row <= 8 and col <= 8):
            if (board[row][col]['pieceColor'] != self.color): # Valid move if empty square or enemy piece
                self.addMove(board, row, col) # Add move to move table

class Rook(Piece):
    def __init__(self, color, row, col):
        super().__init__('Rook', color, row, col)

    # Rook's Move Generation ===========================================================================================================
    def makeMoves(self, board):
        super().makeMoves(board) # General handler for creating moves

        # Move up
        for x in range (self.row - 1, 0, -1):
            row = x
            col = self.col

            if (board[row][col]['piece'] is None):
                self.addMove(board, row, col) # Add move to move table

            elif (board[row][col]['pieceColor'] != self.color):
                self.addMove(board, row, col) # Add move to move table
                break

            elif (board[row][col]['pieceColor'] == self.color):
                break

        # Move down
        for x in range (self.row + 1, 9):
            row = x
            col = self.col

            if (board[row][col]['piece'] is None):
                self.addMove(board, row, col) # Add move to move table

            elif (board[row][col]['pieceColor'] != self.color):
                self.addMove(board, row, col) # Add move to move table
                break

            elif (board[row][col]['pieceColor'] == self.color):
                break

        # Move right
        for x in range (self.col + 1, 9):
            row = self.row
            col = x

            if (board[row][col]['piece'] is None):
                self.addMove(board, row, col) # Add move to move table

            elif (board[row][col]['pieceColor'] != self.color):
                self.addMove(board, row, col) # Add move to move table
                break

            elif (board[row][col]['pieceColor'] == self.color):
                break

        # Move left
        for x in range (self.col - 1, 0, -1):
            row = self.row
            col = x

            if (board[row][col]['piece'] is None):
                self.addMove(board, row, col) # Add move to move table

            elif (board[row][col]['pieceColor'] != self.color):
                self.addMove(board, row, col) # Add move to move table
                break

            elif (board[row][col]['pieceColor'] == self.color):
                break

class Bishop(Piece):
    def __init__(self, color, row, col):
        super().__init__('Bishop', color, row, col)

    # Bishop's Move Generation =========================================================================================================
    def makeMoves(self, board):
        super().makeMoves(board) # General handler for creating moves

        # Upper-Left diagonal
        for x in range (1, 9):
            row = self.row - x
            col = self.col - x
            if (row >= 1 and col >= 1):
                if (board[row][col]['piece'] is None):
                    self.addMove(board, row, col) # Add move to move table
                    
                elif (board[row][col]['pieceColor'] != self.color):
                    self.addMove(board, row, col) # Add move to move table
                    break

                elif (board[row][col]['pieceColor'] == self.color):
                    break
        
        # Lower-Left diagonal
        for x in range (1, 9):
            row = self.row + x
            col = self.col - x
            if (row <= 8 and col >= 1):
                if (board[row][col]['piece'] is None):
                    self.addMove(board, row, col) # Add move to move table

                elif (board[row][col]['pieceColor'] != self.color):
                    self.addMove(board, row, col) # Add move to move table
                    break

                elif (board[row][col]['pieceColor'] == self.color):
                    break

        # Upper-Right diagonal
        for x in range (1, 9):
            row = self.row - x
            col = self.col + x
            if (row >= 1 and col <= 8):
                if (board[row][col]['piece'] is None):
                    self.addMove(board, row, col) # Add move to move table

                elif (board[row][col]['pieceColor'] != self.color):
                    self.addMove(board, row, col) # Add move to move table
                    break

                elif (board[row][col]['pieceColor'] == self.color):
                    break
        
        # Lower-Right diagonal
        for x in range (1, 9):
            row = self.row + x
            col = self.col + x
            if (row <= 8 and col <= 8):
                if (board[row][col]['piece'] is None):
                    self.addMove(board, row, col) # Add move to move table

                elif (board[row][col]['pieceColor'] != self.color):
                    self.addMove(board, row, col) # Add move to move table
                    break

                elif (board[row][col]['pieceColor'] == self.color):
                    break

class Queen(Piece):
    def __init__(self, color, row, col):
        super().__init__('Queen', color, row, col)

    # Queen's Move Generation ==========================================================================================================
    def makeMoves(self, board):
        super().makeMoves(board) # General handler for creating moves

        # Move up
        for x in range (self.row - 1, 0, -1):
            row = x
            col = self.col

            if (board[row][col]['piece'] is None):
                self.addMove(board, row, col) # Add move to move table

            elif (board[row][col]['pieceColor'] != self.color):
                self.addMove(board, row, col) # Add move to move table
                break

            elif (board[row][col]['pieceColor'] == self.color):
                break

        # Move down
        for x in range (self.row + 1, 9):
            row = x
            col = self.col

            if (board[row][col]['piece'] is None):
                self.addMove(board, row, col) # Add move to move table

            elif (board[row][col]['pieceColor'] != self.color):
                self.addMove(board, row, col) # Add move to move table
                break

            elif (board[row][col]['pieceColor'] == self.color):
                break

        # Move right
        for x in range (self.col + 1, 9):
            row = self.row
            col = x

            if (board[row][col]['piece'] is None):
                self.addMove(board, row, col) # Add move to move table

            elif (board[row][col]['pieceColor'] != self.color):
                self.addMove(board, row, col) # Add move to move table
                break

            elif (board[row][col]['pieceColor'] == self.color):
                break

        # Move left
        for x in range (self.col - 1, 0, -1):
            row = self.row
            col = x

            if (board[row][col]['piece'] is None):
                self.addMove(board, row, col) # Add move to move table

            elif (board[row][col]['pieceColor'] != self.color):
                self.addMove(board, row, col) # Add move to move table
                break

            elif (board[row][col]['pieceColor'] == self.color):
                break

        # Upper-Left diagonal
        for x in range (1, 9):
            row = self.row - x
            col = self.col - x
            if (row >= 1 and col >= 1):
                if (board[row][col]['piece'] is None):
                    self.addMove(board, row, col) # Add move to move table
                    
                elif (board[row][col]['pieceColor'] != self.color):
                    self.addMove(board, row, col) # Add move to move table
                    break

                elif (board[row][col]['pieceColor'] == self.color):
                    break
        
        # Lower-Left diagonal
        for x in range (1, 9):
            row = self.row + x
            col = self.col - x
            if (row <= 8 and col >= 1):
                if (board[row][col]['piece'] is None):
                    self.addMove(board, row, col) # Add move to move table

                elif (board[row][col]['pieceColor'] != self.color):
                    self.addMove(board, row, col) # Add move to move table
                    break

                elif (board[row][col]['pieceColor'] == self.color):
                    break

        # Upper-Right diagonal
        for x in range (1, 9):
            row = self.row - x
            col = self.col + x
            if (row >= 1 and col <= 8):
                if (board[row][col]['piece'] is None):
                    self.addMove(board, row, col) # Add move to move table

                elif (board[row][col]['pieceColor'] != self.color):
                    self.addMove(board, row, col) # Add move to move table
                    break

                elif (board[row][col]['pieceColor'] == self.color):
                    break
        
        # Lower-Right diagonal
        for x in range (1, 9):
            row = self.row + x
            col = self.col + x
            if (row <= 8 and col <= 8):
                if (board[row][col]['piece'] is None):
                    self.addMove(board, row, col) # Add move to move table

                elif (board[row][col]['pieceColor'] != self.color):
                    self.addMove(board, row, col) # Add move to move table
                    break

                elif (board[row][col]['pieceColor'] == self.color):
                    break

class King(Piece):
    def __init__(self, color, row, col):
        super().__init__('King', color, row, col)

    # King's Move Generation ===========================================================================================================
    def makeMoves(self, board):
        super().makeMoves(board) # General handler for creating moves

        # Upper-Left diagonal attack
        row = self.row - 1
        col = self.col - 1

        if (row >= 1  and col >= 1):
            if (board[row][col]['pieceColor'] != self.color):
                self.addMove(board, row, col) # Add move to move table

        # Upper-Right diagonal attack
        row = self.row - 1
        col = self.col + 1

        if (row >= 1 and col <= 8):
            if (board[row][col]['pieceColor'] != self.color):
                self.addMove(board, row, col) # Add move to move table

        # Lower-Left diagonal attack
        row = self.row + 1
        col = self.col - 1

        if (row <= 8 and col >= 1):
            if (board[row][col]['pieceColor'] != self.color):
                self.addMove(board, row, col) # Add move to move table

        # Lower-Right diagonal attack
        row = self.row + 1
        col = self.col + 1

        if (row <= 8 and col <= 8):
            if (board[row][col]['pieceColor'] != self.color):
                self.addMove(board, row, col) # Add move to move table

        # Top adjacent attack
        row = self.row - 1
        col = self.col

        if (row >= 1):
            if (board[row][col]['pieceColor'] != self.color):
                self.addMove(board, row, col) # Add move to move table

        # Bottom adjacent attack
        row = self.row + 1
        col = self.col

        if (row <= 8):
            if (board[row][col]['pieceColor'] != self.color):
                self.addMove(board, row, col) # Add move to move table

        # Left adjacent attack
        row = self.row
        col = self.col - 1

        if (col >= 1):
            if (board[row][col]['pieceColor'] != self.color):
                self.addMove(board, row, col) # Add move to move table

        # Right adjacent attack
        row = self.row
        col = self.col + 1

        if (col <= 8):
            if (board[row][col]['pieceColor'] != self.color):
                self.addMove(board, row, col) # Add move to move table

    # Check if King is in check
    def inCheck(self):
        None

# Function that returns a piece based on parameters
def createPiece(type, color, row, col):
    if (type == 'Pawn'):
        return Pawn(color, row, col)

    elif (type == 'Knight'):
        return Knight(color, row, col)

    elif (type == 'Rook'):
        return Rook(color, row, col)

    elif (type == 'Bishop'):
        return Bishop(color, row, col)
        
    elif (type == 'Queen'):
        return Queen(color, row, col)

    elif (type == 'King'):
        return King(color, row, col)

    else:
        return
