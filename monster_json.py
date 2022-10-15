"""Module json for dealing with JSON files."""
import json
from os.path import exists
import requests

# API Url to retrieve all monsters
MONSTER_URL = "https://www.dnd5eapi.co/api/monsters/"
responseList = requests.get(MONSTER_URL).json().get("results")
monsterList = []

for response in responseList:
    fileLoc = "json/" + response['name'] + ".json"

    if response['name'] == "Succubus/Incubus": # Cornercase naming convention
        fileLoc = "json/Succubus+Incubus.json"

    # Skips existing files
    if not exists(fileLoc):
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
        
        # Write json list to a file
        json_str = json.dumps(document, indent=4)
        monsterList.append(document)

        with open(fileLoc, "w", encoding="utf8") as file:
            file.write(json_str)

json_str = json.dumps(monsterList, indent=4)

with open("json/data.json", "w", encoding="utf8") as file:
    file.write(json_str)
