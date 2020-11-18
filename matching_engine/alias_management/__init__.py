from matching_engine.elasticsearch_metadata import ElasticSearch

class AliasManagement(ElasticSearch):
  def __init__(self, url, index):
    super().__init__(url, index)

  def create_alias(self, masterUUID, aliasUUID):
    # Search aliasUUID and get metadata array
    document = self.get_document_by_UUID(aliasUUID)

    if document:
      metadata_array = document["providerData"]

      # For each metadata
      for metadata in metadata_array:
      # Add metadata to masterUUID
        self.add_metadata_by_UUID(masterUUID, metadata)

      # Remove metadata from aliasUUID
        self.delete_metadata_by_UUID(aliasUUID, metadata["UUID"])
      return True
    else:
      return False

  def unalias(self, masterUUID, aliasUUID):
    # Search masterUUID
    document = self.get_document_by_UUID(masterUUID)

    if document:
      metadata_array = document["providerData"]

    # Find aliasUUID in metadata array
      metadata_array = [metadata for metadata in metadata_array if metadata["UUID"] == aliasUUID]

    # For each metadata
      for metadata in metadata_array:
        # Add metadata to aliasUUID
        self.add_metadata_by_UUID(aliasUUID, metadata)

        # Remove metadata from masterUUID
        self.delete_metadata_by_UUID(masterUUID, metadata["UUID"])

      return True
    else:
      return False