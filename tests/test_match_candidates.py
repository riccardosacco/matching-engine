from matching_engine.match_candidates import MatchCandidates

alias = MatchCandidates()

masterUUID = "60e973da-e82e-4490-9741-001e0249e429"
aliasUUID = "b4bb031c-f0d0-4298-96a5-8cb6de956130"
aliasUUID2 = "0dacf1cb-9f90-4ad8-9e6c-c58dbb4b7ce9"


def test_create_alias():
  alias.create_alias(masterUUID, aliasUUID)

  aliases = alias.get_aliases(masterUUID)

  assert aliasUUID in aliases, "create_alias() must insert the UUID in the file"

  alias.create_alias(masterUUID, aliasUUID)

  aliases = alias.get_aliases(masterUUID)

  assert aliasUUID in aliases and len(aliases) == 1, "create_alias() must not create the file if already exists"

  alias.unalias(masterUUID, aliasUUID)



def test_unalias():
  alias.create_alias(masterUUID, aliasUUID)
  alias.create_alias(masterUUID, aliasUUID2)

  alias.unalias(masterUUID, aliasUUID2)

  aliases = alias.get_aliases(masterUUID)
  
  assert aliasUUID in aliases and len(aliases) == 1, "unalias() must remove the UUID from the file keeping existing"

  alias.unalias(masterUUID, aliasUUID)

  aliases = alias.get_aliases(masterUUID)

  assert len(aliases) == 0, "unalias() must delete the file if there are no UUID inside it"

