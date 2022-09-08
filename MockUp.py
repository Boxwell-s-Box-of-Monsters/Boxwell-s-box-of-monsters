# Mock up of the monster generator
from audioop import add
import requests
import tkinter as tk


# Create the window
window = tk.Tk()
window.geometry("325x610")
window.title("Monster Generator")

# Add the top label
infoText = "Welcome to the monster library, please enter the relevant information below."
label = tk.Label(window, text=infoText, wraplength=350, justify="center")
label.grid(column=0, row=0, padx=5, pady=5)

# Create the terrain container
terrainContainer = tk.Frame(window, borderwidth=2, relief="groove")
terrainContainer.grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)
terrainDescriptor = "Terrain Description: "
terrainLabel = tk.Label(terrainContainer, text = terrainDescriptor)
terrainLabel.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)

terrainInput = tk.Text(terrainContainer, height = 1, width = 10)
terrainInput.grid(column=1, row=0, sticky=tk.W, padx=5, pady=5)

# Create the character area
characterContainer = tk.Frame(window, borderwidth=2, relief="groove")
characterContainer.grid(column=0, row=2, sticky=tk.W, padx=5, pady=5)

characterContainerLabel = "Adventuring Party"
characterContainerLabel = tk.Label(characterContainer, text = characterContainerLabel)
characterContainerLabel.grid(column=0, row=0, padx=5, pady=5, columnspan=3)

addCharacter = tk.Button(characterContainer, text='Add Character')
removeCharacter = tk.Button(characterContainer, text="Remove Character")
addCharacter.grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)
removeCharacter.grid(column=1, row=1, sticky=tk.W, padx=5, pady=5)

characterLabel = tk.Label(characterContainer, text="Character")
lvlLabel = tk.Label(characterContainer, text="Level")
damageLabel = tk.Label(characterContainer, text="Damage")
characterLabel.grid(column=0, row=2, sticky=tk.W, padx=5, pady=5)
lvlLabel.grid(column=1, row=2, sticky=tk.W, padx=5, pady=5)
damageLabel.grid(column=2, row=2, sticky=tk.W, padx=5, pady=5)

# Add 4 predetermined characters to the list
characters = []
for i in range(4):
    characterRow = {}

    characterRow['character'] = tk.Label(characterContainer, text='Barbarian')
    characterRow['character'].grid(
        column=0, row=3 + i, sticky=tk.W, padx=5, pady=5)

    characterRow['level'] = tk.Label(characterContainer, text='50')
    characterRow['level'].grid(
        column=1, row=3 + i, sticky=tk.W, padx=5, pady=5)

    characterRow['Damage'] = tk.Label(characterContainer, text='Fire')
    characterRow['Damage'].grid(
        column=2, row=3 + i, sticky=tk.W, padx=5, pady=5)

    characters.append(characterRow)

# Create the damage container
damageContainer = tk.Frame(window, borderwidth=2, relief="groove")
damageContainer.grid(column=0, row=3, sticky=tk.W, padx=5, pady=5)

# Drop down for dmg types
dmgType = ["Acid", "Bludegeoning", "Cold", "Fire", "Lightning", "Necrotic", "Piercing", "Poison", "Psychic", "Radiant", "Slashing", "Thunder"]
dmgVar = tk.StringVar(damageContainer)
dmgDropDown = tk.OptionMenu(damageContainer, dmgVar, *dmgType)
dmgDropDown.grid(column=0, row=0, padx=5, pady=5)

#button for adding dmg type
dmgTypeVal = []
dmgLabel = tk.Label(damageContainer, text=dmgTypeVal)
dmgLabel.grid(column=0, row=1, padx=5, pady=5, columnspan=3)

# Button/button response for adding damage types
def dmgTypeAdd():
    tempDmg = dmgVar.get()
    if tempDmg not in dmgTypeVal:
        dmgTypeVal.append(dmgVar.get())
    dmgLabel.config(text=' '.join(str(x) for x in dmgTypeVal))
dmgAddButton = tk.Button(damageContainer, text='add dmg type', command = dmgTypeAdd)
dmgAddButton.grid(column=1, row=0, padx=5, pady=5)


#button for removing dmg type, NOT IMPLMENTED, may implment if I have time Thursday
def dmgTypeRemove():
    print()
dmgRmvButton = tk.Button(damageContainer, text='Remove dmg type', command = dmgTypeRemove)
dmgRmvButton.grid(column=2, row=0, padx=5, pady=5)

# Create monster description search field
monsterDescriptionContainer = tk.Frame(window, borderwidth=2, relief="groove")
monsterDescriptionContainer.grid(column=0, row=4, sticky=tk.W, padx=5, pady=5)

monsterDescriptor = "Describe what type of monster you want"
monsterLabel = tk.Label(monsterDescriptionContainer, text = monsterDescriptor)
monsterLabel.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)

monsterWindow = tk.Text(monsterDescriptionContainer, height = 3, width = 35)
monsterWindow.grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)

# Add the monster button/button response
monsterNum = [0];
result = tk.StringVar()
result.set("")

def button_action(monsterNum):
    response = "delete me after the mockup!"
    if monsterNum[0] == 0 :
        response = requests.get("https://www.dnd5eapi.co/api/monsters/troll/")
        monsterNum[0] += 1;
    elif monsterNum[0] == 1 :
        response = requests.get("https://www.dnd5eapi.co/api/monsters/medusa/")
        monsterNum[0] += 1
    else :
        response = requests.get("https://www.dnd5eapi.co/api/monsters/roc/")
    responseText = response.json().get('name') 
    responseText += "\nHP: " + str(response.json().get('hit_points'))
    responseText += "\tAC: " + str(response.json().get('armor_class'))
    responseText += "\tCR: " + str(response.json().get('challenge_rating'))
    responseText += "\nStr: " + str(response.json().get('strength'))
    responseText += "\tDex: " + str(response.json().get('dexterity'))
    responseText += "\tCon: " + str(response.json().get('constitution'))
    responseText += "\tInt: " + str(response.json().get('intelligence'))
    responseText += "\tWis: " + str(response.json().get('wisdom'))
    responseText += "\tCha: " + str(response.json().get('charisma'))
    result.set(responseText)

button = tk.Button(window, text='Get Monster', command= lambda: button_action(monsterNum))
button.grid(column=0, row=6)

# Print the result of the button
resultLabel = tk.Label(window, textvariable=result)
resultLabel.grid(column=0, row=7)

# Run the window
window.mainloop()

