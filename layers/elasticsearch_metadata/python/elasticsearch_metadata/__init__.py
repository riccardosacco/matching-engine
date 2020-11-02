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
        result = self.query(newDocument, params="_doc")
        return result

    def add_metadata(self, doc_id, metadata):
        """Add metadata to existing document

        Args:
            doc_id (string): Document id on ElasticSearch
            metadata (object): Metadata object

        Returns:
            object: Response from ElasticSearch
        """
        addMetadataQuery = {
            "script": {
                "source": "ctx._source.providerData.add(params)",
                "params": metadata
            }
        }

        result = self.query(addMetadataQuery, params="_update/%s" % (doc_id))
        return result

    def update_metadata(self, doc_id, metadata):
        return

    def delete_metadata(self, doc_id, metadata):
        return

    def move_metadata_to_existing(self, source_doc_id, dest_doc_id, metadata):
        return

    def move_metadata_to_new(self, source_doc_id, dest_UUID, metadata):
        return
