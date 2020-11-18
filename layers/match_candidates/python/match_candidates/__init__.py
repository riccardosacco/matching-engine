import boto3

class AliasManagement:
  def __init__(self, bucket_name: str = "alias-management"):
    self.s3_client = boto3.resource(
      service_name='s3',
      region_name='eu-west-1'
    )
    self.bucket_name = bucket_name

  def _create_file(self, filename: str, content: str) -> bool:
    """Create file

    Args:
        filename (str): File name without extension
        content (str): Content as string

    Returns:
        boolean: True or False
    """

    try:
      self.s3_client.Object(self.bucket_name, '%s.txt'%(filename)).put(Body=content)
      return True
    except:
      return False

  def _get_file(self, filename: str):
    """Get file

    Args:
        filename (str): File name without extension

    Returns:
        string: File content or False
    """
    try:
      obj = self.s3_client.Object(self.bucket_name, '%s.txt'%(filename))
      body = obj.get()['Body'].read().decode('ascii')
      return body
    except:
      return False

    
  def create_alias(self, masterUUID: str, aliasUUID: str) -> bool:
    """Create alias

    Args:
        masterUUID (str): Master UUID
        aliasUUID (str): Alias UUID

    Returns:
        bool: True or False
    """
    file_content = self._get_file(masterUUID)

    # 1. Check if masterUUID file exists
    if(file_content):
      # If true
      alias_array = file_content.split("\n")

      # Check if alias is already in file_content
      if(aliasUUID not in alias_array):
        file_content += "\n%s" % (aliasUUID)
        return self._create_file(masterUUID, file_content)
      else:
        # Alias already in file_content
        return False
    else:
      # If false create file with aliasUUID
      return self._create_file(masterUUID, aliasUUID)