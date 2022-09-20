from elasticsearch import Elasticsearch

es = Elasticsearch([{'host': 'localhost', 'port': 9200, 'scheme': 'http'}])

result = es.search(
  index='monster',
  query={
      "match_all": {}
  }
)

print(result['hits']['hits'])