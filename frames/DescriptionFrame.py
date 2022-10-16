import tkinter as tk
from Styles import *

############################
# Description Frame
############################


class DescriptionFrame(tk.Frame):
    def __init__(self, container):
        super().__init__(container)

        self.configure(borderwidth=2, relief="groove", bg=LIGHT, bd=0)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # label
        self.monsterLabel = tk.Label(self,
                                     text="Describe what type of monster you want",
                                     bg=LIGHT,
                                     font=(FONT, 14, "bold"),
                                     fg=BLACK,
                                     anchor="center")
        self.monsterLabel.grid(columnspan=2, row=0)

        # text input box
        self.monsterWindow = tk.Text(self, height=3, width=35, font=(FONT, 12),
                                     fg=BLACK, bg=WHITE)
        self.monsterWindow.grid(columnspan=2, row=1)
