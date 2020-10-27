import json
from package import requests


class ElasticSearch:
    def __init__(self, ELASTIC_URL):
        """
        ElasticSearch Class

        Usage:
            >>> from query_management import execute_query

            # Instantiate DB class with ElasticSearch URL
            >>> db = execute_query.ElasticSearch(ELASTIC_URL)

          Params: 
            - ELASTIC_URL: Elastic Search URL string
        """
        self._ELASTIC_URL = ELASTIC_URL

    def query(self, query):
        """
        Query ElasticSearch database

        Usage:
            >>> from query_management import execute_query

            # Instantiate DB class with ElasticSearch URL
            >>> db = execute_query.ElasticSearch(ELASTIC_URL)

            # Execute query with metadata object
            >>> db.query(query)

        Params:
          - query: Query object (in JSON format)

        Return: Query result Object
        """
        res = requests.post(self._ELASTIC_URL, {}, query)
        return json.loads(res.text)
