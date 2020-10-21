import json
import requests

def lambda_handler(event, context):
    # TODO implement
    
    result = requests.get("https://jsonplaceholder.typicode.com/todos")
    
    return {
        'statusCode': 200,
        'body': json.dumps(result)
    }
