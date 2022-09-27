import tkinter as tk
from styles import *
import random
from frames.character_frame import CharacterFrame
from frames.terrain_frame import TerrainFrame
from frames.damage_type_frame import DamageTypeFrame
from frames.description_frame import DescriptionFrame
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
        terrain_frame = TerrainFrame(self)
        terrain_frame.grid(column=0, row=1, sticky=tk.W, **options)

        # Characters Frame
        character_frame = CharacterFrame(self)
        character_frame.grid(column=0, row=2, sticky=tk.W, **options)

        # Damage Type Frame
        dmg_type_frame = DamageTypeFrame(self)
        dmg_type_frame.grid(column=0, row=3, sticky=tk.W, **options)

        # Description Frame
        descript_frame = DescriptionFrame(self)
        descript_frame.grid(column=0, row=4, sticky=tk.W, **options)

        # Get Monster Button and Result
        self.result = tk.StringVar()
        self.result.set("")

        self.button = tk.Button(self,
                                text='Get Monster',
                                command=lambda: self.handleGetMonsterButton(
                                    character_frame.characters),
                                highlightbackground=TAN,
                                font=(FONT, 9, "bold"),
                                fg=BLACK)
        self.button.grid(column=0, row=6, sticky=tk.W, **options)

        # Print the result of the button
        self.result_label = tk.Label(self, textvariable=self.result, bg=TAN, font=(FONT, 10),
                                     fg=BLACK)
        self.result_label.grid(column=0, row=7)

    ############################
    # Button Functions
    ############################
    def getAppropriateCR(self, character_list):
        challengeRating = 0
        for character in character_list:
            challengeRating += int(character['level'].get())
        challengeRating /= 4
        return round(challengeRating, 0)

    # Gets a list of monsters from the challenge rating
    def responseListAdapter(self, challenge_rating):
        # Get list of monsters
        response = requests.get(
            "https://www.dnd5eapi.co/api/monsters?challenge_rating=" + str(challenge_rating))
        return response.json().get('results')

    # Picks a best monster from the available list
    def bestResponseAdapter(self, response_list):
        # Later we will want to change this function based on elastic search
        random.seed(random.randint(0, 100))
        rand_idx = random.randint(0, len(response_list) - 1)
        return requests.get("https://www.dnd5eapi.co" + response_list[rand_idx]['url'])

    # Prints the current best monster
    def printAdapter(self, response):
        # Create a string
        response_text = response.json().get('name')
        response_text += "\nHP: " + str(response.json().get('hit_points'))
        response_text += "\tAC: " + str(response.json().get('armor_class'))
        response_text += "\tCR: " + str(response.json().get('challenge_rating'))
        # New Line with Monster Stats
        response_text += "\nStr: " + str(response.json().get('strength'))
        response_text += "\tDex: " + str(response.json().get('dexterity'))
        response_text += "\tCon: " + str(response.json().get('constitution'))
        response_text += "\tInt: " + str(response.json().get('intelligence'))
        response_text += "\tWis: " + str(response.json().get('wisdom'))
        response_text += "\tCha: " + str(response.json().get('charisma'))
        return response_text

    # Button Code
    def handleGetMonsterButton(self, characterList):
        cr = self.getAppropriateCR(characterList)
        response_list = self.responseListAdapter(cr)
        # Get top result
        if len(response_list) > 0:
            response = self.bestResponseAdapter(response_list)
            response_text = self.printAdapter(response)
        else:
            response_text = "Error, no monsters found"
        self.result.set(response_text)
