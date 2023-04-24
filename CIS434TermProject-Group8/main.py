import tkinter as tk
from tkinter import ttk
from chessboard import Chessboard

# Font styles
LARGE_FONT = 'Arial 40 bold'
MEDIUM_FONT = 'Arial 30'
BUTTON_FONT = 'Arial 14'
LIST_FONT = 'Arial 16'

# Colors
BLACK = '#000000'
GRAY = '#474747'
GREEN = '#6ba649'
WHITE = '#f0f1ff'
DARK_WHITE = '#e6e6e6'
LIME = '#9fe04f'
RED = '#e81a3c'
BLUE = '#3f59b5'

# Main menu screen frame
class MainMenu(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        self.master.geometry('800x600') # Change window geometry

        xOffset = (self.master.winfo_screenwidth() // 2) - (800 // 2)
        yOffset = (self.master.winfo_screenheight() // 2) - (600 // 2)
        self.master.geometry(f'+{xOffset}+{yOffset}') # Center window

        self.master['bg'] = GRAY
        self['bg'] = GREEN
        self.createMenu() # Create screen UI
        
    def createMenu(self):
        self.menuLabel = tk.Label(master=self, bg=GREEN, fg=WHITE, font=LARGE_FONT, pady=40)
        self.menuLabel['text'] = 'Very Basic Chess'
        self.menuLabel.pack()

        # Frame that holds buttons and dropdown list
        self.selFrame = tk.Frame(master=self, bg=GREEN, pady=40)

        # PVP game mode button
        self.pvp_button = tk.Button(master=self.selFrame, command=lambda: self.goToGame(False, None))
        self.pvp_button.configure(bg=LIME, fg=GRAY, font=BUTTON_FONT)
        self.pvp_button['text'] = 'Player vs Player'
        self.pvp_button.grid(row=0, column=0, padx=20)

        # Dropdown list of AI difficulty. Defaults to Normal
        self.botDifficulty_list = ttk.Combobox(master=self.selFrame, state='readonly', font=LIST_FONT)
        self.botDifficulty_list['values'] = ('Easy', 'Normal', 'Hard')
        self.botDifficulty_list.current(1)
        self.botDifficulty_list.grid(row=0, column=2, padx=20)

        # PVAI game mode button
        self.pvai_button = tk.Button(master=self.selFrame, command=lambda: self.goToGame(True, self.botDifficulty_list.get()))
        self.pvai_button.configure(bg=LIME, fg=GRAY, font=BUTTON_FONT)
        self.pvai_button['text'] = 'Player vs AI'
        self.pvai_button.grid(row=0, column=1, padx=20)

        # Pack selection frame to Menu screen
        self.selFrame.pack()

    def goToGame(self, againstBot, botDiff):
        GameScreen(master=self.master, playBot=againstBot, botDiff=botDiff).pack(expand=True, fill='both')
        self.destroy()

# Game screen frame
class GameScreen(tk.Frame):
    def __init__(self, master, playBot, botDiff):
        super().__init__(master)
        self.master = master

        # for player playing against bot
        self.playBot = playBot
        self.botDiff = botDiff

        self.master.geometry('1365x768') # Change window geometry

        xOffset = (self.master.winfo_screenwidth() // 2) - (1365 // 2)
        yOffset = (self.master.winfo_screenheight() // 2) - (768 // 2)
        self.master.geometry(f'+{xOffset}+{yOffset}') # Center window

        self.createGame() # Create screen UI
        
    def createGame(self):
        # The chessboard the game will be played on
        self.chessboard = Chessboard(master=self, playBot=self.playBot, botDiff=self.botDiff)
        self.chessboard.pack(expand=True, fill='both', side='left')
        self.chessboard.pack_propagate(0)

        # Game menu frame that holds game screen's buttons
        self.gameMenu = tk.Frame(master=self)
        self.gameMenu.configure(width=546, bg=GREEN)
        
        # Exit button
        self.exitButton = tk.Button(master=self.gameMenu, command=self.goToMenu)
        self.exitButton.configure(bg=RED, fg=WHITE, font=BUTTON_FONT)
        self.exitButton['text'] = 'Exit'
        self.exitButton.grid(row=0, column=0, padx=20)

        # Pack game menu frame in game screen
        self.gameMenu.pack(expand=True, fill='both', side='left')
        self.gameMenu.pack_propagate(0)
    
    def updateWinner(self, winner, loser, isDraw):

        # Update player stats for draw game
        if(isDraw):
            newScore = self.master.score
            newScore[winner]['ties'] += 1
            newScore[loser]['ties'] += 1

        # Update score
        else:
            newScore = self.master.score
            newScore[winner]['wins'] += 1
            newScore[loser]['losses'] += 1

        EndScreen(master=self.master, winner=winner, loser=loser, isDraw=isDraw, playBot=self.playBot, botDiff=self.botDiff).pack(expand=True)
        self.destroy()

    def goToMenu(self):
        MainMenu(master=self.master).pack(expand=True)
        self.destroy()

# End screen frame
class EndScreen(tk.Frame):
    def __init__(self, master, winner, loser, isDraw, playBot, botDiff):
        super().__init__(master)
        self.master = master
        self.master['bg'] = GRAY
        self['bg'] = GREEN

        # For rematch button
        self.playBot = playBot
        self.botDiff = botDiff

        self.isDraw = isDraw
        self.winner = winner
        self.loser = loser

        self.master.geometry('1365x768') # Change window geometry

        xOffset = (self.master.winfo_screenwidth() // 2) - (1365 // 2)
        yOffset = (self.master.winfo_screenheight() // 2) - (768 // 2)
        self.master.geometry(f'+{xOffset}+{yOffset}') # Center window

        self.createEndScreen()

    def createEndScreen(self):
        score = self.master.score
        p1Wins = score['player1']['wins']
        p1Loss = score['player1']['losses']
        p1Ties = score['player1']['ties']

        p2Wins = score['player2']['wins']
        p2Loss = score['player2']['losses']
        p2Ties = score['player2']['ties']

        bWins = score['bot']['wins']
        bLoss = score['bot']['losses']
        bTies = score['bot']['ties']

        self.result = tk.Label(master=self, bg=GREEN, fg=WHITE, font=LARGE_FONT, padx=40, pady=40)
        
        if (self.isDraw):
            self.result['text'] = 'Game ended in a Draw!'

        else:
            self.result['text'] = f'{self.winner} wins! {self.loser} loses!'

        self.result.pack()

        self.score = tk.Label(master=self, bg=GREEN, fg=WHITE, font=MEDIUM_FONT, padx=40, pady=40)
        self.score['text'] = f'Player 1: {p1Wins} Win(s), {p1Loss} Loss(es), {p1Ties} Tie(s)\n\n'
        self.score['text'] += f'Player 2: {p2Wins} Win(s), {p2Loss} Loss(es), {p2Ties} Tie(s)\n\n'
        self.score['text'] += f'Bot: {bWins} Win(s), {bLoss} Loss(es), {bTies} Tie(s)'
        self.score.pack()

        # Frame that holds buttons and dropdown list
        self.selFrame = tk.Frame(master=self, bg=GREEN, pady=40)

        # Menu button
        self.menuBtn = tk.Button(master=self.selFrame, command=self.goToMenu)
        self.menuBtn.configure(bg=LIME, fg=GRAY, font=BUTTON_FONT)
        self.menuBtn['text'] = 'Return To Menu'
        self.menuBtn.grid(row=0, column=0, padx=20)

        # Rematch button
        self.rematchBtn = tk.Button(master=self.selFrame, command=lambda: self.goToGame(self.playBot, self.botDiff))
        self.rematchBtn.configure(bg=LIME, fg=GRAY, font=BUTTON_FONT)
        self.rematchBtn['text'] = 'Rematch'
        self.rematchBtn.grid(row=0, column=1, padx=20)

        # Pack selection frame to Menu screen
        self.selFrame.pack()

    def goToGame(self, playBot, botDiff):
        GameScreen(master=self.master, playBot=playBot, botDiff=botDiff).pack(expand=True, fill='both')
        self.destroy()

    def goToMenu(self):
        MainMenu(master=self.master).pack(expand=True)
        self.destroy()

# Chess application class
class ChessApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Very Basic Chess')
        # self.resizable(width=False, height=False)
        self.score = {
            'player1': {
                'wins': 0, 'losses': 0, 'ties': 0
            },
            'player2': {
                'wins': 0, 'losses': 0, 'ties': 0
            },
            'bot': {
                'wins': 0, 'losses': 0, 'ties':0
            }
        }

        # Start with menu screen
        MainMenu(self).pack(expand=True)

if (__name__ == '__main__'):
    ChessApp().mainloop()
