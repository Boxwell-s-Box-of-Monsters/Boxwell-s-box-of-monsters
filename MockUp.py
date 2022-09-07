# Mock up of the monster generator
import requests
import json
import tkinter as tk

window = tk.Tk()
window.geometry("700x500")
window.title("Monster Generator")

label = tk.Label(window, text="Welcome to the monster library, please enter a party with the format class level for each member.")
label.pack()

#drop down for dmg types
dmgType = ["Acid", "Bludegeoning", "Cold", "Fire", "lightning", "necrotic", "piercing", "Poison", "Psychic", "Radiant", "Slashing", "Thunder"]
dmgVar = tk.StringVar(window)
dmgDropDown = tk.OptionMenu(window, dmgVar, *dmgType)
dmgDropDown.pack(pady=10)

#button for adding dmg type
dmgTypeVal = []
dmgLabel = tk.Label(window, text=dmgTypeVal)
dmgLabel.pack()
def dmgTypeAdd():
    tempDmg = dmgVar.get()
    if tempDmg not in dmgTypeVal:
        dmgTypeVal.append(dmgVar.get())
    dmgLabel.config(text=', '.join(str(x) for x in dmgTypeVal))
dmgAddButton = tk.Button(window, text='add dmg type', command = dmgTypeAdd)
dmgAddButton.pack(pady=10)


#button for removing dmg type, NOT IMPLMENTED, may implment if I have time Thursday
def dmgTypeRemove():
    print()
dmgRmvButton = tk.Button(window, text='Remove dmg type', command = dmgTypeRemove)
dmgRmvButton.pack(pady=10)


result = tk.StringVar()
result.set("")

def button_action():
    response = requests.get("https://www.dnd5eapi.co/api/monsters/troll/")
    result.set(response.json().get('name'))

button = tk.Button(window, text='Get Monster', command=button_action)
button.pack(pady=10)

resultLabel = tk.Label(window, textvariable=result)
resultLabel.pack()

window.mainloop()

