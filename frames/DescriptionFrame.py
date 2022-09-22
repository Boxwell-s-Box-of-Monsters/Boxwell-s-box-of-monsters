import tkinter as tk
from Styles import *

############################
# Description Frame
############################


class DescriptionFrame(tk.Frame):
    def __init__(self, container):
        super().__init__(container)

        options = {'padx': 5, 'pady': 5}

        self.configure(borderwidth=2, relief="groove", bg=LIGHT, bd=0)

        # label
        self.monsterLabel = tk.Label(self,
                                     text="Describe what type of monster you want",
                                     bg=LIGHT,
                                     font=(FONT, 9, "bold"),
                                     fg=BLACK)
        self.monsterLabel.grid(column=0, row=0, sticky=tk.W, **options)

        # text input box
        self.monsterWindow = tk.Text(self, height=3, width=35, font=(FONT, 8),
                                     fg=BLACK, bg=WHITE)
        self.monsterWindow.grid(column=0, row=1, sticky=tk.W, **options)
