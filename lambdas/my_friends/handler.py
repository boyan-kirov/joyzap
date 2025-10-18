"""
Lambda handler for my_friends
Get list of user's friends with optional keyword search
"""
import os
import sys

# Add parent directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from helpers.jwt import JWT, AuthorizationError
from helpers.response import Response
from database.relation import Relation


def lambda_handler(event, context):
    """
    Lambda handler function for retrieving user's friends list.
    Supports keyword search via query parameters.
    
    Args:
        event: Lambda event object containing request data
        context: Lambda context object
        
    Returns:
        Response object with statusCode, headers, and body
    """
    try:
        # Get database connection string
        constr = os.environ["conn_string"]
        
        # Authenticate request and get user info
        jwt_helper = JWT(os.environ["jwt_secret"])
        user = jwt_helper.auth(event)
        
        try:
            # Handle GET request
            if event.get('httpMethod') == 'GET':
                # Get query string parameters
                query_strings = event.get('queryStringParameters') or {}
                print(query_strings)
                
                # Get friends list from database
                relation_db = Relation(constr)
                res = relation_db.my_friends(user["id"], query_strings.get("keyword", ""))
                relation_db.connection.close()
                
                return Response.ok(res)
            else:
                return Response.error(405, "Method not allowed", "Only GET method is supported")
                
        except Exception as e:
            print(e)
            return Response.bad_request("DBERROR", "Service is not available")
            
    except AuthorizationError as e:
        return Response.error(e.status_code, "", "Unauthorized")
