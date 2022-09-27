import tkinter as tk
from styles import LIGHT, FONT, BLACK, WHITE


############################
# Description Frame
############################


class DescriptionFrame(tk.Frame):
    def __init__(self, container):
        super().__init__(container)

        options = {'padx': 5, 'pady': 5}

        self.configure(borderwidth=2, relief="groove", bg=LIGHT, bd=0)

        # label
        self.monster_label = tk.Label(self,
                                      text="Describe what type of monster you want",
                                      bg=LIGHT,
                                      font=(FONT, 9, "bold"),
                                      fg=BLACK)
        self.monster_label.grid(column=0, row=0, sticky=tk.W, **options)

        # text input box
        self.monster_window = tk.Text(self, height=3, width=35, font=(FONT, 8),
                                      fg=BLACK, bg=WHITE)
        self.monster_window.grid(column=0, row=1, sticky=tk.W, **options)
