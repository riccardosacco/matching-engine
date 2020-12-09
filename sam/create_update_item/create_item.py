import json
import time
from elasticsearch_metadata import ElasticSearch  # pylint: disable=import-error
#db = ElasticSearch("https://search-matching-engine-uv2ckzsmrpytmltjko7x5jf4ra.eu-west-1.es.amazonaws.com", index="programme_index")
db = ElasticSearch("https://search-matching-engine-uv2ckzsmrpytmltjko7x5jf4ra.eu-west-1.es.amazonaws.com", index="massive_test_index")
def create_elem(param):
    print('INFO: create_elem')
    ce_response = {'uuid':'', 'error_code':'','newId':''}
    #param = {'provider_id':provider_id,'uuid':q_response[uuid],'title':title, 'production_year':production_year,'director':director}
    try:
        print('INFO: before invoking elastic search create item')
        requestContext = param['request_context']
        title_elems = param['title']
        n_titles = len(title_elems)
        l_titles = []
        for x in range(n_titles):
            curr_title = title_elems[x-1]
            l_titles.append({"type": requestContext,"title": curr_title}) 

        director_elems = param['director']
        n_directors = len(director_elems)
        l_directors = []
        for x in range(n_directors):
            curr_director = director_elems[x-1]
            l_directors.append({"type": requestContext,"director": curr_director}) 
        
        l_years = []
        if (param['production_year']):
            l_years.append({"type": requestContext,"productionYear": param['production_year']}) 
            
        newDocument = { "UUID":param['uuid'],
         "entitySubType":"programme",
         "providerInfo":{
            "providerName":param['provider_name'],
            "providerID":param['provider_id']
         },
         "titles":json.loads(json.dumps(l_titles)),
         "productionYears":json.loads(json.dumps(l_years)),
         "directors": json.loads(json.dumps(l_directors)),
        }
        #print(newDocument["providerData"])
        print("newdoc")
        startC = time.time() 
        newId = db.create_document(newDocument)
        print("Create document time:", time.time() - startC)
        print(newId)
        print('INFO: after invoking elastic search create item')
    except Exception as exc:
        print('generated an exception: %s' % (exc))
        ce_response['error_code'] = "007" #error creating item
    else:
        ce_response['newId'] = newId
    #TODO: ce_response fields?
    return json.dumps(ce_response)
