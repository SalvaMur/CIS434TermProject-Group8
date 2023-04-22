from stockfish import Stockfish

class Bot:
    def __init__(self, difficulty):
        # self.stockfish = Stockfish(r'PUT STOCKFISH EXECUTABLE FILEPATH HERE')
        self.stockfish = Stockfish('.\\stockfish_15.1_win_x64_popcnt\\stockfish-windows-2022-x86-64-modern.exe') # FOR DEBUGGING, REMOVE FOR FINAL

        # Tuple entry notation: (row, col), used for mapping alg notation to 'Row x Col' notation
        self.algToCoord = {
            'a8': (1, 1), 'b8': (1, 2), 'c8': (1, 3), 'd8': (1, 4), 'e8': (1, 5), 'f8': (1, 6), 'g8': (1, 7), 'h8': (1, 8),
            'a7': (2, 1), 'b7': (2, 2), 'c7': (2, 3), 'd7': (2, 4), 'e7': (2, 5), 'f7': (2, 6), 'g7': (2, 7), 'h7': (2, 8),
            'a6': (3, 1), 'b6': (3, 2), 'c6': (3, 3), 'd6': (3, 4), 'e6': (3, 5), 'f6': (3, 6), 'g6': (3, 7), 'h6': (3, 8),
            'a5': (4, 1), 'b5': (4, 2), 'c5': (4, 3), 'd5': (4, 4), 'e5': (4, 5), 'f5': (4, 6), 'g5': (4, 7), 'h5': (4, 8),
            'a4': (5, 1), 'b4': (5, 2), 'c4': (5, 3), 'd4': (5, 4), 'e4': (5, 5), 'f4': (5, 6), 'g4': (5, 7), 'h4': (5, 8),
            'a3': (6, 1), 'b3': (6, 2), 'c3': (6, 3), 'd3': (6, 4), 'e3': (6, 5), 'f3': (6, 6), 'g3': (6, 7), 'h3': (6, 8),
            'a2': (7, 1), 'b2': (7, 2), 'c2': (7, 3), 'd2': (7, 4), 'e2': (7, 5), 'f2': (7, 6), 'g2': (7, 7), 'h2': (7, 8),
            'a1': (8, 1), 'b1': (8, 2), 'c1': (8, 3), 'd1': (8, 4), 'e1': (8, 5), 'f1': (8, 6), 'g1': (8, 7), 'h1': (8, 8)
        }

        # Set engine's difficulty based on chosen difficulty
        if (difficulty == 'Easy'):
            self.stockfish.set_skill_level(3)

        elif (difficulty == 'Normal'):
            self.stockfish.set_skill_level(10)

        elif (difficulty == 'Hard'):
            self.stockfish.set_skill_level(20)

        print('[BOT]: I\'M ALIVE!')

    # Get move from bot. Will return position of piece and position piece will move to as a tuple
    def getMove(self, board, turn):
        fenString = boardToFEN(board, turn) # Generate FEN string for bot
        self.stockfish.set_fen_position(fenString, False)

        # Get and parse move returned from bot
        move = self.stockfish.get_best_move()
        piecePos = move[0] + move[1]
        newPos = move[2] + move[3]

        # Get square positions in 'Row x Col' notation
        pieceSquare = self.algToCoord[piecePos]
        newSquare = self.algToCoord[newPos]

        print(f'[DEBUG]: {fenString}\n[DEBUG]: {move}') # FOR DEBUGGING

        piece = board[pieceSquare[0]][pieceSquare[1]]['piece']
        print(f'[BOT]: Moving {piece.color}_{piece.type} at {pieceSquare[0]}x{pieceSquare[1]} to {newSquare[0]}x{newSquare[1]}')

        return (pieceSquare, newSquare)

# Generate FEN string from board
def boardToFEN(board, turn):
    fenString = ''
    pieceToFEN = {
        'Pawn': 'p',
        'Knight': 'n',
        'Rook': 'r',
        'Bishop': 'b',
        'Queen': 'q',
        'King': 'k'
    }

    for row in board:
        emptySquares = 0

        for col in board[row]:

            # Square is empty
            if (board[row][col]['piece'] is None):
                emptySquares += 1

            # Square is not empty
            else:
                if (emptySquares != 0): # Append empty square number if not 0
                    fenString += str(emptySquares)
                    emptySquares = 0 # Reset empty squares

                isWhite = board[row][col]['pieceColor'] == 'W'
                type = board[row][col]['piece'].type

                # Add piece to FEN string
                fenString += pieceToFEN[type].upper() if (isWhite) else pieceToFEN[type]

        # If there are still empty squares, add to FEN string
        if (emptySquares != 0):
            fenString += str(emptySquares)

        # If not last row, append '/'
        if (row < 8):
            fenString += '/'

    fenString += f' b - - 0 {turn}' # Bot always plays black pieces

    return fenString