# Mock up of the monster generator
import requests
import tkinter as tk

# Colors
TAN = "#DDC3A2"
LIGHT = "#FFE4C4"
FONT = "arial"

############################
# Terrain Frame
############################

class TerrainFrame(tk.Frame):
    def __init__(self, container):
        super().__init__(container)
        
        options = {'padx': 5, 'pady': 5}

        self.configure(borderwidth=2, relief="groove", bg=LIGHT)
    
        # Terrain Label
        self.terrainLabel = tk.Label(self, 
                                     text = "Terrain Description: ", 
                                     background=LIGHT, 
                                     font=(FONT, 8, "bold"))
        
        self.terrainLabel.grid(column=0, row=0, sticky=tk.W, **options)

        # Terrain Input
        self.terrainInput = tk.Text(self, height = 1, width = 20, font=(FONT, 8))
        self.terrainInput.grid(column=1, row=0, sticky=tk.W, **options)


############################
# Character Frame
############################

class CharacterFrame(tk.Frame):
    def __init__(self, container):
        super().__init__(container)
        
        options = {'padx': 5, 'pady': 5}

        self.configure(borderwidth=2, relief="groove", bg=LIGHT)
        
        # Character Container Label
        self.characterContainerLabel = tk.Label(self, 
                                           text = "Adventuring Party", 
                                           font=(FONT, 9, "bold"), 
                                           background=LIGHT)
        self.characterContainerLabel.grid(column=0, row=0, columnspan=3, **options)
        
        # Add/Remove Buttons
        self.addCharacter = tk.Button(self, text='Add Character', bg=TAN, font=(FONT, 8))
        self.removeCharacter = tk.Button(self, text="Remove Character", bg=TAN, font=(FONT, 8))
        self.addCharacter.grid(column=0, row=1, sticky=tk.W, **options)
        self.removeCharacter.grid(column=1, row=1, sticky=tk.W, **options)
        
        # Labels for Character table
        self.characterLabel = tk.Label(self, text="Character", bg=LIGHT, font=(FONT, 8, "bold"))
        self.lvlLabel = tk.Label(self, text="Level", bg=LIGHT, font=(FONT, 8, "bold"))
        self.damageLabel = tk.Label(self, text="Damage", bg=LIGHT, font=(FONT, 8, "bold"))
        self.characterLabel.grid(column=0, row=2, sticky=tk.W, **options)
        self.lvlLabel.grid(column=1, row=2, sticky=tk.W, **options)
        self.damageLabel.grid(column=2, row=2, sticky=tk.W, **options)
        
        # Characters
        self.characters = []
        for i in range(4):
            characterRow = {}

            characterRow['character'] = tk.Label(self, text='Barbarian', font=(FONT, 8), bg=LIGHT)
            characterRow['character'].grid(
                column=0, row=3 + i, sticky=tk.W, **options)

            characterRow['level'] = tk.Spinbox(self, from_=1, to=20, font=(FONT, 8))
            characterRow['level'].grid(
                column=1, row=3 + i, sticky=tk.W, **options)

            characterRow['Damage'] = tk.Label(self, text='Fire', font=(FONT, 8), bg=LIGHT)
            characterRow['Damage'].grid(
                column=2, row=3 + i, sticky=tk.W, **options)

            self.characters.append(characterRow)
        
############################
# Damage Type Frame
############################
class DamageTypeFrame(tk.Frame):
    def __init__(self, container):
        super().__init__(container)
        
        options = {'padx': 5, 'pady': 5}

        self.configure(borderwidth=2, relief="groove", bg=LIGHT)
        
        # Drop Down for Dmg Types
        self.dmgTypes = ["Acid", "Bludegeoning", "Cold", "Fire", "Lightning", "Necrotic", "Piercing", "Poison", "Psychic", "Radiant", "Slashing", "Thunder"]
        self.dmgVar = tk.StringVar(self)
        self.dmgDropDown = tk.OptionMenu(self, self.dmgVar, *self.dmgTypes)
        self.dmgDropDown.config(bg=TAN, font=(FONT, 8))
        self.dmgDropDown.grid(column=0, row=0, **options)
        
        # Listed dmg types
        self.dmgTypeVal = []
        self.dmgLabel = tk.Label(self, text=self.dmgTypeVal, font=(FONT, 8), bg=LIGHT)
        self.dmgLabel.grid(column=0, row=1, columnspan=3, **options)
        
        # Buttons
        self.dmgAddButton = tk.Button(self, 
                                      text='add dmg type', 
                                      command = self.addDmgType, 
                                      bg=TAN, 
                                      font=(FONT, 8))
        self.dmgAddButton.grid(column=1, row=0, **options)


        self.dmgRmvButton = tk.Button(self, 
                                      text='Remove dmg type', 
                                      command = self.removeDmgType, 
                                      bg=TAN, 
                                      font=(FONT, 8))
        self.dmgRmvButton.grid(column=2, row=0, **options)
         
    def addDmgType(self):
        if self.dmgVar.get() not in self.dmgTypeVal:
            self.dmgTypeVal.append(self.dmgVar.get())
        self.dmgLabel.config(text=' '.join(str(x) for x in self.dmgTypeVal))
        
    def removeDmgType():
        pass

############################
# Description Frame
############################
class DescriptionFrame(tk.Frame):
    def __init__(self, container):
        super().__init__(container)
        
        options = {'padx': 5, 'pady': 5}

        self.configure(borderwidth=2, relief="groove", bg=LIGHT)
        
        # label
        self.monsterLabel = tk.Label(self, 
                                text = "Describe what type of monster you want", 
                                bg=LIGHT, 
                                font=(FONT, 9, "bold"))
        self.monsterLabel.grid(column=0, row=0, sticky=tk.W, **options)
        
        # text input box
        self.monsterWindow = tk.Text(self, height = 3, width = 35, font=(FONT, 8))
        self.monsterWindow.grid(column=0, row=1, sticky=tk.W, **options)



############################
# Main Window
############################
class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.geometry("325x610")
        self.title("Monster Generator")
        self.configure(bg=TAN)
        
        options = {'padx': 5, 'pady': 5}

        # Top Label
        self.label = tk.Label(self, 
                              text="Welcome to the monster library, please enter the relevant information below.", 
                              wraplength=300, 
                              justify="center", 
                              background=TAN, 
                              font=(FONT, 10, "bold"))
        self.label.grid(column=0, row=0, **options)

        # Terrain Frame
        terrainFrame = TerrainFrame(self)
        terrainFrame.grid(column=0, row=1, sticky=tk.W, **options)

        # Characters Frame
        characterFrame = CharacterFrame(self)
        characterFrame.grid(column=0, row=2, sticky=tk.W, **options)

        # Damage Type Frame
        dmgTypeFrame = DamageTypeFrame(self)
        dmgTypeFrame.grid(column=0, row=3, sticky=tk.W, **options)

        
        # Description Frame
        descriptFrame = DescriptionFrame(self)
        descriptFrame.grid(column=0, row=4, sticky=tk.W, **options)

        # Get Monster Button and Result
        self.result = tk.StringVar()
        self.result.set("")
        
        self.button = tk.Button(self, 
                                text='Get Monster', 
                                command= lambda: self.handleGetMonsterButton(characterFrame.characters), 
                                bg=TAN, 
                                font=(FONT, 9, "bold"))
        self.button.grid(column=0, row=6)

        # Print the result of the button
        self.resultLabel = tk.Label(self, textvariable=self.result, background=TAN, font=(FONT, 8))
        self.resultLabel.grid(column=0, row=7)

    def handleGetMonsterButton(self, characterList):
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
        self.result.set(responseText)


if __name__ == "__main__":
    window = MainWindow()
    window.mainloop()
    



