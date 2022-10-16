import tkinter as tk
import random
from io import BytesIO
from urllib.request import urlopen
from PIL import Image, ImageTk
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from elasticsearch_dsl.query import MoreLikeThis
from elasticsearch_dsl import Q
from Styles import *
from frames.CharacterFrame import CharacterFrame
from frames.DescriptionFrame import DescriptionFrame
from frames.DifficultyFrame import DifficultyFrame


############################
# Main Window
############################


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        ############################
        # Setup Elastic Search
        ############################
        self.es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
        # End Elastic Search

        self.minsize(500, 800) # min window size
        self.maxsize(False, 850) # max window size
        self.resizable(False, False) # cannot resize manually
        self.title("Monster Generator")
        self.configure(bg=TAN)
        
        # Make root grid responsive
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=3)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=1)
        self.grid_rowconfigure(5, weight=1)
        self.grid_rowconfigure(6, weight=1)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Top Label
        self.label = tk.Label(self,
                              text="Welcome to the monster library, please enter the relevant information below.",
                              wraplength=500,
                              anchor="center",
                              background=TAN,
                              font=(FONT, 20, "bold"),
                              fg=BLACK)
        self.label.grid(columnspan=2, row=0)

        # Terrain Frame  NOT CURRENTLY PLANNING TO IMPLEMENT
        # terrainFrame = TerrainFrame(self)
        # terrainFrame.grid(column=0, row=1, sticky=tk.W, **options)

        # Characters Frame
        characterFrame = CharacterFrame(self)
        characterFrame.grid(columnspan=2, row=1, ipadx=90, ipady=20, pady=(0, 5))

        # Damage Type Frame NOT IMPLMENTED THIS TIMEBOX, WILL BE ADDED TO CHARACTER INPUT
        # dmgTypeFrame = DamageTypeFrame(self)
        # dmgTypeFrame.grid(column=0, row=3, sticky=tk.W, **options)

        # Description Frame
        descriptFrame = DescriptionFrame(self)
        descriptFrame.grid(columnspan=2, row=2, ipadx=30, ipady=30, pady=(0, 5))

        # Difficulty Frame
        difficultyFrame = DifficultyFrame(self)
        difficultyFrame.grid(columnspan=2, row=3, pady=(0, 5))

        # Get Monster Button and Result
        self.result = tk.StringVar()
        self.result.set("")
        monsterImage = Image.open('images/placeholderMonster.png')
        self.monsterImage = ImageTk.PhotoImage(monsterImage)

        self.button = tk.Button(self,
                                text='Get Monster',
                                command=lambda: self.handleGetMonsterButton(
                                    characterFrame.characters, difficultyFrame.diff, descriptFrame.monsterWindow),
                                highlightbackground=TAN,
                                font=(FONT, 9, "bold"),
                                fg=BLACK)
        self.button.grid(columnspan=2, row=4)

        # Print the result of the button
        self.resultLabel = tk.Label(self, textvariable=self.result, bg=TAN, font=(FONT, 14),
                                    fg=BLACK)
        self.resultLabel.grid(columnspan=2, row=5)
        self.resultImage = tk.Label(self, image=self.monsterImage, bg=TAN)
        self.resultImage.grid(columnspan=2, row=6)

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
    def responseListAdapter(self, challengeRating, monsterWindow):
        # Get list of monsters
        query = Q('match', challenge_rating=challengeRating) & \
                Q(MoreLikeThis(like=monsterWindow.get("1.0", 'end-1c'),
                               fields=['actions_desc', 'special_abilities_desc', 'description', 'name'],
                               min_term_freq=1, min_doc_freq=1))

        s = Search(using=self.es, index='monster_index').query(query)
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
        responseText += "\nHP: " + str(response['hit_points'])
        responseText += "\nAC: " + str(response['armor_class'])
        responseText += "\tCR: " + str(response['challenge_rating'])
        # New Line with Monster Stats
        responseText += "\nStr: " + str(response['strength'])
        responseText += "\tDex: " + str(response['dexterity'])
        responseText += "\tCon: " + str(response['constitution'])
        responseText += "\tInt: " + str(response['intelligence'])
        responseText += "\tWis: " + str(response['wisdom'])
        responseText += "\tCha: " + str(response['charisma'])
        # New line with Monster weaknesses and resistances
        if "damage_vulnerabilities" in response:
            responseText += "\nweaknesses: " + str(response['damage_vulnerabilities'])
        if "damage_resistances" in response:
            responseText += "\tresistances: " + str(response['damage_resistances'])
        if "damage_immunities" in response:
            responseText += "\timmunities: " + str(response['damage_immunities'])
        return responseText

    def printImage(self, response):
        # Display the updated monster's image
        if response['imageURL'] is not None:
            with urlopen(response['imageURL']) as imageURL:
                u = imageURL
                im = Image.open(BytesIO(u.read())).resize((200,200))
                newImage = ImageTk.PhotoImage(im)
                self.resultImage.configure(image=newImage)
                self.resultImage.image = newImage
        else:
            im = Image.open('images/placeholderMonster.png')
            newImage = ImageTk.PhotoImage(im)
            self.resultImage.configure(image=newImage)
            self.resultImage.image = newImage


    # Button Code
    def handleGetMonsterButton(self, characterList, diff, monsterWindow):
        cr = self.getAppropriateCR(characterList, diff)
        responseList = self.responseListAdapter(cr, monsterWindow)
        # Get top result
        if len(responseList) > 0:
            response = self.bestResponseAdapter(responseList)
            responseText = self.printAdapter(response)
            self.printImage(response)
        else:
            responseText = "Error, no monsters found"
        self.result.set(responseText)
