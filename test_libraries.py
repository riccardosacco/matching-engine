from elasticsearch_metadata import ElasticSearch

db = ElasticSearch(
    "https://search-matching-engine-uv2ckzsmrpytmltjko7x5jf4ra.eu-west-1.es.amazonaws.com", index="item_index")

newDocument = {
    "masterUUID": "ba4796ad-ce31-4529-9960-b7b20b0a4012", "providerData": [
        {
            "providerID": "DATATV_01",
            "UUID": "ba4796ad-ce31-4529-9960-b7b20b0a4012", "title": "Il favoloso mondo di Amèlie", "director": "Jean-Pierre Jeunet", "production_year": 2001
        }
    ]
}

print(db.create_document(newDocument))
