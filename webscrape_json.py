"""Module json for dealing with JSON files."""
import json
import time
from os.path import exists
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

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

# API Url to retrieve all monsters
MONSTER_URL = "https://www.dnd5eapi.co/api/monsters/"
responseList = requests.get(MONSTER_URL).json().get("results")
monsterList = []

for response in responseList:
    fileLoc = "json/" + response['name'] + ".json"
    badFileLoc = "json/1" + response['name'] + ".json" # Lets me know which files need redone

    if response['name'] == "Succubus/Incubus": # Cornercase naming convention
        fileLoc = "json/Succubus+Incubus.json"
        badFileLoc = "json/1Succubus+Incubus.json"

    if exists(fileLoc):
        # API url to retrieve monster info
        print(response['name'])
        description, imageURL = webScrape(response)
        # JSON object for a monster
        document = {
            'description': description,
            'imageURL': imageURL
        }

        # Update json
        with open(fileLoc, "r") as jsonFile:
            currentJson = json.load(jsonFile)

            currentJson.update(document)

        monsterList.append(currentJson)

        # prints the json to either a good file or a 'bad' one for inspection
        if description != "" and imageURL is not None:

            with open(fileLoc, "w", encoding="utf8") as file:
                file.write(currentJson)
        else:
            # Write bad json list to a file
            with open(badFileLoc, "w", encoding="utf8") as file:
                file.write(currentJson)

json_str = json.dumps(monsterList, indent=4)

with open("json/data.json", "w", encoding="utf8") as file:
    file.write(json_str)
