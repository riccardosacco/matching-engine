import json
import boto3
import requests
from manage_es_response import manage_response
from query_management import item_programme
from query_management.execute_query import ElasticSearch
from boto3 import client as boto3_client


lambda_client = boto3_client('lambda')
def match_item(event):
    me_response = {'providerid':'','uuid':'','flag_candidates':'', 'error_code':''}
    ##getting parameters
    query_parameters = event["queryStringParameters"]
    #provider_id
    try:
        provider_id = query_parameters["providerId"]
    except:
        provider_id = ""
    #title
    try:
        title = query_parameters["title"]
    except:
        title = ""
    #production_year
    try:
        production_year = query_parameters["production_year"]
    except:
        production_year = ""
    #director
    try:
        director = query_parameters["director"]
    except:
        director = ""
      
    #at least one not empty parameter
    #TODO: manage provider_id
    if (title or production_year or director) :
        print('query_title:'+ title+' query_director:'+director+' query_year:'+production_year)
        ##getting elastic search query 
        es_query = item_programme.generate_query({
        'query_title': title,
        'query_director': director,
        'query_year': production_year
        })
        
        try:          
            ##executing query
            db = ElasticSearch("https://search-matching-engine-uv2ckzsmrpytmltjko7x5jf4ra.eu-west-1.es.amazonaws.com/item_index/_search")
            print('info: invoking db.query')
            query_result = db.query(es_query)
            print('info: invoked db.query')           
        except:
            me_response["error_code"] = "002" #error invoking elastic search
        else:
            if query_result:
                print(query_result)
                m_response = manage_response(json.dumps(query_result))
                q_response =json.loads(m_response['body'])# response = {'uuid':'','flag_candidates':''}                
                print(json.dumps(q_response))
                print('INFO: before uuid')
                print(q_response["uuid"])
                cu_response = {'error_code':''}
                
                
                try:
                    if not q_response["error_code"]:
                        print('info: before lambda_client.invoke')
                        cu_param = {'provider_id':provider_id,'uuid':q_response["uuid"],
                        'title':title, 'production_year':production_year,
                        'director':director, 'flag_create' : q_response["flag_create"]}
                        response = lambda_client.invoke(FunctionName="createUpdateFunction",
                                      InvocationType='RequestResponse',#RequestResponse #Event
                                      Payload=json.dumps(cu_param))
                        cu_response = json.load(response['Payload'])
                        print('info: after lambda_client.invoke')
                        
                    else:
                        me_response[error_code] = q_response["error_code"]
                except:
                    me_response["error_code"] = "006" #error creating/updating item
                else:
                    print(cu_response)
                    c_body = cu_response['body']
                    d_body=json.loads(c_body)
                    print(d_body)
                    t_body=json.loads(d_body)
                    cu_error = t_body["error_code"]
                    if not cu_error:
                        print('no errore')
                        me_response["uuid"] = q_response["uuid"]
                        me_response["flag_candidates"] = q_response["flag_candidates"]
                        me_response["provider_id"] = provider_id 
                        nid = t_body["newId"]
                        me_response["new_id"] = nid["_id"]
                    else:
                        me_response["error_code"] = cu_error                  
            else:
                me_response["error_code"] = "003" #invalid query result
    #all empty parameters 
    else:
        me_response[error_code] = "001" #empty parameters
    
    return {
        'statusCode': 200,
        'body': json.dumps(me_response),
        'headers' : {'Content-type': 'application/json'}
    }
