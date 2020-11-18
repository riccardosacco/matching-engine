import json

from query_management.query_fields.providerID import generate_providerID
from query_management.query_fields.title import generate_title
from query_management.query_fields.director import generate_director
from query_management.query_fields.year import generate_year

def generate_query(metadata):
    """
    Generate ElasticSearch query in JSON format
    Usage:
        >>> from query_management import item_programme
        >>> item_programme.generate_query(metadata)
    Params:
        - metadata: {
            query_providerID: string,
            query_titles: array[string],
            query_directors: array[string],
            query_year: string
        }
    Return: Query Object (in JSON format)
    """

    query_providerID = metadata.get("query_providerID")
    query_titles = metadata.get("query_titles")
    query_directors = metadata.get("query_directors")
    query_year = metadata.get("query_year")

    json_provider_query = {
        "query": {
            "nested": {
                "path": "providerData",
                "query": {}
            }
        }
    }

    json_metadata_query = {
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

    if query_directors:
        scores = {
            "director_InitialsFuzzy": "20",
            "director_ORFuzzy": "25"
        }

        nested_director = generate_director(query_directors, scores)
        json_metadata_query["query"]["bool"]["should"].append(nested_director)

    if query_year:
        nested_year = generate_year(query_year)
        json_metadata_query["query"]["bool"]["should"].append(nested_year)

    if query_titles or query_directors or query_year:
        json_output_query += "{}\n" + json.dumps(json_metadata_query)

    return json_output_query