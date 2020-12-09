import json
import os
from query_management import generate_uuid  # pylint: disable=import-error

def manage_response(es_result):
    matching_threshold = "90"  
    candidates_threshold = "70" 
    provider_score  = 1000
    try: 
        matching_threshold = os.environ['ME_MATCHING_THRESHOLD']  
        candidates_threshold = os.environ['ME_CANDIDATES_THRESHOLD']  
    except :
        pass   
    matching_threshold_int = int(matching_threshold)
    candidates_threshold_int = int(candidates_threshold)
    response_list = []
    try:
        print('matching_threshold '+matching_threshold)
        print('candidates_threshold '+candidates_threshold)
        print('info: before es_response')
        es_response = json.loads(es_result)
        print('info: after es_response')
        responses = es_response["responses"]
        n_response = len(responses)
        for z in range(n_response):
            print(z)
            response = {'uuid':'','flag_candidates':'','flag_create':'','error_code':'','title':''}
            curr_res = responses[z]
            provider_max_score = 0
            metadata_max_score = 0
            tot_score = 0
            metadata_items = 0
            try:
                tot_score = float(curr_res["hits"]["max_score"])
            except:
                pass
            try:
                metadata_items = curr_res["hits"]["total"] ["value"]
            except:
                pass
            # no match
            if (tot_score <= 0) :
                print ("NO MATCH")
            # match only metadata
            elif (tot_score < provider_score) :
                metadata_max_score = tot_score
            # match only providerId
            elif (tot_score==provider_score):
                provider_max_score = tot_score
            # match metadata and providerId
            elif (tot_score>provider_score):
                provider_max_score = provider_score
                metadata_max_score = tot_score-provider_score


            if (provider_max_score==0 and metadata_max_score==0):
                print('scenario: 5')
                #new UUID
                response["uuid"] = str(generate_uuid.v4())
                response["flag_candidates"] = 'N'
                response["flag_create"] = 'Y'
            elif metadata_max_score >= matching_threshold_int and metadata_items==1:
                print('scenario: 1')
                #found match single UUID 
                hits_list = curr_res["hits"]["hits"]
                hits_elem = hits_list[0]
                response["uuid"] = hits_elem['_source']['masterUUID']
                response["flag_candidates"] = 'N'
                response["flag_create"] = 'N'
            elif metadata_max_score >= matching_threshold_int and metadata_items>1:
                print('scenario: 2')
                #new UUID + candidates flag
                response["uuid"] = str(generate_uuid.v4())
                response["flag_candidates"] = 'Y'
                response["flag_create"] = 'Y'
            elif metadata_max_score >= candidates_threshold_int and metadata_items>=1:
                print('scenario: 3')
                #new UUID + candidates flag
                response["uuid"] = str(generate_uuid.v4()) 
                response["flag_candidates"] = 'Y'
                response["flag_create"] = 'Y'
            elif metadata_max_score < candidates_threshold_int:
                print('scenario: 4')
                #new UUID
                response["uuid"] = str(generate_uuid.v4())
                response["flag_candidates"] = 'N'
                response["flag_create"] = 'Y'
            else:
                response["error_code"] = "005" #error in evaluating response
            try:      
                _hits_list = curr_res["hits"]["hits"]
                _hits_elem = _hits_list[0] 
                pr_list = _hits_elem['_source']['providerData'] 
                p = pr_list[0]
                _l_title = p["titles"]
                tit = _l_title[0]
                response["title"] = tit["title"]
            except :
                response["title"] = "no match"
            response_list.append(response)
            
    except:
         response = {'uuid':'','flag_candidates':'','flag_create':'','error_code':'004'} #error loading es response
         response_list.append(response) 
    return {
        'statusCode': 200,
        'body': json.dumps(response_list),
        'headers' : {'Content-type': 'application/json'}
    }
