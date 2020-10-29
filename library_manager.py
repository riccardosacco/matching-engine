from query_management import item_programme
from query_management.execute_query import ElasticSearch

query = item_programme.generate_query({
    "query_title": "Spider-man",
    "query_director": "Sam Raimi",
    "query_year": "2010"
})


db = ElasticSearch(
    "https://search-matching-engine-nhygzot7nqafdvrzb3niwryuay.eu-central-1.es.amazonaws.com/item_index/_search")


print(db.query(query))
