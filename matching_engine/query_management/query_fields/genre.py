def generate_genre(filter_genre):
    return {"nested": {"path": "providerData", "query": { "term":{"providerData.genre": filter_genre}}}}