import tkinter as tk
from Styles import *
import random
from frames.CharacterFrame import CharacterFrame
from frames.TerrainFrame import TerrainFrame
from frames.DamageTypeFrame import DamageTypeFrame
from frames.DescriptionFrame import DescriptionFrame
from frames.DifficultyFrame import DifficultyFrame
import requests

############################
# Main Window
############################


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.geometry("330x580")
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
        self.label.grid(column=1, row=0, sticky=tk.W, **options)

        # Terrain Frame  NOT CURRENTLY PLANNING TO IMPLEMENT
        #terrainFrame = TerrainFrame(self)
        #terrainFrame.grid(column=0, row=1, sticky=tk.W, **options)

        # Characters Frame
        characterFrame = CharacterFrame(self)
        characterFrame.grid(column=1, row=1, sticky=tk.W,  **options)

        # Damage Type Frame NOT IMPLMENTED THIS TIMEBOX, WILL BE ADDED TO CHARACTER INPUT
        #dmgTypeFrame = DamageTypeFrame(self)
        #dmgTypeFrame.grid(column=0, row=3, sticky=tk.W, **options)

        # Description Frame
        descriptFrame = DescriptionFrame(self)
        descriptFrame.grid(column=1, row=2, sticky=tk.W, **options)

        # Difficulty Frame
        difficultyFrame = DifficultyFrame(self)
        difficultyFrame.grid(column=1, row=3, sticky=tk.W, **options)

        # Get Monster Button and Result
        self.result = tk.StringVar()
        self.result.set("")

        self.button = tk.Button(self,
                                text='Get Monster',
                                command=lambda: self.handleGetMonsterButton(
                                    characterFrame.characters, difficultyFrame.diff),
                                highlightbackground=TAN,
                                font=(FONT, 9, "bold"),
                                fg=BLACK)
        self.button.grid(column=1, row=4, sticky=tk.W, **options)

        # Print the result of the button
        self.resultLabel = tk.Label(self, textvariable=self.result, bg=TAN, font=(FONT, 10),
                                    fg=BLACK)
        self.resultLabel.grid(column=1, row=5)

    ############################
    # Button Functions
    ############################
    def getAppropriateCR(self, characterList, diff):
        challengeRating = 0
        for character in characterList:
            challengeRating += int(character['level'].get())
        challengeRating /= 4
        challengeRating += diff.get()

        return round(challengeRating, 0)

    # Gets a list of monsters from the challenge rating
    def responseListAdapter(self, challengeRating):
        # Get list of monsters
        response = requests.get(
            "https://www.dnd5eapi.co/api/monsters?challenge_rating=" + str(challengeRating))
        return response.json().get('results')

    # Picks a best monster from the available list
    def bestResponseAdapter(self, responseList):
        # Later we will want to change this function based on elastic search
        random.seed(random.randint(0, 100))
        randIdx = random.randint(0, len(responseList) - 1)
        return requests.get("https://www.dnd5eapi.co" + responseList[randIdx]['url'])

    # Prints the current best monster
    def printAdapter(self, response):
        # Create a string
        responseText = response.json().get('name')
        responseText += "\nHP: " + str(response.json().get('hit_points'))
        responseText += "\tAC: " + str(response.json().get('armor_class'))
        responseText += "\tCR: " + str(response.json().get('challenge_rating'))
        # New Line with Monster Stats
        responseText += "\nStr: " + str(response.json().get('strength'))
        responseText += "\tDex: " + str(response.json().get('dexterity'))
        responseText += "\tCon: " + str(response.json().get('constitution'))
        responseText += "\tInt: " + str(response.json().get('intelligence'))
        responseText += "\tWis: " + str(response.json().get('wisdom'))
        responseText += "\tCha: " + str(response.json().get('charisma'))
        # New line with Monster weaknesses and resistances
        responseText += "\nweaknesses: " + str(response.json().get('damage_vulnerabilities'))
        responseText += "\tresistances: " + str(response.json().get('damage_resistances'))
        responseText += "\timmunities: " + str(response.json().get('damage_immunities'))
        return responseText

    # Button Code
    def handleGetMonsterButton(self, characterList, diff):
        cr = self.getAppropriateCR(characterList, diff)
        responseList = self.responseListAdapter(cr)
        # Get top result
        if (len(responseList) > 0):
            response = self.bestResponseAdapter(responseList)
            responseText = self.printAdapter(response)
        else:
            responseText = "Error, no monsters found"
        self.result.set(responseText)
