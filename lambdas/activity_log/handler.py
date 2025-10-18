"""
Lambda handler for activity_log
User activity logging and retrieval
"""
import json
import os
import sys

# Add parent directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from helpers.response import Response
from helpers.jwt import JWT
from database.activation_log import Activity


def lambda_handler(event, context):
    """
    Lambda handler function for activity_log.
    
    GET /activity-log -> Retrieve user's activity log
    
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
            activity = Activity(constr)
            response = activity.get_activity_log(decoded_token.get("user_id"))
            activity.connection.close()
            if response:
                return Response.ok({"data": response})
        except Exception as e:
            print(e)
            return Response.bad_request("DBERROR", "Service is not available")
    return Response.bad_request("INVALIDREQUEST", "Request is not valid")
