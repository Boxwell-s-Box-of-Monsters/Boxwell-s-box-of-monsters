"""Module json for dealing with JSON files."""
import json
from elasticsearch import Elasticsearch

es = Elasticsearch([{'host': 'localhost', 'port': 9200, 'scheme': 'http'}])

# Create new index
es.indices.delete(index='monster')
es.indices.create(index="monster")

# Open JSON file
with open('json/data.json', 'r', encoding="utf8") as openfile:
    # Reading from json file
    json_list = json.load(openfile)

# Add each JSON obj in file to the index
for obj in json_list:
    es.index(
        index='monster',
        document=obj
    )
    print(obj["name"])
