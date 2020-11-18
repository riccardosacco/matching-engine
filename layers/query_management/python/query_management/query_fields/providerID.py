def generate_providerID(query_providerID):
    return {
        "script_score": {
            "query": {
                "match": {
                    "providerData.providerInfo.providerID": query_providerID
                }
            },
            "script": {
                "source": "1000"
            }
        }
    }