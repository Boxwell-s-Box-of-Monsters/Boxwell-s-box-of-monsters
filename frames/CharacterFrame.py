import tkinter as tk

from Styles import *


############################
# Character Frame
############################

class CharacterFrame(tk.Frame):
    def __init__(self, container):
        super().__init__(container)

        options = {'padx': 5, 'pady': 5}

        self.configure(borderwidth=2, relief="groove", bg=LIGHT,
                       bd=0)

        # Character Container Label
        self.characterContainerLabel = tk.Label(self,
                                                text="Adventuring Party",
                                                font=(FONT, 9, "bold"),
                                                background=LIGHT,
                                                fg=BLACK)
        self.characterContainerLabel.grid(
            column=0, row=0, columnspan=3, **options)

        # # Add/Remove Buttons
        # self.addCharacter = tk.Button(self, text='Add Character', font=(FONT, 8),
        #                               fg=BLACK, highlightbackground=LIGHT)
        # self.removeCharacter = tk.Button(self, text="Remove Character", font=(FONT, 8),
        #                                  fg=BLACK, highlightbackground=LIGHT)
        # self.addCharacter.grid(column=0, row=1, sticky=tk.W, **options)
        # self.removeCharacter.grid(column=1, row=1, sticky=tk.W, **options)

        # Labels for Character table
        self.characterLabel = tk.Label(self, text="Character", bg=LIGHT, font=(FONT, 8, "bold"),
                                       fg=BLACK)
        self.lvlLabel = tk.Label(self, text="Level", bg=LIGHT, font=(FONT, 8, "bold"),
                                 fg=BLACK)
        # self.damageLabel = tk.Label(self, text="Damage", bg=LIGHT, font=(FONT, 8, "bold"),
        #                             fg=BLACK)
        self.characterLabel.grid(column=0, row=2, sticky=tk.W, **options)
        self.lvlLabel.grid(column=1, row=2, sticky=tk.W, **options)
        # self.damageLabel.grid(column=2, row=2, sticky=tk.W, **options)

        # Drop down for dmg types
        charType = ["Artificer", "Barbarian", "Bard", "Cleric", "Druid", "Fighter",
                    "Monk", "Paladin", "Ranger", "Rogue", "Sorcerer", "Warlock", "Wizard"]
        # Characters
        self.characters = []
        for i in range(4):
            characterRow = {}
            charVar = tk.StringVar(self)

            chrDropDown = tk.OptionMenu(
                self, charVar, *charType)
            chrDropDown.config(width=int(self.winfo_width() / 2), bg=LIGHT)
            chrDropDown.grid(
                column=0, row=3 + i, sticky=tk.W, padx=5, pady=5)
            characterRow['characterDrop'] = chrDropDown
            characterRow['character'] = charVar

            characterRow['level'] = tk.Spinbox(
                self, fg=BLACK, bg=WHITE, from_=1, to=20, validate="key",
            validatecommand=(self.register(self.validateLvl), "%P"))
            characterRow['level'].grid(
                column=1, row=3 + i, sticky=tk.W, padx=5, pady=5)

            # characterRow['Damage'] = tk.Label(
            #     characterContainer, text='Fire', font=(FONT, 8), bg=LIGHT)
            # characterRow['Damage'].grid(
            #     column=2, row=3 + i, sticky=tk.W, padx=5, pady=5)

            self.characters.append(characterRow)

    # used by the character level spinbox to check that input is an int between 0 and 20
    def validateLvl(self, potentialInput):
        r = potentialInput.isdigit()
        if r:
            rangeCheck = int(potentialInput)
            if rangeCheck > 20 or rangeCheck < 0:
                r = False
        return r
