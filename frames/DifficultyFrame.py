import tkinter as tk
from Styles import *

############################
# Terrain Frame
############################


class DifficultyFrame(tk.Frame):
    def __init__(self, container):
        super().__init__(container)

        # options = {'padx': 5, 'pady': 5}

        self.configure(borderwidth=2, relief="groove", bg=LIGHT, bd=0)

        self.diff = tk.IntVar()
        self.R1 = tk.Radiobutton(self, text="Easy", variable=self.diff, value=-1)
        self.R1.grid(row=0, column=0)
        self.R2 = tk.Radiobutton(self, text="Medium", variable=self.diff, value=0)
        self.R2.grid(row=0,column=1)
        self.R3 = tk.Radiobutton(self, text="Hard", variable=self.diff, value=1)
        self.R3.grid(row=0,column=2)
        self.R4 = tk.Radiobutton(self, text="Deadly", variable=self.diff, value=2)
        self.R4.grid(row=0,column=3)
