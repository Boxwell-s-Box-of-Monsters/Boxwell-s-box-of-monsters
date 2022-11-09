import tkinter as tk
from Styles import *

############################
# Description Frame
############################


class DescriptionFrame(tk.Frame):
    def __init__(self, container):
        super().__init__(container)

        self.configure(borderwidth=2, relief="groove", bg=LIGHT, bd=2)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=2)
        # label
        self.monsterLabel = tk.Label(self,
                                     text="Describe what type of monster you want",
                                     bg=LIGHT,
                                     font=(FONT, 12, "bold"),
                                     fg=BLACK,
                                     anchor="center")
        self.monsterLabel.grid(row=0, column=0, sticky=tk.S, pady=(0, 15))



        # text input box
        self.monsterWindow = tk.Text(self, font=(FONT, 12),
                                     fg=BLACK, bg=WHITE,
                                     height=5, width=35)
        self.monsterWindow.bind('<KeyPress>',self.validate)
        self.monsterWindow.grid(column=0, row=1, sticky=tk.NSEW, padx=5, pady=(0, 5))

    def validate(self, event):
        
        c = event.char
        valid_set = set([' ', ',', '\'', '/', '\\', '-'])
        valid_keysym = set(['BackSpace', 'Down', 'Left', 'Up', 'Right', 'Enter', 'Return', 'Delete'])
        #handle special keys case
        if event.keysym in valid_keysym:
            return True
        #check if character is both ascii or alnum
        if c not in valid_set and (not c.isalnum() or not c.isascii()):
            return 'break'
        return True
        