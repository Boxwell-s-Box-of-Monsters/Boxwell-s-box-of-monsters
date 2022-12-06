import tkinter as tk
import random
from os.path import exists
import numpy as np
from transformers import pipeline
from PIL import Image, ImageTk
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from elasticsearch_dsl.query import MoreLikeThis
from elasticsearch_dsl import Q
from Styles import *
from frames.DescriptionFrame import DescriptionFrame
from frames.ResultFrame import ResultFrame
from frames.ImageInputFrame import ImageInputFrame
from Image_Generation import ImageGeneration


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
        monsterImage = Image.open('images/placeholderMonster.png')
        self.monsterImage = ImageTk.PhotoImage(monsterImage)
        # Top Label
        label = tk.Label(self,
                              text="Welcome to the monster library, please enter the relevant information below.",
                              wraplength=500,
                              anchor="center",
                              background=TAN,
                              font=(FONT, 14, "bold"),
                              fg=BLACK)
        label.grid(columnspan=2, row=0, column=0, sticky=tk.NS, **padding)

        #image input frame
        imageInputFrame = ImageInputFrame(self)
        imageInputFrame.grid(column=0, row = 1, sticky=tk.NS, **padding)

        # Description Frame
        descriptFrame = DescriptionFrame(self)
        descriptFrame.grid(column=0, row=2, sticky=tk.NS, **innerPadding, **padding)

        # Get Monster Button and Result
        self.result = tk.StringVar()
        self.result.set("")
        self.resultDesc = tk.StringVar()
        self.resultDesc.set("")
        self.resultList = tk.StringVar()
        self.resultList.set("")

        button = tk.Button(self, text='Create Monster',
                                command=lambda: self.handleCreateMonsterButton(descriptFrame.monsterWindow,
                                                                            imageInputFrame.pilImg))

        button.config(font=(FONT, 10, "bold"),
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
        self.monsterQuantity = 0

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
        potentialMon = []

        for m in potentialMonsters:
            potentialMon.append(m)
        index = self.randomMonsterPicker(potentialMon)
        currentEncounterXP = 0
        encounter = []

        # From the users description, add the paragon monster
        while self.monsterQuantity == 0:
            self.monsterQuantity += self.monstersMultiplied(potentialMon[index],
                                                       currentEncounterXP, maxEncounterXP,
                                                       characterList)
            if self.monsterQuantity == 0:
                potentialMon.remove(potentialMon[index])
                index = self.randomMonsterPicker(potentialMon)
        if len(potentialMon) > 0:
            encounter.append([potentialMon[index], self.monsterQuantity])
            currentEncounterXP += int(potentialMon[index]['xp']) * self.monsterQuantity

            # Make a new list of monsters based on best matches to the paragon monster
            matchingMonsters = self.responseListAdapter(minEncounterXP, (potentialMon[index]['xp'])-1, \
                                                    potentialMon[index]['description'])

            # Adds the best monsters based on the paragon monster to the
            # encounter until the list is empty or the encounter has reached 10
            while len(matchingMonsters) > 0 and self.monsterQuantity < 10:
                # if the number of monsters that can be added is not 0, add it.
                newMonsters = self.monstersMultiplied(matchingMonsters[0],
                                                      currentEncounterXP, maxEncounterXP,
                                                      characterList)
                if newMonsters > 0:
                    encounter.append([matchingMonsters[0], newMonsters])
                    currentEncounterXP += int(matchingMonsters[0]['xp']) * newMonsters
                    self.monsterQuantity += newMonsters

                if len(matchingMonsters) > 1:
                    matchingMonsters = matchingMonsters[1:]
                else:
                    matchingMonsters = []
        return encounter

    def generateMonsterStats(self, monsterWindow):
        responseList = self.responseListAdapter(0, 1000000, monsterWindow)
        values = {
            'hit_points': [],
            'armor_class': [],
            'xp': [],
            'strength': [],
            'dexterity': [],
            'constitution': [],
            'intelligence': [],
            'wisdom': [],
            'charisma': [],
        }
        for response in responseList:
            values['hit_points'].append(response['hit_points'])
            values['armor_class'].append(response['armor_class'])
            values['xp'].append(response['xp'])
            values['strength'].append(response['strength'])
            values['dexterity'].append(response['dexterity'])
            values['constitution'].append(response['constitution'])
            values['intelligence'].append(response['intelligence'])
            values['wisdom'].append(response['wisdom'])
            values['charisma'].append(response['charisma'])
        # Thin out outliers as to make the final result no too extreme
        if len(responseList) > 5:
            values['hit_points'].remove(max(values['hit_points']))
            values['hit_points'].remove(min(values['hit_points']))
            values['armor_class'].remove(max(values['armor_class']))
            values['armor_class'].remove(min(values['armor_class']))
            values['xp'].remove(max(values['xp']))
            values['xp'].remove(min(values['xp']))
        final_values = {
            'hit_points': 0,
            'armor_class': 0,
            'xp': 0,
            'strength': 0,
            'dexterity': 0,
            'constitution': 0,
            'intelligence': 0,
            'wisdom': 0,
            'charisma': 0
        }
        mainStatsNum = 0
        if len(values['hit_points']) == 0:
            # Error text if nothing was ever found, abort rest of execution
            self.result.set("Your monster description must be more descriptive for custom stats.")
            return
        if len(values['hit_points']) > 0:
            mainStatsNum = np.random.randint(0, len(values['hit_points']))
        final_values['hit_points'] = values['hit_points'][mainStatsNum]
        final_values['armor_class'] = values['armor_class'][mainStatsNum]
        final_values['xp'] = values['xp'][mainStatsNum]
        for thing in ['strength', 'dexterity', 'constitution', 'intelligence', 'wisdom', 'charisma']:
            for _ in range(0, int(len(values[thing])/2)-1):
                values[thing].remove(values[thing][np.random.randint(0, len(values[thing])-1)])
            # add one random salt value
            values[thing].append(np.random.randint(1, 25))
            average_num = np.average(values[thing])
            if np.random.randint(0, 1) == 0:
                average_num = np.floor(average_num)
            else:
                average_num = np.ceil(average_num)
            final_values[thing] = int(average_num)
        self.result.set(f"HP: {final_values['hit_points']}  |  Armor Class: {final_values['armor_class']}  |  XP: "
                        f"{final_values['xp']}\n\n"
                        f"Strength: {final_values['strength']}   |   Dexterity: {final_values['dexterity']}   |   "
                        f"Constitution: {final_values['constitution']}\n"
                        f"Intelligence: {final_values['intelligence']}   |   Wisdom: {final_values['wisdom']}   |   "
                        f"Charisma: {final_values['charisma']}")
    # returns an integer for the number of monsters that can be added to the encounter for a specific monster
    def monstersMultiplied(self, monster, currentEncounterXP, maxEncounterXP, characterList):
        # update xpMult according to how many monsters are already in the encounter
        addedMonsters = 0
        xpMult = 1
        if self.monsterQuantity+1 >= 7:
            xpMult = 2.5
        elif self.monsterQuantity+1 >= 3:
            xpMult = 2
        elif self.monsterQuantity+1 == 2:
            xpMult = 1.5

        typeMult = 0
        for character in characterList:
            cDmg = character['damageVar'].get().lower()
            typeMult = 0
            if cDmg in monster['damage_vulnerabilities']:
                typeMult += 0.5
            elif cDmg in monster['damage_resistances']:
                typeMult += 2
            elif cDmg in monster['damage_immunities']:
                typeMult += 4
            else:
                typeMult += 1
        typeMult /= len(characterList)

        # adds the same monster multiple times, taking into account the xp multiplier and the preexisting encounter xp
        acceptableXP = (maxEncounterXP - (currentEncounterXP+typeMult*int(monster['xp']))*xpMult >= 0)
        while acceptableXP and (self.monsterQuantity+addedMonsters < 10):
            addedMonsters += 1
            currentEncounterXP += int(monster['xp'])
            if self.monsterQuantity+addedMonsters+1 >= 7:
                xpMult = 2.5
            elif self.monsterQuantity+addedMonsters+1 >= 3:
                xpMult = 2
            elif self.monsterQuantity+addedMonsters+1 == 2:
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
        if response['name'] == "Succubus/Incubus": # Cornercase naming convention
            imgLoc = "images/Succubus+Incubus.png"
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
            if len(encounter) > 0:
                responseText = self.printAdapter(encounter[0][0])
                self.printImage(encounter[0][0])
                responseList = self.printList(encounter)
            else:
                responseText = "Sorry, all the monsters found were too strong, try adjusting your terms"
                responseList = ""
                resultDesc = ""
                self.displayBlank()
                self.resultDesc.set(resultDesc)
        else:
            responseText = "Sorry, no monsters found, try adding more terms"
            responseList = ""
            resultDesc = ""
            self.displayBlank()
            self.resultDesc.set(resultDesc)

        self.result.set(responseText)
        self.resultList.set(responseList)

    def handleCreateMonsterButton(self, monsterWindow, startImage):
        # generate the monster Image
        descText = monsterWindow.get("1.0",'end-1c')
        image_to_text = pipeline("image-to-text", model="nlpconnect/vit-gpt2-image-captioning", max_new_tokens = 100)
        test = image_to_text(startImage)

        for t in test:
            print(t['generated_text'])
            descText += " " + t['generated_text']

        tempImg = ImageGeneration(startImage, descText)
        self.monsterImage = ImageTk.PhotoImage(tempImg)
        self.resultImage.configure(image=self.monsterImage)

        #genereate and dispaly stats
        self.generateMonsterStats(monsterWindow)
