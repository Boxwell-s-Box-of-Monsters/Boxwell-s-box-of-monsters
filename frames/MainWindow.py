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
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=1)
        self.grid_rowconfigure(5, weight=1)

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
        characterFrame.grid(column=0, row=1, ipadx=50, ipady=10, padx=5, sticky=tk.N)

        # Damage Type Frame NOT IMPLMENTED THIS TIMEBOX, WILL BE ADDED TO CHARACTER INPUT
        # dmgTypeFrame = DamageTypeFrame(self)
        # dmgTypeFrame.grid(column=0, row=3, sticky=tk.W, **options)

        # Description Frame
        descriptFrame = DescriptionFrame(self)
        descriptFrame.grid(column=1, row=1, ipadx=10, ipady=10, padx=(0, 5), sticky=tk.NS)

        # Difficulty Frame
        difficultyFrame = DifficultyFrame(self)
        difficultyFrame.grid(column=0, columnspan=2, row=2, sticky=tk.NS, pady=5)

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
                                font=(FONT, 12, "bold"),
                                fg=BLACK)
        self.button.grid(columnspan=2, column=0, row=3, ipadx=5, ipady=5, sticky=tk.NS)

        # Print the result of the button
        self.resultLabel = tk.Label(self, textvariable=self.result, bg=TAN, font=(FONT, 14),
                                    fg=BLACK)
        self.resultLabel.grid(columnspan=2, row=4, sticky=tk.NS)
        self.resultImage = tk.Label(self, image=self.monsterImage, bg=TAN)
        self.resultImage.grid(columnspan=2, column=0, row=5, sticky=tk.NS)

    ############################
    # Button Functions
    ############################
    def getAppropriateCR(self, characterList, diff):
        level = 0
        for character in characterList:
            level += int(character['level'].get())
        level /= len(characterList)
        level = int(round(level, 0))

        #Probably want to move this later
        xpTable = [[25, 50, 75, 100],
                    [50, 100, 150, 200],
                    [75, 150, 225, 400],
                    [125, 250, 375, 500],
                    [250, 500, 750, 1100],
                    [300, 600, 900, 1400],
                    [350, 750, 1100, 1700],
                    [450, 900, 1400, 2100],
                    [550, 1100, 1600, 2400],
                    [600, 1200, 1900, 2800],
                    [800, 1600, 2400, 3600],
                    [1000, 2000, 3000, 4500],
                    [1100, 2200, 3400, 5100],
                    [1250, 2500, 3800, 5700],
                    [1400, 2800, 4300, 6400],
                    [1600, 3200, 4800, 7200],
                    [2000, 3900, 5900, 8800],
                    [2100, 4200, 6300, 9500],
                    [2400, 4900, 7300, 10900],
                    [2800, 5700, 8500, 12700]]

        return xpTable[level-1][diff.get()]

    # Gets a list of monsters from the challenge rating
    def responseListAdapter(self, targetXP, monsterWindow):
        # Get list of monsters
        query = Q(MoreLikeThis(like=monsterWindow.get("1.0", 'end-1c'),
                               fields=['actions_desc', 'special_abilities_desc', 'description', 'name'],
                               min_term_freq=1, min_doc_freq=1))

        s = Search(using=self.es, index='monster_index').filter('range', xp={'lte': targetXP}).query(query)
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

    def displayBlank(self):
        im = Image.open('images/placeholderMonster.png')
        newImage = ImageTk.PhotoImage(im)
        self.resultImage.configure(image=newImage)
        self.resultImage.image = newImage

    def printImage(self, response):
        # Display the updated monster's image
        if response['imageURL'] is not None:
            print(response['imageURL'])
            with urlopen(response['imageURL']) as imageURL:
                u = imageURL
                im = Image.open(BytesIO(u.read())).resize((200,200))
                newImage = ImageTk.PhotoImage(im)
                self.resultImage.configure(image=newImage)
                self.resultImage.image = newImage
        else:
            self.displayBlank()

    # Button Code
    def handleGetMonsterButton(self, characterList, diff, monsterWindow):
        xp = self.getAppropriateCR(characterList, diff)
        responseList = self.responseListAdapter(xp, monsterWindow)
        # Get top result
        if len(responseList) > 0:
            response = self.bestResponseAdapter(responseList)
            responseText = self.printAdapter(response)
            self.printImage(response)
        else:
            responseText = "Error, no monsters found"
            self.displayBlank()
        self.result.set(responseText)
        
    
        