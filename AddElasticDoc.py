from elasticsearch import Elasticsearch
import requests

es = Elasticsearch([{'host': 'localhost', 'port': 9200, 'scheme': 'http'}])

# Create new index
es.indices.delete(index='monster')
es.indices.create(index="monster")

# DnD api

# Aboleth
url_aboleth = "https://www.dnd5eapi.co/api/monsters/aboleth"
response = requests.get(url_aboleth).json()

document_aboleth = {
    'name': response.get('name'),
    'armor_class': response.get('armor_class'),
    'challenge_rating': response.get('challenge_rating'),
    'strength': response.get('strength'),
    'dexterity': response.get('dexterity'),
    'constitution': response.get('constitution'),
    'intelligence': response.get('intelligence'),
    'wisdom': response.get('wisdom'),
    'charisma': response.get('charisma'),
    'description': 'Aboleth are twenty-foot long fish-like creatures with potent psionic abilities. They are considered impossibly ancient, older than humanity itself, and in possession of horrible secrets about the early history of the world. In murky subterranean waters, they enslave entire cities, and turn them into mucous-covered, mindless servitors with the ability to breathe water. '
}

es.index(
    index='monster',
    document=document_aboleth
)

