import json
from p_match import match_item  # pylint: disable=import-error


def p_match_req(event, context):
    print("entrato p_match_req")
    print(event)
    return match_item(l_params=event)

def p_match_req_get(event, context):
    print("entrato p_match_req_get")
    return match_item(l_params=event["queryStringParameters"])
