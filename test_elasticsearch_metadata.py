from matching_engine.elasticsearch_metadata import ElasticSearch
from matching_engine.query_management import execute_query
from matching_engine.alias_management import AliasManagement

db = ElasticSearch(
    "https://search-matching-engine-uv2ckzsmrpytmltjko7x5jf4ra.eu-west-1.es.amazonaws.com", index="item_index")

print(AliasManagement)