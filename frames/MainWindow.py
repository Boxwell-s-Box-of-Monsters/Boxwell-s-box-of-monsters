import tkinter as tk
from Styles import *
import random
from frames.CharacterFrame import CharacterFrame
from frames.TerrainFrame import TerrainFrame
from frames.DamageTypeFrame import DamageTypeFrame
from frames.DescriptionFrame import DescriptionFrame
import requests

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
                              font=(FONT, 10, "bold"),
                              fg=BLACK)
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
                                command=lambda: self.handleGetMonsterButton(
                                    characterFrame.characters),
                                highlightbackground=TAN,
                                font=(FONT, 9, "bold"),
                                fg=BLACK)
        self.button.grid(column=0, row=6, sticky=tk.W, **options)

        # Print the result of the button
        self.resultLabel = tk.Label(self, textvariable=self.result, bg=TAN, font=(FONT, 10),
                                    fg=BLACK)
        self.resultLabel.grid(column=0, row=7)

    def handleGetMonsterButton(self, characterList):
        # Get appropriate CR
        challengeRating = 0
        for character in characterList:
            challengeRating += int(character['level'].get())
        challengeRating /= 4
        challengeRating = round(challengeRating, 0)

        # Get list of monsters
        response = requests.get(
            "https://www.dnd5eapi.co/api/monsters?challenge_rating=" + str(challengeRating))
        responseList = response.json().get('results')

        # Get top result
        if (len(responseList) > 0):
            random.seed(random.randint(0, 100))
            randIdx = random.randint(0, len(responseList) - 1)

            response = requests.get(
                "https://www.dnd5eapi.co" + responseList[randIdx]['url'])

            # Print
            responseText = response.json().get('name')
            responseText += "\nHP: " + str(response.json().get('hit_points'))
            responseText += "\tAC: " + str(response.json().get('armor_class'))
            responseText += "\tCR: " + \
                str(response.json().get('challenge_rating'))
            responseText += "\nStr: " + str(response.json().get('strength'))
            responseText += "\tDex: " + str(response.json().get('dexterity'))
            responseText += "\tCon: " + \
                str(response.json().get('constitution'))
            responseText += "\tInt: " + \
                str(response.json().get('intelligence'))
            responseText += "\tWis: " + str(response.json().get('wisdom'))
            responseText += "\tCha: " + str(response.json().get('charisma'))
        else:
            responseText = "Error, no monsters found"
        self.result.set(responseText)
