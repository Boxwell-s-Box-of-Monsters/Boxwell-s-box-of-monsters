# Mock up of the monster generator
from audioop import add
import requests
import json
import tkinter as tk

window = tk.Tk()
window.geometry("700x500")
window.title("Monster Generator")

label = tk.Label(
    window, text="Welcome to the monster library, please enter a party with the format class level for each member.")
label.pack()
classes = ["Artificer", "Barbarian", "Bard", "Cleric", "Druid", "Fighter",
           "Monk", "Paladin", "Ranger", "Rogue", "Sorcerer", "Warlock", "Wizard"]

variable1 = tk.StringVar(window)
dropDownMenu1 = tk.OptionMenu(window, variable1, *classes)
dropDownMenu1.pack(pady=10)
variable2 = tk.StringVar(window)
dropDownMenu2 = tk.OptionMenu(window, variable2, *classes)
dropDownMenu2.pack(pady=10)
variable3 = tk.StringVar(window)
dropDownMenu3 = tk.OptionMenu(window, variable3, *classes)
dropDownMenu3.pack(pady=10)
variable4 = tk.StringVar(window)
dropDownMenu4 = tk.OptionMenu(window, variable4, *classes)
dropDownMenu4.pack(pady=10)


# create labels for character area

characterContainer = tk.Frame(window, borderwidth=2, relief="groove")
characterContainer.pack(pady=10)

addCharacter = tk.Button(characterContainer, text='Add Character')
removeCharacter = tk.Button(characterContainer, text="Remove Character")
addCharacter.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)
removeCharacter.grid(column=1, row=0, sticky=tk.W, padx=5, pady=5)


characterLabel = tk.Label(characterContainer, text="Character")
lvlLabel = tk.Label(characterContainer, text="Level")
damageLabel = tk.Label(characterContainer, text="Damage")
characterLabel.grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)
lvlLabel.grid(column=1, row=1, sticky=tk.W, padx=5, pady=5)
damageLabel.grid(column=2, row=1, sticky=tk.W, padx=5, pady=5)


characters = []
for i in range(4):
    characterRow = {}

    characterRow['character'] = tk.Label(characterContainer, text='Barbarian')
    characterRow['character'].grid(
        column=0, row=2 + i, sticky=tk.W, padx=5, pady=5)

    characterRow['level'] = tk.Label(characterContainer, text='50')
    characterRow['level'].grid(
        column=1, row=2 + i, sticky=tk.W, padx=5, pady=5)

    characterRow['Damage'] = tk.Label(characterContainer, text='Fire')
    characterRow['Damage'].grid(
        column=2, row=2 + i, sticky=tk.W, padx=5, pady=5)

    characters.append(characterRow)


result = tk.StringVar()
result.set("")


def button_action():
    response = requests.get("https://www.dnd5eapi.co/api/monsters/troll/")
    result.set(response.json().get('name'))
    print(response.json())


button = tk.Button(window, text='Get Monster', command=button_action)
button.pack(pady=10)

resultLabel = tk.Label(window, textvariable=result)
resultLabel.pack()

window.mainloop()
