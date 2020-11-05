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

    def query(self, query={}, params="", method="post"):
        """Query ElasticSearch

        Args:
            query (object, optional): Query object. Defaults to {}.
            params (string, optional): URL params. Defaults to "".
            method (string, optional): HTTP Method ("get" | "post"). Defaults to "post".

        Returns:
            object: Response from ElasticSearch
        """
        res = False

        if(method == "post"):
            res = json.loads(requests.post(
                self._url + "/" + params, json=query).text)
        elif(method == "get"):
            res = json.loads(requests.get(self._url + "/" + params).text)
        return res

    def get_document(self, doc_id):
        """Get document by id

        Args:
            doc_id (string): Document ID

        Returns:
            object: ElasticSearch _source object
        """
        result = self.query(params="_doc/%s" % (doc_id), method="get")

        return result["_source"]

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
        """Update metadata to existing document

        Args:
            doc_id (string): Document id on ElasticSearch
            metadata (object): Metadata object

        Returns:
            object: Response from ElasticSearch
        """
        updateMetadataQuery = {
            "script": {
                "source": """
                    def targets = ctx._source.providerData.findAll(data -> data.providerID == params.providerID);
                    for(data in targets) {
                        for(metadata in data.entrySet()){
                            if(params.containsKey(metadata.getKey())){
                                data[metadata.getKey()] = params[metadata.getKey()]
                            }
                        }
                    }""",
                "params": metadata
            }
        }

        result = self.query(updateMetadataQuery,
                            params="_update/%s" % (doc_id))

        return result

    def delete_metadata(self, doc_id, metadata):
        """Delete metadata from object

        Args:
            doc_id (string): Document ID on ElasticSearch
            metadata (object): Metadata object

        Returns:
            object: Response from ElasticSearch
        """
        deleteMetadataQuery = {
            "script": {
                "source": "ctx._source.providerData.removeIf(data -> data.providerID == params.providerID)",
                "params": metadata
            }
        }
        result = self.query(deleteMetadataQuery,
                            params="_update/%s" % (doc_id))
        return result

    def _filter_metadata(self, metadata_source, metadata_match) -> bool:
        """Filter metadata function

        Args:
            metadata_source (object): Metadata source object
            metadata_match (object): Metadata to match

        Returns:
            bool: True if object has the same providerID
        """
        if metadata_source["providerID"] == metadata_match["providerID"]:
            return True
        else:
            return False

    def get_metadata(self, doc_id, metadata_match):
        """Get single metadata from document

        Args:
            doc_id (string): Document ID
            metadata_match (object): Metadata match object (with providerID)

        Returns:
            object: Metadata object
        """
        # Get document
        doc = self.get_document(doc_id)

        # Filter metadata
        source_metadata_object = list(
            filter(lambda obj: self._filter_metadata(obj, metadata_match), doc["providerData"]))

        if(len(source_metadata_object) == 1):
            return source_metadata_object[0]
        else:
            return False

    def move_metadata_to_existing(self, source_doc_id, dest_doc_id, metadata_match):
        """Move metadata to existing document

        Args:
            source_doc_id (string): Source document ID
            dest_doc_id (string): Destination document ID
            metadata_match (object): Metadata match Object (with providerID)
        """
        # Get metadata from source object
        source_metadata = self.get_metadata(source_doc_id, metadata_match)

        # Update destination document if found
        if source_metadata:
            # Delete metadata from source object
            self.delete_metadata(source_doc_id, metadata_match)

            # Add metadata to dest document
            return self.add_metadata(dest_doc_id, source_metadata)
        else:
            return False

    def move_metadata_to_new(self, source_doc_id, dest_UUID, metadata_match):
        """Move metadata to existing document

        Args:
            source_doc_id (string): Source document ID
            dest_UUID (string): Destination Master UUID
            metadata_match (object): Metadata match Object (with providerID)
        """
        # Get metadata from source object
        source_metadata = self.get_metadata(source_doc_id, metadata_match)

        if source_metadata:
            newDocument = {
                "masterUUID": dest_UUID,
                "providerData": [source_metadata]
            }

            return self.create_document(newDocument)
        else:
            return False
