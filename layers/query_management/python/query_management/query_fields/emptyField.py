def generate_emptyField(field, max_score):
    return {"script_score": {"query": {"bool": {"must_not": [{"nested": {"path": "providerData." + field.split('.')[0],"query": {"bool": {"must": {"exists": {"field": "providerData." + field + ""}}}}}}]}},"script": {"source": str(max_score)}}}
