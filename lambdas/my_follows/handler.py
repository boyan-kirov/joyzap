"""
Lambda handler for my_follows
Get list of users that this user follows
"""
import json
import os
import sys

# Add parent directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from helpers.response import Response
from helpers.jwt import JWT
from database.relation import Relation


def lambda_handler(event, context):
    """
    Lambda handler function for my_follows.
    
    GET /my-follows?keyword=xxx -> Get users this user follows with optional keyword filter
    
    Args:
        event: Lambda event object containing request data
        context: Lambda context object
        
    Returns:
        Response object with statusCode, headers, and body
    """
    if "conn_string" in os.environ and "jwt_secret" in os.environ:
        constr = os.environ["conn_string"]
        jwt_helper = JWT(os.environ["jwt_secret"])
        decoded_token = jwt_helper.auth(event)
        try:
            query_string_parameters = event.get('queryStringParameters') or {}
            keyword = query_string_parameters.get('keyword')
            relation = Relation(constr)
            response = relation.my_follows(decoded_token.get("user_id"), keyword)
            relation.connection.close()
            if response:
                return Response.ok({"data": response})
        except Exception as e:
            print(e)
            return Response.bad_request("DBERROR", "Service is not available")
    return Response.bad_request("INVALIDREQUEST", "Request is not valid")
