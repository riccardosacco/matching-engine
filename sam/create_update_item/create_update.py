import json
from create_item import create_elem  # pylint: disable=import-error
from update_item import update_elem  # pylint: disable=import-error

def create_update_item(event, context):
    print('INFO: start create update')
    print(event)
    cu_response = {'uuid':'','error_code':''}
    if event["flag_create"] == 'Y':
        print('INFO: start create')
        cu_response = create_elem(param=event)
    elif event["flag_create"] == 'N':
        print('INFO: start update')
        cu_response = update_elem(param=event)
    return {
        'statusCode': 200,
        'body': json.dumps(cu_response),
        'headers' : {'Content-type': 'application/json'}
    }