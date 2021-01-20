import json

from query_management.query_fields.providerID import generate_providerID
from query_management.query_fields.title import generate_title
from query_management.query_fields.year import generate_year
from query_management.query_fields.genre import generate_genre
from query_management.query_fields.emptyField import generate_emptyField

def generate_query(matchitems, min_threshold = 70):
    """
    Generate ElasticSearch query in JSON format
    Usage:
        >>> from query_management import item_series
        >>> item_series.generate_query(metadata)
    Params:
        - metadata: {
            query_providerID: string,
            query_titles: array[string],
            query_year: string,
            filter_genre: string
        }
    Return: Query Object (in JSON format)
    """
    
    json_output_query = ""
    title_max_score = 70
    year_max_score = 30

    for metadata in matchitems:
       query_providerID = metadata.get("query_providerID")
       query_titles = metadata.get("query_titles")
       query_year = metadata.get("query_year")
       filter_genre = metadata.get("filter_genre")
    
       json_query = {
            "min_score": min_threshold,
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
    
       if query_titles or query_year:
           json_metadata_query = {
               "bool": {
                   "should": [],
                   "filter": []
               }
           }
    
           if query_titles:
               nested_title = generate_title(query_titles, title_max_score)
               json_metadata_query["bool"]["should"].append(nested_title)
          
           if query_year:
               nested_year = generate_year(query_year, year_max_score)
               #empty_year = generate_emptyField("productionYears",year_max_score)
               json_metadata_query["bool"]["should"].append(nested_year)
               #json_metadata_query["bool"]["should"].append(empty_year)
    
           nested_genre = generate_genre(filter_genre)
           json_metadata_query["bool"]["filter"].append(nested_genre)
    
           json_query["query"]["bool"]["should"].append(json_metadata_query)
    
       json_output_query += "{}\n" + json.dumps(json_query) + "\n"

    return json_output_query