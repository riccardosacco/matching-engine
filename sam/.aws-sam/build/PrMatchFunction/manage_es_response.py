import json
import os
from query_management import generate_uuid

def manage_response(es_result):
    matching_threshold = os.environ['ME_MATCHING_THRESHOLD']  
    candidates_threshold = os.environ['ME_CANDIDATES_THRESHOLD']   
    #matching_threshold = "90"  
    #candidates_threshold = "70"
    matching_threshold_int = int(matching_threshold)
    candidates_threshold_int = int(candidates_threshold)
    error_code = ""
    response = {'uuid':'','flag_candidates':'','flag_create':'','error_code':''}
    try:
        print('matching_threshold '+matching_threshold)
        print('candidates_threshold '+candidates_threshold)
        print('info: before es_response')
        es_response = json.loads(es_result)
        print('info: after es_response')
        max_score = float(es_response["hits"]["max_score"])
        n_items = len(es_response["hits"]["hits"])
        print(max_score)
        print(n_items)
    except:
         response["error_code"] = "004" #error loading es response
    else:
        if max_score >= matching_threshold_int and n_items==1:
            print('info: 1')
            #found match single UUID 
            response["uuid"] = es_response["hits"]["hits"][0]['_source']['providerData']['uuid']
            response["flag_candidates"] = 'N'
            response["flag_create"] = 'N'
        elif max_score >= matching_threshold_int and n_items>1:
            print('info: 2')
            #new UUID + candidates flag
            response["uuid"] = str(generate_uuid.v4())
            response["flag_candidates"] = 'Y'
            response["flag_create"] = 'Y'
        elif max_score >= candidates_threshold_int and n_items>=1:
            print('info: 3')
            #new UUID + candidates flag
            response["uuid"] = str(generate_uuid.v4()) 
            response["flag_candidates"] = 'Y'
            response["flag_create"] = 'Y'
        elif max_score < candidates_threshold_int:
            print('info: 4')
            #new UUID
            response["uuid"] = str(generate_uuid.v4())
            response["flag_candidates"] = 'N'
            response["flag_create"] = 'Y'
        else:
            response["error_code"] = "005" #error in evaluating response
    return {
        'statusCode': 200,
        'body': json.dumps(response),
        'headers' : {'Content-type': 'application/json'}
    }
