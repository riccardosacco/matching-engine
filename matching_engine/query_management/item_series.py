import json

from query_management.query_fields.providerID import generate_providerID
from query_management.query_fields.title import generate_title

def generate_query(metadata, min_threshold = 70):
    """
    Generate ElasticSearch query in JSON format
    Usage:
        >>> from query_management import item_series
        >>> item_series.generate_query(metadata)
    Params:
        - metadata: {
            query_providerID: string,
            query_titles: array[string]
        }
    Return: Query Object (in JSON format)
    """

    query_providerID = metadata.get("query_providerID")
    query_titles = metadata.get("query_titles")

    json_provider_query = {
        "query": {
            "nested": {
                "path": "providerData",
                "query": {}
            }
        }
    }

    json_metadata_query = {
        "min_score": min_threshold,
        "query": {
            "bool": {
                "should": []
            }
        },
    }

    json_output_query = ""

    if query_providerID:
        provider_query = generate_providerID(query_providerID)
        json_provider_query["query"]["nested"]["query"] = provider_query
        json_output_query += "{}\n" + json.dumps(json_provider_query) + "\n"

    if query_titles:
        scores = {
            "title_exactMatchFuzzy": "50",
            "title_matchPhrase":"45",
            "title_stopWords":"35",
            "title_ORFuzzy": "20"
        }

        nested_title = generate_title(query_titles, scores)
        json_metadata_query["query"]["bool"]["should"].append(nested_title)


    if query_titles:
        json_output_query += "{}\n" + json.dumps(json_metadata_query)

    return json_output_query