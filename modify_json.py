"""Module json for dealing with JSON files."""
import json
import requests
from os.path import exists

# API Url to retrieve all monsters
MONSTER_URL = "https://www.dnd5eapi.co/api/monsters/"
responseList = requests.get(MONSTER_URL).json().get("results")

for response in responseList:
    fileLoc = "json/" + response['name'] + ".json"
    badFileLoc = "json/1" + response['name'] + ".json" # Lets me know which files need redone

    if response['name'] == "Succubus/Incubus": # Cornercase naming convention
        fileLoc = "json/Succubus+Incubus.json"

    # Skips existing files
    if exists(fileLoc) == True:
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
        damage_vulnerabilities = monsterObj["damage_vulnerabilities"]
        damage_resistances = monsterObj["damage_resistances"]
        damage_immunities = monsterObj["damage_immunities"]
        condition_immunities = monsterObj["condition_immunities"]
        senses = monsterObj["senses"]
        xp = monsterObj["xp"]
        special_abilities = monsterObj["special_abilities"]
        SPECIAL_ABILITIES_DESC = ""
        actions = monsterObj["actions"]
        ACTIONS_DESC = ""
        for ability in special_abilities:
            SPECIAL_ABILITIES_DESC += ability["desc"] + ' '
        for action in actions:
            ACTIONS_DESC += action["desc"] + ' '

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
            'damage_vulnerabilities': damage_vulnerabilities,
            'damage_resistances': damage_resistances,
            'damage_immunities': damage_immunities,
            'condition_immunities': condition_immunities,
            'senses': senses,
            'xp': xp,
        }
    
        # prints the json to either a good file or a 'bad' one for inspection
        
        with open(fileLoc, "r") as jsonFile:
            currentJson = json.load(jsonFile)

            currentJson.update(document)

        json_str = json.dumps(currentJson, indent=4)
        with open(fileLoc, "w", encoding="utf8") as file:
            file.write(json_str)

monsterList = []
for response in responseList:
    fileLoc = "json/" + response['name'] + ".json"

    if response['name'] == "Succubus/Incubus": # Cornercase naming convention
        fileLoc = "json/Succubus+Incubus.json"


    with open(fileLoc, "r", encoding="utf8") as file:
        monsterList.append(json.load(open(fileLoc)))
json_str = json.dumps(monsterList, indent=4)

with open("json/data.json", "w", encoding="utf8") as file:
    file.write(json_str)
