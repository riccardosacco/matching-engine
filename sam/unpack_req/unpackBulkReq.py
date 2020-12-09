import json
from unpackBulk import unpack  # pylint: disable=import-error

def execute(event, context):
    body = json.loads(event['body'])
    items = body["items"]
    n_items = len(items)
    print(items)    
    print(n_items)
    l_req = []
    unpack_res = [] 
    for x in range(n_items):
        req = items[x]
        l_req.append(req)    
    l_res = unpack(l_req=l_req)
    for y in range(len(l_res)):
        ll_res = json.loads(l_res[y])
        for z in range(len(ll_res)):
            unpack_res.append(ll_res[z])
    print("\nFINEE")
    return {
        'statusCode': 200,
        'body': json.dumps(unpack_res),
        'headers' : {'Content-type': 'application/json'}
    }