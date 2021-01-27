def generate_enrichedUUID(query_enrichedUUID, max_score):
    return {"nested": {"path": "providerData", "query": {"script_score": {"query": {"term": {"providerData.UUID": query_enrichedUUID}},"script": {"source": str(max_score)}}}}}