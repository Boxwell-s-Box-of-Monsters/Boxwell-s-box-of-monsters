"""Module json for dealing with JSON files."""
import json
from pickle import TRUE
import requests
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from os.path import exists

def webScrape(response):
    # Find page with the monster's image
    headers = {
    "referer":"referer: https://www.google.com/",
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"
    }
    s = requests.Session()
    searchTerm = "https://www.google.com/search?q=\"ForgottenRealms\" " + response['name']
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
    if img == None:
        return None
    else:
        return img['href']

# API Url to retrieve all monsters
MONSTER_URL = "https://www.dnd5eapi.co/api/monsters/"
responseList = requests.get(MONSTER_URL).json().get("results")

for response in responseList:
    fileLoc = "json/" + response['name'] + ".json"
    badFileLoc = "json/1" + response['name'] + ".json" # Lets me know which files need redone

    if response['name'] == "Succubus/Incubus": # Conercase naming convention
        fileLoc = "json/Succubus+Incubus.json"

    # Skips existing files
    if exists(fileLoc) == False and exists(badFileLoc) == False:
        # API url to retrieve monster info
        print(response['name'])
        monsterObj = requests.get("https://www.dnd5eapi.co" + response['url']).json()
        name = monsterObj["name"]
        hp = monsterObj["hit_points"]
        hit_dice = monsterObj["hit_dice"]
        armor_class = monsterObj["armor_class"]
        challenge_rating = monsterObj["challenge_rating"]
        strength = monsterObj["strength"]
        dexterity = monsterObj["dexterity"]
        constitution = monsterObj["constitution"]
        intelligence = monsterObj["intelligence"]
        wisdom = monsterObj["wisdom"]
        charisma = monsterObj["charisma"]
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
        description, imageURL = webScrape(response)
        # JSON object for a monster
        document = {
            'name': name,
            'hit_points': hp,
            'hit_dice': hit_dice,
            'armor_class': armor_class,
            'challenge_rating': challenge_rating,
            'strength': strength,
            'dexterity': dexterity,
            'constitution': constitution,
            'intelligence': intelligence,
            'wisdom': wisdom,
            'charisma': charisma,
            'actions_desc': ACTIONS_DESC,
            'special_abilities_desc': SPECIAL_ABILITIES_DESC,
            'description': description,
            'imageURL': imageURL
        }
    
        # prints the json to either a good file or a 'bad' one for inspection
        if description != "" || imageURL == None:
            # Write json list to a file
            json_str = json.dumps(document, indent=4)

            with open(fileLoc, "w", encoding="utf8") as file:
                file.write(json_str)
        else:
            # Write bad json list to a file
            json_str = json.dumps(document, indent=4)

            with open(badFileLoc, "w", encoding="utf8") as file:
                file.write(json_str)
