import json
from elasticsearch_metadata import ElasticSearch
db = ElasticSearch("https://search-matching-engine-uv2ckzsmrpytmltjko7x5jf4ra.eu-west-1.es.amazonaws.com", index="item_index")

def create_elem(param):
    print('INFO: create_elem')
    ce_response = {'uuid':'', 'error_code':'','newId':''}
    #param = {'provider_id':provider_id,'uuid':q_response[uuid],'title':title, 'production_year':production_year,'director':director}
    try:
        print('INFO: before invoking elastic search create item')
        #elasticsearch_metadata.create_item_doc(param)
        newDocument = {"masterUUID": param['uuid'], "providerData": [
          {
            "providerID": param['provider_id'],
            "UUID": param['uuid'], 
            "title": param['title'], 
            "director": param['director'], 
            "production_year": param['production_year']
          }
         ]
        }
        print(newDocument["providerData"])
        newId = db.create_document(newDocument)
        print(newId)
        print('INFO: after invoking elastic search create item')
    except:
        ce_response['error_code'] = "007" #error creating item
    else:
        ce_response['newId'] = newId
    #TODO: ce_response fields?
    return json.dumps(ce_response)
