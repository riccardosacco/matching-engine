from alias_management import AliasManagement

alias = AliasManagement(
    "https://search-matching-engine-uv2ckzsmrpytmltjko7x5jf4ra.eu-west-1.es.amazonaws.com", index="item_index")

masterUUID = "f7bba461-dcd3-4d86-8d0a-3fc4666d5dc4"
aliasUUID = "ba4796ad-ce31-4529-9960-b7b20b0a4012"

print(alias.get_document_by_UUID(masterUUID))

# print(alias.create_alias(masterUUID, "56c5ffbc-cfc7-45ff-84df-9c231fedfbd7"))

# print(alias._get_file(masterUUID))

# print(alias.unalias(masterUUID, aliasUUID))