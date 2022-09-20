import requests
import json

# API Url to retrieve all monsters
monster_url = "https://www.dnd5eapi.co/api/monsters/"
responseList = requests.get(monster_url).json().get("results")

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
        description = monsterObj["desc"]
    else:
        description = ""
    
    special_abilities = monsterObj["special_abilities"]
    special_abilities_desc = ""
    
    actions = monsterObj["actions"]
    actions_desc = ""
    
    for ability in special_abilities:
        special_abilities_desc += ability["desc"] + ' '
        
    for action in actions:
        actions_desc += action["desc"] + ' '
        
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
        'actions_desc': actions_desc,
        'special_abilities_desc': special_abilities_desc,
        'description': description
    }
    
    monsterList.append(document)
    
# Write json list to a file
json_str = json.dumps(monsterList, indent=4)

with open("json/data.json", "w") as file:
    file.write(json_str)
