from elasticsearch_metadata import ElasticSearch

db = ElasticSearch(
    "https://search-matching-engine-uv2ckzsmrpytmltjko7x5jf4ra.eu-west-1.es.amazonaws.com", index="item_index")

document = {
    "masterUUID": "ba4796ad-ce31-4529-9960-b7b20b0a4012",
    "providerData": [
        {
            "providerID": "DATATV_02",
            "UUID": "ba4796ad-ce31-4529-9960-b7b20b0a4012",
            "title": "Il favoloso mondo di Amèlie",
            "director": "Jean-Pierre",
            "production_year": 2001
        }
    ]
}


def test_create_document():
    newResult = db.create_document(document)

    doc_id = newResult

    inserted = db.get_document(doc_id)

    db.delete_document(doc_id)

    assert document == inserted


def test_update_document():

    newResult = db.create_document(document)

    doc_id = newResult["_id"]

    updateMetadata = {
        "providerID": "DATATV_02",
        "production_year": 2001
    }

    db.update_metadata(doc_id, updateMetadata)

    updated = db.get_document(doc_id)

    db.delete_document(doc_id)

    document["providerData"][0]["production_year"] = updateMetadata["production_year"]

    assert document == updated
