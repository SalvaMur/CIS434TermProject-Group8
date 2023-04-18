import tkinter as tk
from tkinter import ttk

# Font styles
LARGE_FONT = 'Arial 40 bold'
BUTTON_FONT = 'Arial 14'
LIST_FONT = 'Arial 16'

# Colors
BLACK = '#000000'
GRAY = '#474747'
GREEN = '#6ba649'
WHITE = '#f0f1ff'
LIME = '#9fe04f'
RED = '#e81a3c'

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
        
class Chessboard(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self['width'] = 819
        self['bg'] = GRAY

        self.createBoard()

    def createBoard(self):
        self.board = tk.Canvas(master=self, width=700, height=700, bg=GREEN)
        self.board.pack(expand=True)



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

        # Packe game menu frame in game screen
        self.gameMenu.pack(expand=True, fill='both', side='left')
        self.gameMenu.pack_propagate(0)
    
    def goToMenu(self):
        MainMenu(master=self.master).pack(expand=True)
        self.destroy()

# Chess application class
class ChessApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Very Basic Chess')
        #self.resizable(width=False, height=False)
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
