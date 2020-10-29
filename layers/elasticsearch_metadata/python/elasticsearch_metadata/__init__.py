import json


class ElasticSearch:
    def __init__(self, ELASTIC_URL, INDEX):
        """
        ElasticSearch Class

        Usage:
            >>> from elasticsearch_metadata import ElasticSearch

            # Instantiate DB class with ElasticSearch URL & index
            >>> db = ElasticSearch(ELASTIC_URL, INDEX)

          Params: 
            - ELASTIC_URL: Elastic Search URL string
            - INDEX: Elastic data index
        """
        self._ELASTIC_URL = ELASTIC_URL + "/" + INDEX

    def query(self, query, params=""):
        res = requests.post(self._ELASTIC_URL + "/" + params, {}, query)
        return json.loads(res.text)

    def create_document(self, newDocument):
        result = self.query(newDocument, "_doc/_create")
        return result
