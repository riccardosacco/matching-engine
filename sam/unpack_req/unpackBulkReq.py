import json
from unpackBulk import unpack  # pylint: disable=import-error

def execute(event, context):
    body = json.loads(event['body'])
    items = body["items"]
    n_items = len(items)
    l_req = []
    unpack_res = "["
    for x in range(n_items):
        req = items[x-1]
        l_req.append(req)    
    l_res = unpack(l_req=l_req)
    for y in range(len(l_res)):
        el = json.dumps(l_res[y-1])
        sep = "" if y==len(l_res)-1 else ","
        unpack_res = unpack_res + json.loads(el) + sep
    unpack_res = unpack_res + "]"
    print(unpack_res)
    print("\nFINE")
    return {
        'statusCode': 200,
        'body': unpack_res,
        'headers' : {'Content-type': 'application/json'}
    }