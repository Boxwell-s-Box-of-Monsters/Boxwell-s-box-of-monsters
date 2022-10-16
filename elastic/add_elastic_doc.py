"""Module json for dealing with JSON files."""
import json
from elasticsearch import Elasticsearch

es = Elasticsearch([{'host': 'localhost', 'port': 9200, 'scheme': 'http'}])

# Create new index
es.indices.delete(index='monster_index')
es.indices.create(index="monster_index")

with open('./json/data.json', "r") as monsters:
    json.load(monsters)
    print(monsters)
    for monster in monsters:
        es.index(index='monster_index', document=monster)
