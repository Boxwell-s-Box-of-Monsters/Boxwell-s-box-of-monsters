import tkinter as tk
from styles import LIGHT, BLACK, FONT, TAN


############################
# Damage Type Frame
############################


class DamageTypeFrame(tk.Frame):
    def __init__(self, container):
        super().__init__(container)

        options = {'padx': 5, 'pady': 5}

        self.configure(borderwidth=2, relief="groove", bg=LIGHT, bd=0)

        # Drop Down for Dmg Types
        self.dmg_types = ["Acid", "Bludgeoning", "Cold", "Fire", "Lightning", "Necrotic",
                          "Piercing", "Poison", "Psychic", "Radiant", "Slashing", "Thunder"]
        self.dmg_var = tk.StringVar(self)
        self.dmg_drop_down = tk.OptionMenu(self, self.dmg_var, *self.dmg_types)
        self.dmg_drop_down.config(bg=LIGHT, font=(FONT, 8), fg=BLACK)
        self.dmg_drop_down.grid(column=0, row=0, **options)

        # Listed dmg types
        self.dmg_type_val = []
        self.dmg_label = tk.Label(self, text=self.dmg_type_val, font=(FONT, 8), bg=LIGHT,
                                  fg=BLACK)
        self.dmg_label.grid(column=0, row=1, columnspan=3, **options)

        # Buttons
        self.dmg_add_button = tk.Button(self,
                                        text='add dmg type',
                                        command=self.add_dmg_type,
                                        bg=TAN,
                                        font=(FONT, 8),
                                        fg=BLACK,
                                        highlightbackground=LIGHT)

        self.dmg_add_button.grid(column=1, row=0, **options)

        self.dmg_rmv_button = tk.Button(self,
                                        text='Remove dmg type',
                                        command=self.remove_dmg_type,
                                        bg=TAN,
                                        font=(FONT, 8),
                                        fg=BLACK,
                                        highlightbackground=LIGHT)
        self.dmg_rmv_button.grid(column=2, row=0, **options)

    def add_dmg_type(self):
        if self.dmg_var.get() not in self.dmg_type_val:
            self.dmg_type_val.append(self.dmg_var.get())
        self.dmg_label.config(text='\n'.join(str(x) for x in self.dmg_type_val))

    def remove_dmg_type(self):
        pass
