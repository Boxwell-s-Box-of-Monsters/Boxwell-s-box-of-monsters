import tkinter as tk
from Styles import *

############################
# Terrain Frame
############################


class DifficultyFrame(tk.Frame):
    def __init__(self, container):
        super().__init__(container)

        options = {'padx': 5, 'pady': 5}

        self.configure(borderwidth=2, relief="groove", bg=LIGHT, bd=0)

        diff = tk.IntVar()
        R1 = tk.Radiobutton(self, text="Easy", variable=diff, value=-1)
        R1.grid(row=0, column=0)
        R2 = tk.Radiobutton(self, text="Medium", variable=diff, value=0)
        R2.grid(row=0,column=1)
        R3 = tk.Radiobutton(self, text="Hard", variable=diff, value=1)
        R3.grid(row=0,column=2)
        R4 = tk.Radiobutton(self, text="Deadly", variable=diff, value=2)
        R4.grid(row=0,column=3)
       
