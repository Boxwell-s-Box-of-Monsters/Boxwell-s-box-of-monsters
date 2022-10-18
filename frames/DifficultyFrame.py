import tkinter as tk
from Styles import *

############################
# Terrain Frame
############################


class DifficultyFrame(tk.Frame):
    def __init__(self, container):
        super().__init__(container)

        self.configure(borderwidth=2, relief="groove", bd=0, bg=TAN)
        
        self.grid_columnconfigure((0, 1, 2, 3), weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=3)
        
        self.label = tk.Label(self,
                              text="Difficulty",
                              fg=BLACK,
                              bg=TAN, 
                              anchor="center",
                              font=(FONT, 14, "bold"))
        self.label.grid(row=0, column=0, columnspan=4, sticky=tk.S)

        self.diff = tk.IntVar()
        self.R1 = tk.Radiobutton(self, text="Easy", variable=self.diff, value=0, bg=TAN)
        self.R1.grid(row=1, column=0, sticky=tk.N)
        self.R2 = tk.Radiobutton(self, text="Medium", variable=self.diff, value=1, bg=TAN)
        self.R2.grid(row=1,column=1, sticky=tk.N)
        self.R3 = tk.Radiobutton(self, text="Hard", variable=self.diff, value=2, bg=TAN)
        self.R3.grid(row=1,column=2, sticky=tk.N)
        self.R4 = tk.Radiobutton(self, text="Deadly", variable=self.diff, value=3, bg=TAN)
        self.R4.grid(row=1,column=3, sticky=tk.N)
