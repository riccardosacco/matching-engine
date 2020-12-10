import json

from query_management.query_fields.providerID import generate_providerID
from query_management.query_fields.alternativeID import generate_alternativeID
from query_management.query_fields.title import generate_title
from query_management.query_fields.director import generate_director
from query_management.query_fields.year import generate_year
from query_management.query_fields.genre import generate_genre

def generate_query(matchitems, min_threshold = 70):
    """
    Generate ElasticSearch query in JSON format
    Usage:
        >>> from query_management import item_programme
        >>> item_programme.generate_query(matchitems)
    Params:
        - matchitems: [{
            query_providerID: string,
            query_alternativeIDs: array[string],
            query_titles: array[string],
            query_directors: array[string],
            query_year: string
            filter_genre: string
        }]
    Return: Query Object (in JSON format)
    """
    json_output_query = ""

    for metadata in matchitems:
        query_providerID = metadata.get("query_providerID")
        query_alternativeIDs = metadata.get("query_alternativeIDs")
        query_titles = metadata.get("query_titles")
        query_directors = metadata.get("query_directors")
        query_year = metadata.get("query_year")
        filter_genre = metadata.get("filter_genre")
		
        json_metadata_query = {
            "min_score": min_threshold,
        #   "_source": ["masterUUID","providerData.UUID","providerData.providerInfo"],
            "query": {
                "bool": {
                    "should": [],
                    "filter": []
                }
            },
        }

        if query_providerID:
            max_score = 10000
            nested_providerID = generate_providerID(query_providerID,max_score)
            json_metadata_query["query"]["bool"]["should"].append(nested_providerID)

        if query_alternativeIDs:
            max_score = 1000
            nested_alternativeID = generate_alternativeID(query_alternativeIDs,max_score)
            json_metadata_query["query"]["bool"]["should"].append(nested_alternativeID)

        if query_titles:
            max_score = 50

            nested_title = generate_title(query_titles, max_score)
            json_metadata_query["query"]["bool"]["should"].append(nested_title)

        if query_directors:
            max_score = 25

            nested_director = generate_director(query_directors, max_score)
            json_metadata_query["query"]["bool"]["should"].append(nested_director)

        if query_year:
            max_score = 25

            nested_year = generate_year(query_year, max_score)
            json_metadata_query["query"]["bool"]["should"].append(nested_year)

        if filter_genre:
            nested_genre = generate_genre(filter_genre)
            json_metadata_query["query"]["bool"]["filter"].append(nested_genre)

        if query_titles or query_directors or query_year:
            json_output_query += "{}\n" + json.dumps(json_metadata_query) + "\n"
    
    return json_output_query