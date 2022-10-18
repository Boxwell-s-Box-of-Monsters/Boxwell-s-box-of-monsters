import tkinter as tk
from Styles import *


############################
# Character Frame
############################

class CharacterFrame(tk.Frame):
    def __init__(self, container):
        super().__init__(container)

        self.characterLimit = 8

        options = {'padx': 2, 'pady': 2}

        self.configure(borderwidth=2, relief="groove", bg=LIGHT,
                       bd=2)

        self.grid_rowconfigure((3, 4, 5, 6, 7, 8, 9, 10), weight=1)

        # Character Container Label
        self.characterContainerLabel = tk.Label(self,
                                                text="Adventuring Party",
                                                font=(FONT, 12, "bold"),
                                                background=LIGHT,
                                                fg=BLACK,
                                                anchor="center")
        self.characterContainerLabel.grid(
            row=0, column=0, columnspan=3, pady=2, sticky=tk.S)

        # Add/Remove Buttons
        self.addCharacterBtn = tk.Button(self, text='Add Character', font=(FONT, 10),
                                      fg=BLACK, highlightbackground=LIGHT, command=self.addCharacter)
        self.removeCharacterBtn = tk.Button(self, text="Remove Character", font=(FONT, 10),
                                         fg=BLACK, highlightbackground=LIGHT, command=self.removeCharacter)
        self.addCharacterBtn.grid(column=0, row=1, sticky=tk.N, **options)
        self.removeCharacterBtn.grid(column=1, row=1, sticky=tk.N, **options)
        self.removeCharacterBtn['state'] = tk.DISABLED

        # Labels for Character table
        characterLabel = tk.Label(self, text="Character", bg=LIGHT, font=(FONT, 10, "bold"),
                                       fg=BLACK)
        lvlLabel = tk.Label(self, text="Level", bg=LIGHT, font=(FONT, 10, "bold"),
                                 fg=BLACK)
        damageLabel = tk.Label(self, text="Damage", bg=LIGHT, font=(FONT, 10, "bold"),
                                    fg=BLACK)
        characterLabel.grid(column=0, row=2, sticky=tk.S, **options)
        lvlLabel.grid(column=1, row=2, sticky=tk.S, **options)
        damageLabel.grid(column=2, row=2, sticky=tk.S, **options)

        # Drop down for dmg types
        self.charType = ["Artificer", "Barbarian", "Bard", "Cleric", "Druid", "Fighter",
                    "Monk", "Paladin", "Ranger", "Rogue", "Sorcerer", "Warlock", "Wizard"]
        self.damageTypes = ['Acid', 'Bludgeoning', 'Cold', 'Fire', 'Force', 'Lightning',
                    'Necrotic', 'Piercing', 'Poison', 'Psychic', 'Radiant', 'Slashing', 'Thunder']
        # Characters
        self.characters = []
        self.characters.append(self.createCharacterRow(0))

    # used by the character level spinbox to check that input is an int between 0 and 20
    def validateLvl(self, potentialInput):
        r = potentialInput.isdigit()
        if r:
            rangeCheck = int(potentialInput)
            if rangeCheck > 20 or rangeCheck < 0:
                r = False
        return r

    # used by add character button to create a new character entry area
    def addCharacter(self):
        self.characters.append(self.createCharacterRow(len(self.characters)))

        #check number of characters
        if len(self.characters) >= 8:
            #disable add character button
            self.addCharacterBtn['state'] = tk.DISABLED
        #make sure remove charactrer button is enabled
        self.removeCharacterBtn['state'] = tk.NORMAL

    # used to remove character button to remove the last character entry
    def removeCharacter(self):
        rowToDelete = self.characters[-1]

        #delete the 3 tkinter widgets so they dont get rendered anymore
        rowToDelete['characterDrop'].destroy()
        rowToDelete['level'].destroy()
        rowToDelete['damage'].destroy()

        self.characters.pop()
        #check number of characters
        if len(self.characters) <= 1:
            #disable remove character button
            self.removeCharacterBtn['state'] = tk.DISABLED

        #make sure add character button is now enabled
        self.addCharacterBtn['state'] = tk.NORMAL

    def createCharacterRow(self, i):
        characterRow = {}
        charVar = tk.StringVar(self)
        damageVar = tk.StringVar(self)

        chrDropDown = tk.OptionMenu(
            self, charVar, *self.charType)
        chrDropDown.config(bg=LIGHT, fg=BLACK)
        chrDropDown.grid(
            column=0, row=3 + i, sticky=tk.N, padx=2, pady=(2, 2))
        characterRow['characterDrop'] = chrDropDown
        characterRow['character'] = charVar

        characterRow['level'] = tk.Spinbox(
            self, fg=BLACK, bg=WHITE, from_=1, to=20, validate="key", width=2,
        validatecommand=(self.register(self.validateLvl), "%P"))
        characterRow['level'].grid(
            column=1, row=3 + i, sticky=tk.N, padx=2, pady=(0, 2))

        characterRow['damage'] = tk.OptionMenu(
            self, damageVar, *self.damageTypes)
        characterRow['damage'].config(bg=LIGHT, fg=BLACK)
        characterRow['damage'].grid(
            column=2, row=3 + i, sticky=tk.N, padx=2)

        return characterRow
