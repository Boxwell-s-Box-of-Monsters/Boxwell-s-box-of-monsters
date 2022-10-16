"""Module json for dealing with JSON files."""
import sys
import json
import time
from os.path import exists
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# API Url to retrieve all monsters
MONSTER_URL = "https://www.dnd5eapi.co/api/monsters/"
responseList = requests.get(MONSTER_URL).json().get("results")
monsterList = []

def webScrape(monsterResponse):
    # Find page with the monster's image
    headers = {
    "referer":"referer: https://www.google.com/",
    "user-agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
    (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"
    }
    s = requests.Session()
    searchTerm = "https://www.google.com/search?q=\"ForgottenRealms\" " + monsterResponse['name']
    googleSearch = s.get(searchTerm, headers=headers)
    print(googleSearch)
    soup = BeautifulSoup(googleSearch.text, 'html.parser')
    webpage = soup.find("div", {"class": "yuRUbf"})
    webpage = webpage.find("a", href=True)['href']
    time.sleep(5)
    return descriptionAdapter(webpage), imageAdapter(s, headers, webpage)

def descriptionAdapter(webpage):
    # scrape javascript generated text
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(webpage)
    parapgrah = driver.find_elements(By.CLASS_NAME, "mw-parser-output")
    text = ""
    for p in parapgrah:
        text += " " + p.text

    parapgrah = driver.find_elements(By.TAG_NAME, "p")
    for p in parapgrah:
        text += " " + p.text
    return text

def imageAdapter(session, headers, webpage):
    # Find the url for the monster's image
    forgottenRealms = session.get(webpage, headers=headers)
    soup = BeautifulSoup(forgottenRealms.text, 'html.parser')
    img = soup.find("a", {"class": "image image-thumbnail"})
    if img is None:
        return None
    return img['href']

def initialize(fileLocInit, responseInit):
    # Skips existing files
    if not exists(fileLocInit):
        # API url to retrieve monster info
        monsterObj = requests.get("https://www.dnd5eapi.co" + responseInit['url']).json()
        special_abilities = monsterObj["special_abilities"]
        SPECIAL_ABILITIES_DESC = ""
        actions = monsterObj["actions"]
        ACTIONS_DESC = ""
        for ability in special_abilities:
            SPECIAL_ABILITIES_DESC += ability["desc"] + ' '
        for action in actions:
            ACTIONS_DESC += action["desc"] + ' '
        description = ""
        imageURL = ""

        # JSON object for a monster
        document = {
            'name': monsterObj["name"],
            'hit_points': monsterObj["hit_points"],
            'hit_dice': monsterObj["hit_dice"],
            'armor_class': monsterObj["armor_class"],
            'challenge_rating': monsterObj["challenge_rating"],
            'strength': monsterObj["strength"],
            'dexterity': monsterObj["dexterity"],
            'constitution': monsterObj["constitution"],
            'intelligence': monsterObj["intelligence"],
            'wisdom': monsterObj["wisdom"],
            'charisma': monsterObj["charisma"],
            'actions_desc': ACTIONS_DESC,
            'special_abilities_desc': SPECIAL_ABILITIES_DESC,
            'description': description,
            'imageURL': imageURL
        }
        # Write json list to a file
        json_str_init = json.dumps(document, indent=4)

        with open(fileLocInit, "w", encoding="utf8") as fileInit:
            fileInit.write(json_str_init)
        return document
    return None

def modify(fileLocMod, responseMod):
    if exists(fileLoc):
        # API url to retrieve monster info
        monsterObj = requests.get("https://www.dnd5eapi.co" + responseMod['url']).json()
        print(monsterObj) # To get pylint to shut up about unused variables, remove when necessary
        # Add keys to the document, ex: name = monsterObj["name"]
        # JSON object for a monster
        document = {
            # ex: 'name': name
        }
        # updates the json to either a good file or a 'bad' one for inspection
        with open(fileLocMod, "r") as jsonFile:
            currentJson = json.load(jsonFile)
            currentJson.update(document)
            return currentJson
    return None

def webscrape(fileLocWeb, responseWeb):
    if exists(fileLocWeb):
        badFileLocWeb = "json/1" + response['name'] + ".json"

        if responseWeb['name'] == "Succubus/Incubus": # Cornercase naming convention
            fileLocWeb = "json/Succubus+Incubus.json"
            badFileLocWeb = "json/1Succubus+Incubus.json"
        # API url to retrieve monster info
        description, imageURL = webScrape(responseWeb)
        # JSON object for a monster
        document = {
            'description': description,
            'imageURL': imageURL
        }

        # Update json
        with open(fileLocWeb, "r") as jsonFile:
            currentJson = json.load(jsonFile)

            currentJson.update(document)


        # prints the json to either a good file or a 'bad' one for inspection
        if description != "" and imageURL is not None:

            with open(fileLocWeb, "w", encoding="utf8") as fileWeb:
                fileWeb.write(currentJson)
        else:
            # Write bad json list to a file
            with open(badFileLocWeb, "w", encoding="utf8") as fileWeb:
                fileWeb.write(currentJson)

        return currentJson
    return None

for response in responseList:
    fileLoc = "json/" + response['name'] + ".json"
    if response['name'] == "Succubus/Incubus": # Cornercase naming convention
        fileLoc = "json/Succubus+Incubus.json"
    print(response['name'])
    # Alternates functionalitty based on command line argument
    if len(sys.argv) == 2:
        if sys.argv[1] == "initialize":
            monsterList.append(initialize(fileLoc, response))
        elif sys.argv[1] == "webscrape":
            monsterList.append(webscrape(fileLoc, response))
        elif sys.argv[1] == "modify":
            monsterList.append(modify(fileLoc, response))

json_str = json.dumps(monsterList, indent=4)

with open("json/data.json", "w", encoding="utf8") as file:
    file.write(json_str)
