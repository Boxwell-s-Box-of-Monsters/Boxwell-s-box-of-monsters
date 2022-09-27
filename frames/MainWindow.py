import tkinter as tk
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from elasticsearch_dsl import Q
from Styles import *
import random
from frames.CharacterFrame import CharacterFrame
from frames.TerrainFrame import TerrainFrame
from frames.DamageTypeFrame import DamageTypeFrame
from frames.DescriptionFrame import DescriptionFrame
from frames.DifficultyFrame import DifficultyFrame
import requests
import json

############################
# Main Window
############################


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        ############################
        # Setup Elastic Search
        ############################
        es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
        monsterFile = open('./json/data.json')
        monsters = json.load(monsterFile)
        print(monsters)
        for monster in monsters:
            es.index(index='monster_index', body = monster)

        # End Elastic Search

        self.geometry("350x680")
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

        # Difficulty Frame
        difficultyFrame = DifficultyFrame(self)
        difficultyFrame.grid(column=0, row=5, sticky=tk.W, **options)

        # Get Monster Button and Result
        self.result = tk.StringVar()
        self.result.set("")

        self.button = tk.Button(self,
                                text='Get Monster',
                                command=lambda: self.handleGetMonsterButton(
                                    characterFrame.characters, difficultyFrame.diff, es),
                                highlightbackground=TAN,
                                font=(FONT, 9, "bold"),
                                fg=BLACK)
        self.button.grid(column=0, row=6, sticky=tk.W, **options)

        # Print the result of the button
        self.resultLabel = tk.Label(self, textvariable=self.result, bg=TAN, font=(FONT, 10),
                                    fg=BLACK)
        self.resultLabel.grid(column=0, row=7)

    

    #########################
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
    def responseListAdapter(self, challengeRating, es):
        # Get list of monsters
        query = Q('match', challenge_rating=challengeRating)
        s = Search(using=es, index='monster_index').query(query)
        response = s.execute()
        return response

    # Picks a best monster from the available list
    def bestResponseAdapter(self, responseList):
        # Later we will want to change this function based on elastic search
        random.seed(random.randint(0, 100))
        randIdx = random.randint(0, len(responseList) - 1)
        return responseList.hits[randIdx]

    # Prints the current best monster
    def printAdapter(self, response):
        # Create a string
        responseText = response['name']
        #responseText += "\nHP: " + str(response['hit_points'])
        responseText += "\nAC: " + str(response['armor_class'])
        responseText += "\tCR: " + str(response['challenge_rating'])
        # New Line with Monster Stats
        responseText += "\nStr: " + str(response['strength'])
        responseText += "\tDex: " + str(response['dexterity'])
        responseText += "\tCon: " + str(response['constitution'])
        responseText += "\tInt: " + str(response['intelligence'])
        responseText += "\tWis: " + str(response['wisdom'])
        responseText += "\tCha: " + str(response['charisma'])
        return responseText

    # Button Code
    def handleGetMonsterButton(self, characterList, diff, es):
        cr = self.getAppropriateCR(characterList, diff)
        responseList = self.responseListAdapter(cr, es)
        # Get top result
        if (len(responseList) > 0):
            response = self.bestResponseAdapter(responseList)
            responseText = self.printAdapter(response)
        else:
            responseText = "Error, no monsters found"
        self.result.set(responseText)
