from query_management import item_programme

metadata = {
  "query_providerID":"DATA_TV",
  "query_title":"Spider-man",
  "query_director":"Sam Raimi",
  "query_year":"2005"
}

query = item_programme.generate_query(metadata)

print(query)