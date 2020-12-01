from matching_engine.query_management import item_programme

from matching_engine.query_management import execute_query

db = execute_query.ElasticSearch("https://search-matching-engine-uv2ckzsmrpytmltjko7x5jf4ra.eu-west-1.es.amazonaws.com/programme_index/_msearch")

metadata = {
  "query_providerID": "DTV_01", 
  "query_titles": ["Chernobyl", "Chernobyl Serie2", "Chernobyl Serie"], 
  "query_directors": ["Johan Renck", "J.Renck"], 
  "query_year": "2019"
}

query = item_programme.generate_query(metadata)

print(query)

result = db.query(query)

print(result)