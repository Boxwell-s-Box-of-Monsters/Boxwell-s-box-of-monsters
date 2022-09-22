"""Module json for dealing with JSON files."""
import json
import requests

# API Url to retrieve all monsters
MONSTER_URL = "https://www.dnd5eapi.co/api/monsters/"
responseList = requests.get(MONSTER_URL).json().get("results")

monsterList = []
for response in responseList:
    # API url to retrieve monster info
    monsterObj = requests.get("https://www.dnd5eapi.co" + response['url']).json()
    name = monsterObj["name"]
    armor_class = monsterObj["armor_class"]
    challenge_rating = monsterObj["challenge_rating"]
    strength = monsterObj["strength"]
    dexterity = monsterObj["dexterity"]
    constitution = monsterObj["constitution"]
    intelligence = monsterObj["intelligence"]
    wisdom = monsterObj["wisdom"]
    charisma = monsterObj["charisma"]
    if "desc" in monsterObj.keys():
        DESCRIPTION = monsterObj["desc"]
    else:
        DESCRIPTION = ""
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
        'description': DESCRIPTION
    }
    monsterList.append(document)
# Write json list to a file
json_str = json.dumps(monsterList, indent=4)

with open("json/data.json", "w", encoding="utf8") as file:
    file.write(json_str)
