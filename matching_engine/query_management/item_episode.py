import json

from query_management.query_fields.providerID import generate_providerID
from query_management.query_fields.alternativeID import generate_alternativeID
from query_management.query_fields.title import generate_title
from query_management.query_fields.director import generate_director
from query_management.query_fields.year import generate_year
from query_management.query_fields.seriesTitle import generate_seriesTitle
from query_management.query_fields.episodeNum import generate_episodeNum
from query_management.query_fields.seasonNum import generate_seasonNum
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
            query_year: string,
            query_seriesTitle: array[string],
            query_episodeNum: string,
            query_seasonNum: string,
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
        query_episodeNum = metadata.get("query_episodeNum")
        query_seasonNum = metadata.get("query_seasonNum")
        query_seriesTitle = metadata.get("query_seriesTitle")
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
            max_score = 10000
            nested_providerID = generate_providerID(query_providerID,max_score)
            json_query["query"]["bool"]["should"].append(nested_providerID)

        if query_alternativeIDs:
            max_score = 1000
            nested_alternativeID = generate_alternativeID(query_alternativeIDs,max_score)
            json_query["query"]["bool"]["should"].append(nested_alternativeID)

        if query_titles or query_seriesTitle or query_directors or query_year or query_episodeNum or query_seasonNum:
            json_metadata_query = {
                "bool": {
                    "should": [],
                    "filter": []
                }
            }

            if query_titles:
                max_score = 30
                nested_title = generate_title(query_titles, max_score)
                json_metadata_query["bool"]["should"].append(nested_title)
    
            if query_seriesTitle:
                max_score = 30
                nested_seriesTitle = generate_seriesTitle(query_seriesTitle, max_score)
                json_metadata_query["bool"]["should"].append(nested_seriesTitle)
    
            if query_directors:
                max_score = 20
                nested_director = generate_director(query_directors, max_score)
                json_metadata_query["bool"]["should"].append(nested_director)
    
            if query_year:
                max_score = 20
                nested_year = generate_year(query_year, max_score)
                json_metadata_query["bool"]["should"].append(nested_year)
    
            if query_episodeNum:
                max_score = 10
                nested_episodeNum = generate_episodeNum(query_episodeNum, max_score)
                json_metadata_query["bool"]["should"].append(nested_episodeNum)
    
            if query_seasonNum:
                max_score = 10
                nested_seasonNum = generate_seasonNum(query_seasonNum, max_score)
                json_metadata_query["bool"]["should"].append(nested_seasonNum)
    
            nested_genre = generate_genre(filter_genre)
            json_metadata_query["bool"]["filter"].append(nested_genre)

            json_query["query"]["bool"]["should"].append(json_metadata_query)

        json_output_query += "{}\n" + json.dumps(json_query) + "\n"
    
    return json_output_query