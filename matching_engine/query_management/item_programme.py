import json

from query_management.query_fields.providerID import generate_providerID
from query_management.query_fields.enrichedUUID import generate_enrichedUUID
from query_management.query_fields.alternativeID import generate_alternativeID
from query_management.query_fields.title import generate_title
from query_management.query_fields.director import generate_director
from query_management.query_fields.year import generate_year
from query_management.query_fields.genre import generate_genre
from query_management.query_fields.emptyField import generate_emptyField

def generate_query(matchitems, min_threshold = 70):
    """
    Generate ElasticSearch query in JSON format
    Usage:
        >>> from query_management import item_programme
        >>> item_programme.generate_query(matchitems)
    Params:
        - matchitems: [{
            query_providerID: string,
            query_enrichedUUID: string,
            query_alternativeIDs: array[string],
            query_titles: array[string],
            query_directors: array[string],
            query_year: string,
            filter_genre: string
        }]
    Return: Query Object (in JSON format)
    """
    json_output_query = ""
    title_max_score = 50
    director_max_score = 25
    year_max_score = 25

    for metadata in matchitems:
        query_providerID = metadata.get("query_providerID")
        query_enrichedUUID = metadata.get("query_enrichedUUID")
        query_alternativeIDs = metadata.get("query_alternativeIDs")
        query_titles = metadata.get("query_titles")
        query_directors = metadata.get("query_directors")
        query_year = metadata.get("query_year")
        filter_genre = metadata.get("filter_genre")

        json_query = {
            "min_score": min_threshold,
        #   "_source": ["masterUUID","providerData.UUID","providerData.providerInfo"],
            "query": {
                "bool": {
                    "should": []
                }
            },
        }

        if query_providerID:
            max_score = 100000
            nested_providerID = generate_providerID(query_providerID,max_score)
            json_query["query"]["bool"]["should"].append(nested_providerID)

        if query_enrichedUUID:
            max_score = 10000
            nested_enrichedUUID = generate_enrichedUUID(query_enrichedUUID,max_score)
            json_query["query"]["bool"]["should"].append(nested_enrichedUUID)

        if query_alternativeIDs:
            max_score = 1000
            nested_alternativeID = generate_alternativeID(query_alternativeIDs,max_score)
            json_query["query"]["bool"]["should"].append(nested_alternativeID)

        json_metadata_query = {
            "bool": {
                "should": [],
                "filter": []
            }
        }
   
        if query_directors:
            nested_director = generate_director(query_directors, director_max_score)
            empty_director = generate_emptyField("directors",director_max_score)
            json_metadata_query["bool"]["should"].append(nested_director)
            json_metadata_query["bool"]["should"].append(empty_director)
        else: 
            title_max_score = title_max_score + director_max_score
   
        if query_year:
            nested_year = generate_year(query_year, year_max_score)
            empty_year = generate_emptyField("productionYears",year_max_score)
            json_metadata_query["bool"]["should"].append(nested_year)
            json_metadata_query["bool"]["should"].append(empty_year)
        else: 
            title_max_score = title_max_score + year_max_score

        nested_title = generate_title(query_titles, title_max_score)
        json_metadata_query["bool"]["should"].append(nested_title)

        nested_genre = generate_genre(filter_genre)
        json_metadata_query["bool"]["filter"].append(nested_genre)

        json_query["query"]["bool"]["should"].append(json_metadata_query)

        json_output_query += "{}\n" + json.dumps(json_query) + "\n"
    
    return json_output_query