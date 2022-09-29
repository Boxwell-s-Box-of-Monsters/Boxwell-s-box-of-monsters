import tkinter as tk
from Styles import *
import random
from frames.CharacterFrame import CharacterFrame
from frames.TerrainFrame import TerrainFrame
from frames.DamageTypeFrame import DamageTypeFrame
from frames.DescriptionFrame import DescriptionFrame
from frames.DifficultyFrame import DifficultyFrame
import requests
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

<<<<<<< Updated upstream
        self.geometry("350x680")
=======
        self.geometry("350x850")
>>>>>>> Stashed changes
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
        monsterImage = Image.open('images/placeholderMonster.png')
        self.monsterImage = ImageTk.PhotoImage(monsterImage)

        self.button = tk.Button(self,
                                text='Get Monster',
                                command=lambda: self.handleGetMonsterButton(
                                    characterFrame.characters, difficultyFrame.diff),
                                highlightbackground=TAN,
                                font=(FONT, 9, "bold"),
                                fg=BLACK)
        self.button.grid(column=0, row=6, sticky=tk.W, **options)

        # Print the result of the button
        self.resultLabel = tk.Label(self, textvariable=self.result, bg=TAN, font=(FONT, 10),
                                    fg=BLACK)
        self.resultLabel.grid(column=0, row=7)
        self.resultImage = tk.Label(self, image=self.monsterImage, bg=TAN)
        self.resultImage.grid(column=0, row=8)

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
        return responseText

    # Prints the current best monster's image
    def printImage(self, response):
        # Find page with the monster's image
        headers = {
        "referer":"referer: https://www.google.com/",
        "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"
        }
        s = requests.Session()
        searchTerm = "https://www.google.com/search?q=\"ForgottenRealms\" " + response.json().get('name')
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
    def handleGetMonsterButton(self, characterList, diff):
        cr = self.getAppropriateCR(characterList, diff)
        responseList = self.responseListAdapter(cr)
        # Get top result
        if (len(responseList) > 0):
            response = self.bestResponseAdapter(responseList)
            responseText = self.printAdapter(response)
            self.printImage(response)
        else:
            responseText = "Error, no monsters found"
        self.result.set(responseText)
