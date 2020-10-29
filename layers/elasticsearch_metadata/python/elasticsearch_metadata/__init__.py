import json
import requests


class ElasticSearch:
    def __init__(self, url, index):
        """
        ElasticSearch Class

        Usage:
            >>> from elasticsearch_metadata import ElasticSearch

            # Instantiate DB class with ElasticSearch URL & index
            >>> db = ElasticSearch(ELASTIC_URL, INDEX)

          Params: 
            - ELASTIC_URL: Elastic Search URL string
            - index: Elastic data index
        """
        self._url = url + "/" + index

    def query(self, query, params=""):
        res = requests.post(self._url + "/" + params, json=query)
        return json.loads(res.text)

    def create_document(self, newDocument):
        """Create new document on ElasticSearch

        Args:
            newDocument (document): New document object

        Returns:
            number: Sequence ID of new object
        """
        result = self.query(newDocument, params="_doc/_create")
        return result["_seq_no"]

    def add_metadata(self, doc_id, provider_content_id, provider_name, metadata):
        return

    def update_metadata(self, doc_id, provider_content_id, provider_name, metadata):
        return

    def delete_metadata(self, doc_id, provider_content_id, provider_name, metadata):
        return

    def move_metadata_to_existing(source_doc_id, dest_doc_id, provider_content_id, provider_name, metadata):
        return

    def move_metadata_to_new(source_doc_id, dest_UUID, provider_content_id, provider_name, metadata):
        return
