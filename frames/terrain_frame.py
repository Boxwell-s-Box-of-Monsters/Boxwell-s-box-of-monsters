import tkinter as tk
from styles import LIGHT, FONT, BLACK, WHITE


############################
# Terrain Frame
############################


class TerrainFrame(tk.Frame):
    def __init__(self, container):
        super().__init__(container)

        options = {'padx': 5, 'pady': 5}

        self.configure(borderwidth=2, relief="groove", bg=LIGHT, bd=0)

        # Terrain Label
        self.terrain_label = tk.Label(self,
                                      text="Terrain Description: ",
                                      background=LIGHT,
                                      font=(FONT, 8, "bold"),
                                      fg=BLACK)

        self.terrain_label.grid(column=0, row=0, sticky=tk.W, **options)

        # Terrain Input
        self.terrain_input = tk.Text(self, height=1, width=20, font=(FONT, 8),
                                     fg=BLACK, bg=WHITE)
        self.terrain_input.grid(column=1, row=0, sticky=tk.W, **options)
