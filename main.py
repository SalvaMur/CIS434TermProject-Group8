import tkinter as tk

# Main menu screen frame
class MainMenu(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        
        self.master.geometry('800x600') # Change window geometry
        self.createMenu()
        
    def createMenu(self):
        self.play_button = tk.Button(master=self, text='PLAY', command=self.goToGame)
        self.play_button.grid(row=0, column=0)
        
    def goToGame(self):
        GameScreen(master=self.master).pack()
        self.destroy()
        
# Game screen frame
class GameScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        self.master.geometry('1365x768') # Change window geometry
        self.createGame()
        
    def createGame(self):
        self.play_button = tk.Button(master=self, text='MENU', command=self.goToMenu)
        self.play_button.grid(row=0, column=0)
    
    def goToMenu(self):
        MainMenu(master=self.master).pack()
        self.destroy()

# Chess application class
class ChessApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Chess')
        self.resizable(width=False, height=False)
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
        MainMenu(self).pack()

if (__name__ == '__main__'):
    ChessApp().mainloop()
