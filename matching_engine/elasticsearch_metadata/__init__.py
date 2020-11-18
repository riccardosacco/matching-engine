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
        elif(method == "delete"):
            res = json.loads(requests.delete(self._url + "/" + params).text)
        return res

    def get_document(self, doc_id):
        """Get document by id

        Args:
            doc_id (string): Document ID

        Returns:
            object: ElasticSearch _source object
        """
        result = self.query(params="_doc/%s" % (doc_id), method="get")

        if "_source" in result:
            return result["_source"]
        else:
            return False

    def create_document(self, masterUUID, metadata):
        """Create new document on ElasticSearch

        Args:
            masterUUID (string): MasterUUID
            metadata (object): Metadata object

        Returns: Document ID of new object
        """

        newDocument = {
            "masterUUID": masterUUID,
            "providerData": [metadata]
        }

        result = self.query(newDocument, params="_doc")
        return result["_id"]

    def delete_document(self, doc_id) -> bool:
        result = self.query(method="delete", params="_doc/%s" % (doc_id))

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

        # Get metadata
        oldMetadata = self.get_metadata(doc_id, metadata)
        
        if oldMetadata == False:
            return False
        
        try:
            # Iterate over metadata
            for key, value in metadata.items():

                # If metadata value is list don't override
                if type(value) is list:
                    for item in value:
                        # If type is equal to SCHED add if not exists and keep the others
                        if item.get("type") == "SCHED":
                            for keyObj, valueObj in item:
                                pass

                        # If type is equal to ENRICH replace all ENRICH with the new item
                        elif item.get("type") == "ENRICH":
                            pass
                        
                        # If no type is specified add if not exists
                        else:
                            pass


                # If metadata value is dictionary
                elif type(value) is dict:
                    for keyObj, valueObj in value.items():
                        oldMetadata[key][keyObj] = valueObj

                # If metadata value is string
                elif type(value) is str:
                    oldMetadata[key] = value

                # If metadata value is boolean
                elif type(value) is bool:
                    oldMetadata[key] = value

        except:
            return False
        
        print(oldMetadata)


        updateMetadataQuery = {
            "script": {
                "source": """
                    def targets = ctx._source.providerData.findAll(data -> data.providerInfo.providerID == params.providerInfo.providerID);
                    for(data in targets) {
                        for(metadata in data.entrySet()){
                            if(params.containsKey(metadata.getKey())){
                                data[metadata.getKey()] = params[metadata.getKey()]
                            }
                        }
                    }""",
                "params": oldMetadata
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
                "source": "ctx._source.providerData.removeIf(data -> data.providerInfo.providerID == params.providerInfo.providerID)",
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
        if metadata_source["providerInfo"]["providerID"] == metadata_match["providerInfo"]["providerID"]:
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

    def get_document_by_UUID(self, masterUUID):
        """Get document by UUID

        Args:
            masterUUID (string): Master UUID

        Returns:
            object: ES object
        """

        # Create query by masterUUID
        queryUUID = {
            "query": {
                "match": {
                    "masterUUID": masterUUID
                }
            }
        }

        # Query ES
        result = self.query(queryUUID, params="_search")

        # If document is found
        if(len(result["hits"]["hits"]) != 0):
            document = result["hits"]["hits"][0]["_source"]
        else:
            document = False

        return document

    def add_metadata_by_UUID(self, masterUUID, metadata):
        queryUUID = {
            "query": {
                "match": {
                    "masterUUID": masterUUID
                }
            },
            "script": {
                "source": "ctx._source.providerData.add(params)",
                "params": metadata
            }
        }

        return self.query(queryUUID, params="_update_by_query")

    def delete_metadata_by_UUID(self, masterUUID, UUID):
        removeQueryUUID = {
            "query": {
                "match": {
                    "masterUUID": masterUUID
                }
            },
            "script": {
                "source": "ctx._source.providerData.removeIf(data -> data.UUID == params.UUID)",
                    "params": {
                        "UUID": UUID
                    }
            }
        }

        return self.query(removeQueryUUID, params="_update_by_query")

    def move_metadata_to_existing(self, source_doc_id, dest_doc_id, metadata) -> bool:
        """Move metadata to existing document

        Args:
            source_doc_id (string): Source document ID
            dest_doc_id (string): Destination document ID
            metadata (object): Metadata Object
        """

        try:
            # Delete metadata from ES document
            self.delete_metadata(source_doc_id, metadata["providerInfo"]["providerID"])

            # Add metadata to destination ES document
            self.add_metadata(dest_doc_id, metadata)

            return True
        except:
            return False
        
    def move_metadata_to_new(self, source_doc_id, dest_UUID, metadata):
        """Move metadata to existing document

        Args:
            source_doc_id (string): Source document ID
            dest_UUID (string): Destination Master UUID
            metadata (object): Metadata Object
        """

        # Delete metadata from source_doc_id
        self.delete_metadata(source_doc_id, metadata["providerInfo"]["providerID"])

        # Create document and return document ID
        return self.create_document(dest_UUID, metadata)