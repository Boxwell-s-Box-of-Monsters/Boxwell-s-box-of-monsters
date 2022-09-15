# Mock up of the monster generator
import requests
import tkinter as tk

# Colors
TAN = "#DDC3A2"
LIGHT = "#FFE4C4"
FONT = "helvetica"

# Create the window
window = tk.Tk()
window.geometry("325x610")
window.title("Monster Generator")
window.configure(bg=TAN)

# Add the top label
infoText = "Welcome to the monster library, please enter the relevant information below."
label = tk.Label(window, text=infoText, wraplength=300, justify="center", background=TAN, font=(FONT, 10, "bold"))
label.grid(column=0, row=0, padx=5, pady=5)

# Create the terrain container
terrainContainer = tk.Frame(window, borderwidth=2, relief="groove", bg=LIGHT)
terrainContainer.grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)
terrainDescriptor = "Terrain Description: "
terrainLabel = tk.Label(terrainContainer, text = terrainDescriptor, background=LIGHT, font=(FONT, 8, "bold"))
terrainLabel.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)

terrainInput = tk.Text(terrainContainer, height = 1, width = 20, font=(FONT, 8))
terrainInput.grid(column=1, row=0, sticky=tk.W, padx=5, pady=5)

# Create the character area
characterContainer = tk.Frame(window, borderwidth=2, relief="groove", bg=LIGHT)
characterContainer.grid(column=0, row=2, sticky=tk.W, padx=5, pady=5)

characterContainerLabel = "Adventuring Party"
characterContainerLabel = tk.Label(characterContainer, text = characterContainerLabel, font=(FONT, 9, "bold"), background=LIGHT)
characterContainerLabel.grid(column=0, row=0, padx=5, pady=5, columnspan=3)

addCharacter = tk.Button(characterContainer, text='Add Character', bg=TAN, font=(FONT, 8))
removeCharacter = tk.Button(characterContainer, text="Remove Character", bg=TAN, font=(FONT, 8))
addCharacter.grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)
removeCharacter.grid(column=1, row=1, sticky=tk.W, padx=5, pady=5)

characterLabel = tk.Label(characterContainer, text="Character", bg=LIGHT, font=(FONT, 8, "bold"))
lvlLabel = tk.Label(characterContainer, text="Level", bg=LIGHT, font=(FONT, 8, "bold"))
damageLabel = tk.Label(characterContainer, text="Damage", bg=LIGHT, font=(FONT, 8, "bold"))
characterLabel.grid(column=0, row=2, sticky=tk.W, padx=5, pady=5)
lvlLabel.grid(column=1, row=2, sticky=tk.W, padx=5, pady=5)
damageLabel.grid(column=2, row=2, sticky=tk.W, padx=5, pady=5)

# Add 4 predetermined characters to the list
characters = []
for i in range(4):
    characterRow = {}

    characterRow['character'] = tk.Label(characterContainer, text='Barbarian', font=(FONT, 8), bg=LIGHT)
    characterRow['character'].grid(
        column=0, row=3 + i, sticky=tk.W, padx=5, pady=5)

    characterRow['level'] = tk.Spinbox(characterContainer, from_=1, to=20)
    characterRow['level'].grid(
        column=1, row=3 + i, sticky=tk.W, padx=5, pady=5)

    characterRow['Damage'] = tk.Label(characterContainer, text='Fire', font=(FONT, 8), bg=LIGHT)
    characterRow['Damage'].grid(
        column=2, row=3 + i, sticky=tk.W, padx=5, pady=5)

    characters.append(characterRow)

# Create the damage container
damageContainer = tk.Frame(window, borderwidth=2, relief="groove", bg=LIGHT)
damageContainer.grid(column=0, row=3, sticky=tk.W, padx=5, pady=5)

# Drop down for dmg types
dmgType = ["Acid", "Bludegeoning", "Cold", "Fire", "Lightning", "Necrotic", "Piercing", "Poison", "Psychic", "Radiant", "Slashing", "Thunder"]
dmgVar = tk.StringVar(damageContainer)
dmgDropDown = tk.OptionMenu(damageContainer, dmgVar, *dmgType)
dmgDropDown.config(bg=TAN, font=(FONT, 8))
dmgDropDown.grid(column=0, row=0, padx=5, pady=5)

#button for adding dmg type
dmgTypeVal = []
dmgLabel = tk.Label(damageContainer, text=dmgTypeVal, font=(FONT, 8), bg=LIGHT)
dmgLabel.grid(column=0, row=1, padx=5, pady=5, columnspan=3)

# Button/button response for adding damage types
def dmgTypeAdd():
    tempDmg = dmgVar.get()
    if tempDmg not in dmgTypeVal:
        dmgTypeVal.append(dmgVar.get())
    dmgLabel.config(text=' '.join(str(x) for x in dmgTypeVal))
dmgAddButton = tk.Button(damageContainer, text='add dmg type', command = dmgTypeAdd, bg=TAN, font=(FONT, 8))
dmgAddButton.grid(column=1, row=0, padx=5, pady=5)


#button for removing dmg type, NOT IMPLMENTED, may implment if I have time Thursday
def dmgTypeRemove():
    print()
dmgRmvButton = tk.Button(damageContainer, text='Remove dmg type', command = dmgTypeRemove, bg=TAN, font=(FONT, 8))
dmgRmvButton.grid(column=2, row=0, padx=5, pady=5)

# Create monster description search field
monsterDescriptionContainer = tk.Frame(window, borderwidth=2, relief="groove", bg=LIGHT)
monsterDescriptionContainer.grid(column=0, row=4, sticky=tk.W, padx=5, pady=5)

monsterDescriptor = "Describe what type of monster you want"
monsterLabel = tk.Label(monsterDescriptionContainer, text = monsterDescriptor, bg=LIGHT, font=(FONT, 9, "bold"))
monsterLabel.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)

monsterWindow = tk.Text(monsterDescriptionContainer, height = 3, width = 35, font=(FONT, 8))
monsterWindow.grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)

# Add the monster button/button response
result = tk.StringVar()
result.set("")

def button_action(characterList):
    #Get appropriate CR
    challengeRating = 0
    for character in characterList:
        challengeRating += int(character['level'].get())
    challengeRating /= 4
    challengeRating = round(challengeRating,0)

    #Get list of monsters
    response = requests.get("https://www.dnd5eapi.co/api/monsters?challenge_rating=" + str(challengeRating))
    responseList = response.json().get('results');
    
    #Get top result
    if (len(responseList) > 0):
        response = requests.get("https://www.dnd5eapi.co" + responseList[0]['url'])

        #Print
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
    else:
        responseText = "Error, no monsters found";
    result.set(responseText)

button = tk.Button(window, text='Get Monster', command= lambda: button_action(characters), bg=TAN, font=(FONT, 9, "bold"))
button.grid(column=0, row=6)

# Print the result of the button
resultLabel = tk.Label(window, textvariable=result, background=TAN, font=(FONT, 8))
resultLabel.grid(column=0, row=7)

# Run the window
window.mainloop()

