"""
Lambda handler for my_followers
Get list of followers (pending friend requests sent to me)
"""
import os
import sys

# Add parent directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from helpers.response import Response
from database.relation import Relation
from helpers.jwt import JWT, AuthorizationError


def lambda_handler(event, context):
    """
    Lambda handler function for my_followers.
    
    GET /followers -> Get list of followers with optional keyword search
    
    Args:
        event: Lambda event object containing request data
        context: Lambda context object
        
    Returns:
        Response object with statusCode, headers, and body
    """
    try:
        constr = os.environ["conn_string"]
        jwt_helper = JWT(os.environ["jwt_secret"])
        user = jwt_helper.auth(event)
        try:
            if event.get('httpMethod') == 'GET':
                query_strings = event.get('queryStringParameters') or {}
                print(query_strings)
                event_db = Relation(constr)
                res = event_db.my_followers(user["id"], query_strings.get("keyword",""))
                event_db.connection.close()
                return Response.ok(res)

        except Exception as e:
            print(e)
            return Response.bad_request("DBERROR", "Service is not available")
    except AuthorizationError as e:
        return Response.error(e.status_code,"", "Unauthorized")
