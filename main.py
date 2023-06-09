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
        self.pvp_button = tk.Button(master=self.selFrame, command=self.goToGame)
        self.pvp_button.configure(bg=LIME, fg=GRAY, font=BUTTON_FONT)
        self.pvp_button['text'] = 'Player vs Player'
        self.pvp_button.grid(row=0, column=0, padx=20)

        # WIP -----------------------------------------------
        # PVAI game mode button
        self.pvai_button = tk.Button(master=self.selFrame, command=None)
        self.pvai_button.configure(bg=LIME, fg=GRAY, font=BUTTON_FONT)
        self.pvai_button['text'] = 'Player vs AI'
        self.pvai_button.grid(row=0, column=1, padx=20)

        # Dropdown list of AI difficulty. Defaults to Normal
        self.botDifficulty_list = ttk.Combobox(master=self.selFrame, state='readonly', font=LIST_FONT)
        self.botDifficulty_list['values'] = ('Easy', 'Normal', 'Hard')
        self.botDifficulty_list.current(1)
        self.botDifficulty_list.grid(row=0, column=2, padx=20)

        # Pack selection frame to Menu screen
        self.selFrame.pack()
        
    def goToGame(self):
        GameScreen(master=self.master).pack(expand=True, fill='both')
        self.destroy()

# Game screen frame
class GameScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        self.master.geometry('1365x768') # Change window geometry

        xOffset = (self.master.winfo_screenwidth() // 2) - (1365 // 2)
        yOffset = (self.master.winfo_screenheight() // 2) - (768 // 2)
        self.master.geometry(f'+{xOffset}+{yOffset}') # Center window

        self.createGame() # Create screen UI
        
    def createGame(self):
        # The chessboard the game will be played on
        self.chessboard = Chessboard(master=self)
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
    
    def updateWinner(self, winner, loser):
        # Update score
        newScore = self.master.score
        newScore[winner]['wins'] += 1
        newScore[loser]['losses'] += 1
        self.master.score = newScore

        EndScreen(master=self.master, winner=winner, loser=loser).pack(expand=True)
        self.destroy()

    def goToMenu(self):
        MainMenu(master=self.master).pack(expand=True)
        self.destroy()

# End screen frame
class EndScreen(tk.Frame):
    def __init__(self, master, winner, loser):
        super().__init__(master)
        self.master = master
        self.master['bg'] = GRAY
        self['bg'] = GREEN

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
        
        if self.winner == 'player1' and self.loser == 'player2':
            self.result['text'] = f'Player 1 wins! Player 2 losses!'
        elif self.winner == 'player2' and self.loser == 'player1':
            self.result['text'] = f'Player 2 wins! Player 1 losses!'
        elif self.winner == 'player1' and self.loser == 'bot':
            self.result['text'] = f'Player 1 wins! Bot losses!'
        elif self.winner == 'bot' and self.loser == 'player1':
            self.result['text'] = f'Bot wins! Player 1 losses!'
        self.result.pack()

        self.score = tk.Label(master=self, bg=GREEN, fg=WHITE, font=MEDIUM_FONT, padx=40, pady=40)
        if p1Wins == 1:
            self.score['text'] = f'Player 1: {p1Wins} Win, {p1Loss} Losses, {p1Ties} Ties\n'
        elif p1Loss == 1:
            self.score['text'] = f'Player 1: {p1Wins} Wins, {p1Loss} Loss, {p1Ties} Ties\n'
        elif p1Ties == 1:
            self.score['text'] = f'Player 1: {p1Wins} Wins, {p1Loss} Losses, {p1Ties} Tie\n'
        elif p1Wins == 1 and p1Loss == 1:
            self.score['text'] = f'Player 1: {p1Wins} Win, {p1Loss} Loss, {p1Ties} Ties\n'
        elif p1Wins == 1 and p1Ties == 1:
            self.score['text'] = f'Player 1: {p1Wins} Win, {p1Loss} Losses, {p1Ties} Tie\n'
        elif p1Loss == 1 and p1Ties == 1:
            self.score['text'] = f'Player 1: {p1Wins} Wins, {p1Loss} Loss, {p1Ties} Tie\n'
        elif p1Wins ==1 and p1Loss == 1 and p1Ties == 1:
            self.score['text'] = f'Player 1: {p1Wins} Win, {p1Loss} Losses, {p1Ties} Ties\n'
        else:
            self.score['text'] = f'Player 1: {p1Wins} Wins, {p1Loss} Losses, {p1Ties} Ties\n'
            
        if p2Wins == 1:
            self.score['text'] += f'Player 2: {p2Wins} Win, {p2Loss} Losses, {p2Ties} Ties\n'
        elif p2Loss == 1:
            self.score['text'] += f'Player 2: {p2Wins} Wins, {p2Loss} Loss, {p2Ties} Ties\n'
        elif p2Ties == 1:
            self.score['text'] += f'Player 2: {p2Wins} Wins, {p2Loss} Losses, {p2Ties} Tie\n'
        elif p2Wins == 1 and p2Loss == 1:
            self.score['text'] += f'Player 2: {p2Wins} Win, {p2Loss} Loss, {p2Ties} Ties\n'
        elif p2Wins == 1 and p2Ties == 1:
            self.score['text'] += f'Player 2: {p2Wins} Win, {p2Loss} Losses, {p2Ties} Tie\n'
        elif p2Loss == 1 and p2Ties == 1:
            self.score['text'] += f'Player 2: {p2Wins} Wins, {p2Loss} Loss, {p2Ties} Tie\n'
        elif p2Wins ==1 and p2Loss == 1 and p2Ties == 1:
            self.score['text'] += f'Player 2: {p2Wins} Win, {p2Loss} Loss, {p2Ties} Tie\n'
        else:
            self.score['text'] += f'Player 2: {p2Wins} Win(s), {p2Loss} Loss(es), {p2Ties} Tie(s)\n'
            
        if bWins == 1:
            self.score['text'] += f'Bot: {bWins} Win, {bLoss} Losses, {bTies} Ties'
        elif bLoss == 1:
            self.score['text'] += f'Bot: {bWins} Wins, {bLoss} Loss, {bTies} Ties'
        elif bTies == 1:
            self.score['text'] += f'Bot: {bWins} Wins, {bLoss} Losses, {bTies} Tie'
        elif bWins == 1 and bLoss == 1:
            self.score['text'] += f'Bot: {bWins} Win, {bLoss} Loss, {bTies} Ties'
        elif bWins == 1 and bTies == 1:
            self.score['text'] += f'Bot: {bWins} Win, {bLoss} Losses, {bTies} Tie'
        elif bLoss == 1 and bTies == 1:
            self.score['text'] += f'Bot: {bWins} Wins, {bLoss} Loss, {bTies} Tie'
        elif bWins ==1 and bLoss == 1 and bTies == 1:
            self.score['text'] += f'Bot: {bWins} Win, {bLoss} Loss, {bTies} Tie'
        else:
            self.score['text'] += f'Bot: {bWins} Wins, {bLoss} Losses, {bTies} Ties'

        self.score.pack()

        # Frame that holds buttons and dropdown list
        self.selFrame = tk.Frame(master=self, bg=GREEN, pady=40)

        # Menu button
        self.menuBtn = tk.Button(master=self.selFrame, command=self.goToMenu)
        self.menuBtn.configure(bg=LIME, fg=GRAY, font=BUTTON_FONT)
        self.menuBtn['text'] = 'Return To Menu'
        self.menuBtn.grid(row=0, column=0, padx=20)

        # Rematch button
        self.rematchBtn = tk.Button(master=self.selFrame, command=self.goToGame)
        self.rematchBtn.configure(bg=LIME, fg=GRAY, font=BUTTON_FONT)
        self.rematchBtn['text'] = 'Rematch'
        self.rematchBtn.grid(row=0, column=1, padx=20)

        # Pack selection frame to Menu screen
        self.selFrame.pack()

    def goToGame(self):
        GameScreen(master=self.master).pack(expand=True, fill='both')
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
