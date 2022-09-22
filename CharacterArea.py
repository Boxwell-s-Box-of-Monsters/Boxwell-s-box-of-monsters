import tkinter as tk
from Styles import *


def createCharacterArea(window: tk.Tk) -> tk.Frame:

    window.update()

    # Create the character area
    characterContainer = tk.Frame(
        window, borderwidth=2, relief="groove", bg=LIGHT)
    characterContainer.grid(column=0, row=2, sticky=tk.W, padx=5, pady=5)
    characterContainer.config(width=int(window.winfo_width() / 2))

    characterContainerLabel = "Adventuring Party"
    characterContainerLabel = tk.Label(
        characterContainer, text=characterContainerLabel, font=(FONT, 9, "bold"), background=LIGHT)
    characterContainerLabel.grid(column=0, row=0, padx=5, pady=5, columnspan=3)

    # addCharacter = tk.Button(
    #     characterContainer, text='Add Character', bg=TAN, font=(FONT, 8))
    # removeCharacter = tk.Button(
    #     characterContainer, text="Remove Character", bg=TAN, font=(FONT, 8))
    # addCharacter.grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)
    # removeCharacter.grid(column=1, row=1, sticky=tk.W, padx=5, pady=5)

    characterLabel = tk.Label(
        characterContainer, text="Character", bg=LIGHT, font=(FONT, 8, "bold"))
    lvlLabel = tk.Label(characterContainer, text="Level",
                        bg=LIGHT, font=(FONT, 8, "bold"))
    # damageLabel = tk.Label(characterContainer, text="Damage",
    #                        bg=LIGHT, font=(FONT, 8, "bold"))
    characterLabel.grid(column=0, row=2, sticky=tk.W, padx=5, pady=5)
    lvlLabel.grid(column=1, row=2, sticky=tk.W, padx=5, pady=5)
    # damageLabel.grid(column=2, row=2, sticky=tk.W, padx=5, pady=5)

    # Drop down for dmg types
    charType = ["Artificer", "Barbarian", "Bard", "Cleric", "Druid", "Fighter",
                "Monk", "Paladin", "Ranger", "Rogue", "Sorcerer", "Warlock", "Wizard"]

    # Add 4 predetermined characters to the list
    characters = []
    for i in range(4):
        characterRow = {}
        charVar = tk.StringVar(characterContainer)

        chrDropDown = tk.OptionMenu(
            characterContainer, charVar, *charType)
        chrDropDown.config(width=int(characterContainer.winfo_width() / 2))
        chrDropDown.grid(
            column=0, row=3 + i, sticky=tk.W, padx=5, pady=5)
        characterRow['characterDrop'] = chrDropDown
        characterRow['character'] = charVar

        characterRow['level'] = tk.Spinbox(characterContainer, from_=1, to=20)
        characterRow['level'].grid(
            column=1, row=3 + i, sticky=tk.W, padx=5, pady=5)

        # characterRow['Damage'] = tk.Label(
        #     characterContainer, text='Fire', font=(FONT, 8), bg=LIGHT)
        # characterRow['Damage'].grid(
        #     column=2, row=3 + i, sticky=tk.W, padx=5, pady=5)

        characters.append(characterRow)

    return characterContainer
