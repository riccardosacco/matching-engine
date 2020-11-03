from elasticsearch_metadata import ElasticSearch

db = ElasticSearch(
    "https://search-matching-engine-uv2ckzsmrpytmltjko7x5jf4ra.eu-west-1.es.amazonaws.com", index="item_index")

newDocument = {
    "masterUUID": "ba4796ad-ce31-4529-9960-b7b20b0a4012",
    "providerData": []
}

metadata = {
    "providerID": "DATATV_02",
    "UUID": "ba4796ad-ce31-4529-9960-b7b20b0a4012",
    "title": "Il favoloso mondo di Amèlie",
    "director": "Jean-Pierre",
    "production_year": 2001
}

insertResult = db.create_document(newDocument)

addResult = db.add_metadata(insertResult["_id"], metadata)

metadataUpdate = {
    "providerID": "DATATV_02",
    "title": "Il fantasmagorico mondo di Amelie",
    "production_year": 2004
}

updateResult = db.update_metadata(insertResult["_id"], metadataUpdate)

print(addResult)
