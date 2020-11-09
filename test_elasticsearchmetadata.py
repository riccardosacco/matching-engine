from elasticsearch_metadata import ElasticSearch

db = ElasticSearch(
    "https://search-matching-engine-uv2ckzsmrpytmltjko7x5jf4ra.eu-west-1.es.amazonaws.com", index="item_index")

newDocument = {
    "masterUUID": "ba4796ad-ce31-4529-9960-b7b20b0a4012",
    "providerData": []
}

# insertResult = db.create_document(newDocument)

# print(insertResult)

# metadata = {
#     "providerID": "DATATV_02",
#     "UUID": "ba4796ad-ce31-4529-9960-b7b20b0a4012",
#     "title": "Il favoloso mondo di Amèlie",
#     "director": "Jean-Pierre",
#     "production_year": 2001
# }

# addResult = db.add_metadata(insertResult["_id"], metadata)

# metadata = {
#     "providerID": "DATATV_05",
#     "UUID": "ba4796ad-ce31-4529-9960-b7b20b0a4012",
#     "title": "Il favoloso mondo di Amèlie",
#     "director": "Jean-Pierre",
#     "production_year": 2001
# }

# addResult = db.add_metadata(insertResult["_id"], metadata)

# metadataUpdate = {
#     "providerID": "DATATV_02",
#     "title": "Il fantasmagorico mondo di Amelie",
#     "production_year": 2004
# }

# updateResult = db.update_metadata(insertResult["_id"], metadataUpdate)

# doc_ids = ["lsPNl3UBAyco7qjQhVGz", "lcPMl3UBAyco7qjQiFHb"]

# getResult = db.get_document(doc_ids[0])

# print(getResult)

# getResult = db.get_document(doc_ids[1])

# print(getResult)

# metadataMove = {
#     "providerID": "DATATV_05"
# }

# moveResult = db.move_metadata_to_existing(doc_ids[0], doc_ids[1], metadataMove)

# print(moveResult)

# metadataRemove = {
#     "providerID": "DATATV_05"
# }

# deleteResult = db.delete_metadata(doc_ids[1], metadataRemove)

# print(deleteResult)
