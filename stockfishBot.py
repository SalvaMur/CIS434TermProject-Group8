from stockfish import Stockfish

class Bot:
    def __init__(self):
        self.stockfish = Stockfish(r'C:\stockfish_15.1_win_x64_popcnt\stockfish-windows-2022-x86-64-modern.exe') # FOR DEBUGGING, REMOVE FOR FINAL
        # self.stockfish = Stockfish(r'PUT STOCKFISH EXECUTABLE FILEPATH HERE')

        print('[BOT]: I\'M ALIVE!')