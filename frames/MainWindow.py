import tkinter as tk
import random
from os.path import exists
from PIL import Image, ImageTk
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from elasticsearch_dsl.query import MoreLikeThis
from elasticsearch_dsl import Q
from Styles import *
from frames.CharacterFrame import CharacterFrame
from frames.DescriptionFrame import DescriptionFrame
from frames.DifficultyFrame import DifficultyFrame
from frames.ResultFrame import ResultFrame


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

        # self.minsize(1000, 800) # min window size
        # self.maxsize(False, 900) # max window size
        #self.resizable(False, False) # cannot resize manually
        self.state('zoomed')
        self.title("Monster Generator")
        self.configure(bg=TAN)

        # Make root grid responsive
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=1)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        padding = {"pady": (0, 5), "padx": (2, 2)}
        innerPadding = {"ipadx": 3, "ipady":3}

        # Top Label
        label = tk.Label(self,
                              text="Welcome to the monster library, please enter the relevant information below.",
                              wraplength=500,
                              anchor="center",
                              background=TAN,
                              font=(FONT, 14, "bold"),
                              fg=BLACK)
        label.grid(columnspan=2, row=0, column=0, sticky=tk.NS, **padding)

        # Terrain Frame  NOT CURRENTLY PLANNING TO IMPLEMENT
        # terrainFrame = TerrainFrame(self)
        # terrainFrame.grid(column=0, row=1, sticky=tk.W, **options)

        # Characters Frame
        characterFrame = CharacterFrame(self)
        characterFrame.grid(column=0, row=1, sticky=tk.NS, **padding)

        # Damage Type Frame NOT IMPLMENTED THIS TIMEBOX, WILL BE ADDED TO CHARACTER INPUT
        # dmgTypeFrame = DamageTypeFrame(self)
        # dmgTypeFrame.grid(column=0, row=3, sticky=tk.W, **options)

        # Description Frame
        descriptFrame = DescriptionFrame(self)
        descriptFrame.grid(column=0, row=2, sticky=tk.NS, **innerPadding, **padding)

        # Difficulty Frame
        difficultyFrame = DifficultyFrame(self)
        difficultyFrame.grid(column=0, row=3, sticky=tk.NS, **padding)

        # Get Monster Button and Result
        self.result = tk.StringVar()
        self.result.set("")
        self.resultDesc = tk.StringVar()
        self.resultDesc.set("")
        self.resultList = tk.StringVar()
        self.resultList.set("")
        monsterImage = Image.open('images/placeholderMonster.png')
        self.monsterImage = ImageTk.PhotoImage(monsterImage)

        button = tk.Button(self,
                                text='Get Monster',
                                command=lambda: self.handleGetMonsterButton(
                                    characterFrame.characters, difficultyFrame.diff, descriptFrame.monsterWindow),
                                font=(FONT, 10, "bold"),
                                highlightbackground=TAN,
                                fg=BLACK)
        button.grid(column=0, row=4, sticky=tk.N, ipadx=10, ipady=10)

        # Print the result of the button
        resultFrame = ResultFrame(self)
        resultLabel = tk.Label(resultFrame, textvariable=self.result, bg=TAN, font=(FONT, 14),
                                    fg=BLACK)
        resultLabelDesc = tk.Label(resultFrame, textvariable=self.resultDesc,
                                   wraplength=1000, justify="left", bg=TAN, font=(FONT, 14),
                                    fg=BLACK)
        resultListLabel = tk.Label(resultFrame, textvariable=self.resultList, bg=TAN, font=(FONT, 14),
                                    fg=BLACK)
        self.resultImage = tk.Label(resultFrame, image=self.monsterImage, bg=TAN)
        resultFrame.setPositions(resultLabel, resultLabelDesc, self.resultImage, resultListLabel)
        resultFrame.grid(column=1, row=1, sticky=tk.N)

    ############################
    # Button Functions
    ############################
    def getAppropriateCR(self, characterList, diff):
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

        minXp = 0
        maxXp = 0
        for character in characterList:
            level = int(character['level'].get())
            if diff.get() == 0:
                minXp += xpTable[level-1][diff.get()-1]
                maxXp += xpTable[level-1][diff.get()]
            else:
                minXp += xpTable[level-1][diff.get()]/2
                maxXp += xpTable[level-1][diff.get()]
        minXp /= 25


        return minXp, maxXp

    # Gets a list of monsters from the challenge rating
    def responseListAdapter(self, minXP, maxXP, monsterWindow):
        # Get list of monsters
        if isinstance(monsterWindow, str) is False:
            monsterWindow = monsterWindow.get("1.0", 'end-1c')

        query = Q(MoreLikeThis(like=monsterWindow,
                               fields=['actions_desc', 'special_abilities_desc', 'description', 'name'],
                               min_term_freq=1, min_doc_freq=1))

        lowerBound = 0.9
        s = Search(using=self.es, index='monster_index') \
            .filter('range', xp={'gte': lowerBound*maxXP, 'lte': maxXP}).query(query)
        response = s.execute()
        lowerBound -= .1

        while len(response) <= 3 and lowerBound > 0 and lowerBound*maxXP > minXP:
            s = Search(using=self.es, index='monster_index') \
                .filter('range', xp={'gte': lowerBound*maxXP, 'lte': maxXP}).query(query)
            response = s.execute()
            lowerBound -= .1

        return response

    # Picks the index of a monster out of the list weighted based on score
    def randomMonsterPicker(self, responseList):
        totalScore = 0
        for i in range(len(responseList)):
            totalScore += responseList[0].meta.score
        rand = random.random() * totalScore
        i = -1
        while rand > 0:
            i += 1
            rand -= responseList[0].meta.score
        return i

    # Picks the best monsters for the encounter
    def encounterGenerator(self, minEncounterXP, maxEncounterXP, potentialMonsters, characterList):
        index = self.randomMonsterPicker(potentialMonsters)
        currentEncounterXP = 0
        encounter = []
        monsterQuantity = 0

        # From the users description, add the paragon monster
        monsterQuantity += self.monstersMultiplied(potentialMonsters[index],
                                                   currentEncounterXP, maxEncounterXP, monsterQuantity, characterList)
        encounter.append([potentialMonsters[index], monsterQuantity])
        currentEncounterXP += int(potentialMonsters[index]['xp']) * monsterQuantity

        # Make a new list of monsters based on best matches to the paragon monster
        matchingMonsters = self.responseListAdapter(minEncounterXP, (potentialMonsters[index]['xp'])-1, \
                                                potentialMonsters[index]['description'])

        # Adds the best monsters based on the paragon monster to the
        # encounter until the list is empty or the encounter has reached 10
        while len(matchingMonsters) > 0 and monsterQuantity < 10:
            # if the number of monsters that can be added is not 0, add it.
            newMonsters = self.monstersMultiplied(matchingMonsters[0],
                                                  currentEncounterXP, maxEncounterXP, monsterQuantity, characterList)
            if newMonsters > 0:
                encounter.append([matchingMonsters[0], newMonsters])
                currentEncounterXP += int(matchingMonsters[0]['xp']) * newMonsters
                monsterQuantity += newMonsters

            if len(matchingMonsters) > 1:
                matchingMonsters = matchingMonsters[1:]
            else:
                matchingMonsters = []
        return encounter

    # returns an integer for the number of monsters that can be added to the encounter for a specific monster
    def monstersMultiplied(self, monster, currentEncounterXP, maxEncounterXP, monsterQuantity, characterList):
        # update xpMult according to how many monsters are already in the encounter
        addedMonsters = 0
        xpMult = 1
        if monsterQuantity+1 >= 7:
            xpMult = 2.5
        elif monsterQuantity+1 >= 3:
            xpMult = 2
        elif monsterQuantity+1 == 2:
            xpMult = 1.5

        typeMult = 0
        for character in characterList:
            cDmg = character['damageVar'].get()
            #cDmg = 'fire'
            print(cDmg) # for testing purposes
            typeMult = 0
            if cDmg in monster['damage_vulnerabilities']:
                print("VULNERABLE-----------------------------------------------------")
                typeMult += 0.5
            elif cDmg in monster['damage_resistances']:
                print("RESISTANT-----------------------------------------------------")
                typeMult += 2
            elif cDmg in monster['damage_immunities']:
                print("IMMUNE-----------------------------------------------------")
                typeMult += 4
            else:
                typeMult += 1
        typeMult /= len(characterList)
        print(str(monster['name']) + " " + str(typeMult)) # for testing purposes

        # adds the same monster multiple times, taking into account the xp multiplier and the preexisting encounter xp
        acceptableXP = (maxEncounterXP - (currentEncounterXP+int(monster['xp']))*xpMult >= 0) # typeMult multiplier will be added once working
        while acceptableXP and (monsterQuantity+addedMonsters < 10):
            addedMonsters += 1
            currentEncounterXP += int(monster['xp'])
            if monsterQuantity+addedMonsters+1 >= 7:
                xpMult = 2.5
            elif monsterQuantity+addedMonsters+1 >= 3:
                xpMult = 2
            elif monsterQuantity+addedMonsters+1 == 2:
                xpMult = 1.5
            acceptableXP = (maxEncounterXP - (currentEncounterXP+int(monster['xp']))*xpMult >= 0)
        return addedMonsters

    # Prints the current best monster
    def printAdapter(self, response):
        # Create a string
        responseText = response['name']
        responseText += "\nHP: " + str(response['hit_points'])
        responseText += "\tAC: " + str(response['armor_class'])
        responseText += "\tCR: " + str(response['challenge_rating'])
        responseText += "\tXP: " + str(response['xp'])
        # New Line with Monster Stats
        responseText += "\nStr: " + str(response['strength'])
        responseText += "\tDex: " + str(response['dexterity'])
        responseText += "\tCon: " + str(response['constitution'])
        responseText += "\tInt: " + str(response['intelligence'])
        responseText += "\tWis: " + str(response['wisdom'])
        responseText += "\tCha: " + str(response['charisma'])
        # New line with Monster weaknesses and resistances
        if len(response['damage_vulnerabilities'])>0:
            responseText += "\nweaknesses: "
            for r in response['damage_vulnerabilities']:
                responseText += str(r) + ' '
        if len(response['damage_resistances'])>0:
            responseText += "\nresistances: "
            for r in response['damage_resistances']:
                responseText += str(r) + ' '
        if len(response['damage_immunities'])>0:
            responseText += "\nimmunities: "
            for r in response['damage_immunities']:
                responseText += str(r) + ' '
        self.resultDesc.set("\t" + str(response['caption']))
        return responseText

    def printList(self, encounter):
        responseList = "Encounter\n\n"

        for e in encounter:
            responseList += str(e[1]) + "x " + str(e[0]['name']) + "\n"

        return responseList

    def displayBlank(self):
        im = Image.open('images/placeholderMonster.png')
        newImage = ImageTk.PhotoImage(im)
        self.resultImage.configure(image=newImage)
        self.resultImage.image = newImage

    def printImage(self, response):
        # Display the updated monster's image
        imgLoc = 'images/' + response['name'] + '.png'
        if exists(imgLoc):
            im = Image.open(imgLoc).resize((200,200))
            newImage = ImageTk.PhotoImage(im)
            self.resultImage.configure(image=newImage)
            self.resultImage.image = newImage
        else:
            self.displayBlank()

    # Button Code
    def handleGetMonsterButton(self, characterList, diff, monsterWindow):
        minEncounterXP, maxEncounterXP = self.getAppropriateCR(characterList, diff)
        responseList = self.responseListAdapter(minEncounterXP, maxEncounterXP, monsterWindow)
        # Get top result
        if len(responseList) > 0:
            encounter = self.encounterGenerator(minEncounterXP, maxEncounterXP, responseList, characterList)
            responseText = self.printAdapter(encounter[0][0])
            self.printImage(encounter[0][0])
            responseList = self.printList(encounter)
        else:
            responseText = "Sorry, no monsters found, try adding more terms"
            responseList = ""
            resultDesc = ""
            self.displayBlank()
            self.resultDesc.set(resultDesc)

        self.result.set(responseText)
        self.resultList.set(responseList)
