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

    if exists(fileLoc):
        # API url to retrieve monster info
        print(response['name'])
        monsterObj = requests.get("https://www.dnd5eapi.co" + response['url']).json()
        # Add keys to the document, ex: name = monsterObj["name"]

        # JSON object for a monster
        document = {
            # ex: 'name': name
        }
        monsterList.append(json.load(file))
        # updates the json to either a good file or a 'bad' one for inspection
        with open(fileLoc, "r") as jsonFile:
            currentJson = json.load(jsonFile)

            currentJson.update(document)

        json_str = json.dumps(currentJson, indent=4)
        with open(fileLoc, "w", encoding="utf8") as file:
            file.write(json_str)

json_str = json.dumps(monsterList, indent=4)

with open("json/data.json", "w", encoding="utf8") as file:
    file.write(json_str)
