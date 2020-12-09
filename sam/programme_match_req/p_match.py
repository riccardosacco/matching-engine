import json
import time
import boto3
import requests
import os
from manage_es_response import manage_response  # pylint: disable=import-error
from query_management import item_programme  # pylint: disable=import-error
from query_management.execute_query import ElasticSearch  # pylint: disable=import-error
from query_management import execute_query # pylint: disable=import-error
from boto3 import client as boto3_client


lambda_client = boto3_client('lambda')
#ELASTIC_URL = "https://search-matching-engine-uv2ckzsmrpytmltjko7x5jf4ra.eu-west-1.es.amazonaws.com/programme_index/_msearch"
ELASTIC_URL = "https://search-matching-engine-uv2ckzsmrpytmltjko7x5jf4ra.eu-west-1.es.amazonaws.com/massive_test_index/_msearch"#
def match_item(l_params):
    print("entrato match_item")
    l_me_response = []   
    l_query_dict = []
    l_request_id = []  
    for y in range(len(l_params)): 
        _params = l_params[y]
        #me_response = {'providerid':'','uuid':'','flag_candidates':'', 'error_code':''}    
        me_response =   {
            #'new_id':'',
            'requestId': '',
            'uuid': '',
            'newUUIDFlag': False,
            'aliasCandidatesFlag': False,
            'appliedAction': {
              'type': '',
              'uuid': ''
            } 
        }
        ##getting parameters
        #title
        title = []
        try:       
            print(_params["title"])
            if (len(_params["title"].strip()) > 0):
                title.append(_params["title"].strip())
        except:
            pass
        #request_context
        try:
            request_context = _params["requestContext"]
        except:
            request_context = ""
        #provider_id
        try:
            provider_id = str(_params["providerData"]["providerId"]).lower()

        except:
            provider_id = ""
        #provider_name
        try:
            provider_name = _params["providerData"]["providerName"]
        except:
            provider_name = ""
        #production_year
        try:
            production_year = str(_params["productionYear"])
        except:
            production_year = ""
        #director
        try:
            directorP = _params["directors"]
            directorS = directorP.split(',')
            director = list(map(str.strip,directorS))
        except:
            director = ""
    
        #enrichedUUID
        try:
            enrichedUUID = _params["enrichedUUID"]
        except:
            enrichedUUID = ""
        #alternativeTitles
        try:
            alternativeTitles = _params["alternativeTitles"]
        except:
            alternativeTitles = ""
        try:
            n_aTitles = len(alternativeTitles)
            for z in range(n_aTitles):
                elemT = alternativeTitles[z-1]
                title.append(elemT['value'])
                #title[t_len+z]=elemT["value"]
        except:
            pass
   
        # min_threshold
        min_threshold = 70
        try:
            min_threshold = int(os.environ['ME_CANDIDATES_THRESHOLD'])
        except:
            pass
        
        #at least one not empty parameter
        #TODO: manage provider_id
        if (len(title)) :
            ##getting elastic search query  
            query_dict = {'query_titles': title}
            if (provider_id) :
                query_dict['query_providerID'] = provider_id
            if (director) :
                query_dict['query_directors'] = director
            if (production_year) :
                query_dict['query_year'] = production_year
            l_query_dict.append(query_dict)  
            l_request_id.append(_params["requestId"])
        #all empty parameters 
        else:
            me_response["error_code"] = "001" #empty parameters        
    print("l_query_dict")    
    print(l_query_dict)

    startGq = time.time() 
    es_query = item_programme.generate_query(matchitems=l_query_dict,min_threshold=min_threshold)    
    print("Generate query time:", time.time() - startGq)
    print(es_query)
    try:          
        ##executing query
        db = execute_query.ElasticSearch(ELASTIC_URL)
        print('info: invoking db.query')
        startQ = time.time()
        query_result = db.query(es_query)
        print("Query time:", time.time() - startQ)
        print('info: invoked db.query')           
    except:
        me_response["error_code"] = "002" #error invoking elastic search
    else:
        if query_result:
            print(query_result)
            m_response = manage_response(es_result=json.dumps(query_result))
            l_q_response =json.loads(m_response['body'])# response = {'uuid':'','flag_candidates':''}                
            print(json.dumps(l_q_response))
            l_me_response = l_q_response
            # TODO: scommentare invocazione create
            for k in range(len(l_q_response)):
                try:
                    q_response = l_q_response[k]
                    l_me_response[k]["requestId"] = l_request_id[k]
                    print("ASSOCIATI: "+q_response["title"]+" reqid:"+l_request_id[k])
                    #me_response["uuid"] = q_response["uuid"]
                    l_me_response[k]["newUUIDFlag"] = True if q_response["flag_create"]=='Y' else False
                    l_me_response[k]["aliasCandidatesFlag"] = True if q_response["flag_candidates"]=='Y' else False     
                    #print('INFO: before uuid')
                    #print(l_me_response[k]["uuid"])
                    #cu_response = {'error_code':''}
                    cu_error=''
                    fu_error=''
                    """ if not q_response["error_code"]:
                        print('info: before create lambda_client.invoke')
                        cu_param = {'provider_id':provider_id,'provider_name':provider_name,'uuid':q_response["uuid"],
                        'title':title, 'production_year':production_year,
                        'director':director, 'flag_create' : q_response["flag_create"], "request_context":request_context}
                        response = lambda_client.invoke(FunctionName="createUpdateFunction",
                                    InvocationType='Event',#RequestResponse #Event
                                    Payload=json.dumps(cu_param))

                        #cu_response = json.load(response['Payload'])
                        print('info: after lambda_client.invoke')
                        print(response)
                        try:
                            cu_error = '' if json.dumps(response['StatusCode'])=='202' else '006'
                        except:
                            pass
                        try:
                            fu_error = response['FunctionError'] 
                        except:
                            pass 
                        cu_error = fu_error if fu_error else cu_error 
                    else:
                        me_response["error_code"] = q_response["error_code"] """
                except:
                    me_response["error_code"] = "006" #error creating/updating item
                         
        else:
            me_response["error_code"] = "003" #invalid query result
            l_me_response.append(me_response)  
    return {
        'statusCode': 200,
        'body': json.dumps(l_me_response),
        'headers' : {'Content-type': 'application/json'}
  }   
