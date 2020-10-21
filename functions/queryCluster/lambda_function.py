import json
import os

# Import requests library
import package.requests as requests

# TODO: call queryGenerator lambda function


def lambda_handler(event, context):
    res = requests.post(os.environ["ELASTIC_URL"],
                        {}, json.loads(event["body"]))

    return {
        "statusCode": 200,
        "body": res.text
    }
