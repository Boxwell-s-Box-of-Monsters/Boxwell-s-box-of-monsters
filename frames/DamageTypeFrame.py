import tkinter as tk
from Styles import *


############################
# Damage Type Frame
############################


class DamageTypeFrame(tk.Frame):
    def __init__(self, container):
        super().__init__(container)

        options = {'padx': 5, 'pady': 5}

        self.configure(borderwidth=2, relief="groove", bg=LIGHT, bd=0)

        # Drop Down for Dmg Types
        self.dmgTypes = ["Acid", "Bludegeoning", "Cold", "Fire", "Lightning",
                         "Necrotic", "Piercing", "Poison", "Psychic", "Radiant", "Slashing", "Thunder"]
        self.dmgVar = tk.StringVar(self)
        self.dmgDropDown = tk.OptionMenu(self, self.dmgVar, *self.dmgTypes)
        self.dmgDropDown.config(bg=LIGHT, font=(FONT, 8), fg=BLACK)
        self.dmgDropDown.grid(column=0, row=0, **options)

        # Listed dmg types
        self.dmgTypeVal = []
        self.dmgLabel = tk.Label(self, text=self.dmgTypeVal, font=(FONT, 8), bg=LIGHT,
                                 fg=BLACK)
        self.dmgLabel.grid(column=0, row=1, columnspan=3, **options)

        # Buttons
        self.dmgAddButton = tk.Button(self,
                                      text='add dmg type',
                                      command=self.addDmgType,
                                      bg=TAN,
                                      font=(FONT, 8),
                                      fg=BLACK,
                                      highlightbackground=LIGHT)

        self.dmgAddButton.grid(column=1, row=0, **options)

        self.dmgRmvButton = tk.Button(self,
                                      text='Remove dmg type',
                                      command=self.removeDmgType,
                                      bg=TAN,
                                      font=(FONT, 8),
                                      fg=BLACK,
                                      highlightbackground=LIGHT)
        self.dmgRmvButton.grid(column=2, row=0, **options)

    def addDmgType(self):
        if self.dmgVar.get() not in self.dmgTypeVal:
            self.dmgTypeVal.append(self.dmgVar.get())
        self.dmgLabel.config(text='\n'.join(str(x) for x in self.dmgTypeVal))

    def removeDmgType():
        pass
