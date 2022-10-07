import tkinter as tk
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from elasticsearch_dsl.query import MoreLikeThis
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
from PIL import Image, ImageTk
from urllib.request import urlopen
from io import BytesIO
from bs4 import BeautifulSoup

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

        self.geometry("350x750")
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
        monsterImage = Image.open('images/placeholderMonster.png')
        self.monsterImage = ImageTk.PhotoImage(monsterImage)

        self.button = tk.Button(self,
                                text='Get Monster',
                                command=lambda: self.handleGetMonsterButton(
                                    characterFrame.characters, difficultyFrame.diff, es, descriptFrame.monsterWindow),
                                highlightbackground=TAN,
                                font=(FONT, 9, "bold"),
                                fg=BLACK)
        self.button.grid(column=1, row=4, sticky=tk.W, **options)

        # Print the result of the button
        self.resultLabel = tk.Label(self, textvariable=self.result, bg=TAN, font=(FONT, 10),
                                    fg=BLACK)
        self.resultLabel.grid(column=1, row=5)
        self.resultImage = tk.Label(self, image=self.monsterImage, bg=TAN)
        self.resultImage.grid(column=1, row=6)

    

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
    def responseListAdapter(self, challengeRating, es, monsterWindow):
        # Get list of monsters
        query = Q('match', challenge_rating=challengeRating) & \
            Q(MoreLikeThis(like= monsterWindow.get("1.0", 'end-1c'), \
            fields=['actions_desc','special_abilities_desc','description', 'name'], min_term_freq = 1, min_doc_freq = 1))

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
        ##########responseText += "\nHP: " + str(response['hit_points'])
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
        #responseText += "\nweaknesses: " + str(response['damage_vulnerabilities'])
        #responseText += "\tresistances: " + str(response['damage_resistances'])
        #responseText += "\timmunities: " + str(response['damage_immunities'])
        return responseText
        return responseText

    def printImage(self, response):
        # Find page with the monster's image
        headers = {
        "referer":"referer: https://www.google.com/",
        "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"
        }
        s = requests.Session()
        searchTerm = "https://www.google.com/search?q=\"ForgottenRealms\" " + response['name']
        googleSearch = s.get(searchTerm, headers=headers)
        soup = BeautifulSoup(googleSearch.text, 'html.parser')
        webpage = soup.find("div", {"class": "yuRUbf"})
        webpage = webpage.find("a", href=True)['href']

        # Find the url for the monster's image
        forgottenRealms = s.get(webpage, headers=headers)
        soup = BeautifulSoup(forgottenRealms.text, 'html.parser')
        imgURL = soup.find("a", {"class": "image image-thumbnail"})['href']

        # Display the updated monster's image
        if imgURL != None:
            u = urlopen(imgURL)
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
    def handleGetMonsterButton(self, characterList, diff, es, monsterWindow):
        cr = self.getAppropriateCR(characterList, diff)
        responseList = self.responseListAdapter(cr, es, monsterWindow)
        # Get top result
        if (len(responseList) > 0):
            response = self.bestResponseAdapter(responseList)
            responseText = self.printAdapter(response)
            self.printImage(response)
        else:
            responseText = "Error, no monsters found"
        self.result.set(responseText)
