import json
from elasticsearch_metadata import ElasticSearch
db = ElasticSearch("https://search-matching-engine-uv2ckzsmrpytmltjko7x5jf4ra.eu-west-1.es.amazonaws.com", index="item_index")



def update_elem(data):
    print('INFO: update_elem')
    ce_response = {'uuid':'', 'error_code':''}
    #param = {'provider_id':provider_id,'uuid':q_response[uuid],'title':title, 'production_year':production_year,'director':director}
    try:
        print('INFO: before invoking elastic search update item')
         # db.update_document(newDocument) ?
    except expression as identifier:
        ce_response['error_code'] = "008" #error updating item
    #else:
    #TODO: ce_response fields?
    
    return json.dumps(ue_response)
