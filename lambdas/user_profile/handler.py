"""
Lambda handler for user_profile
User profile operations with event data
"""
import json
import os
import sys

# Add parent directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from helpers.response import Response
from helpers.jwt import JWT
from database.members import Member


def lambda_handler(event, context):
    """
    Lambda handler function for user_profile.
    
    GET /user-profile/{user_id} -> Get user profile
    GET /user-profile/{user_id}/{event_id} -> Get user profile with event data
    PUT /user-profile -> Update user profile
    
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
            member = Member(constr)
            
            if event.get('requestContext').get('http').get('method') == 'GET':
                path_parameters = event.get('pathParameters') or {}
                user_id = path_parameters.get('user_id')
                event_id = path_parameters.get('event_id')
                
                if not user_id:
                    return Response.bad_request("INVALIDREQUEST", "user_id is required")
                
                if event_id:
                    # Get user profile with event data
                    response = member.get_user_profile_with_event(user_id, event_id)
                else:
                    # Get basic user profile
                    response = member.get_user(user_id)
                
                member.connection.close()
                
                if response:
                    return Response.ok({"data": response})
                else:
                    return Response.bad_request("NOTFOUND", "User not found")
                    
            elif event.get('requestContext').get('http').get('method') == 'PUT':
                # Update user profile
                body = json.loads(event.get('body'))
                user_id = decoded_token.get("user_id")
                
                response = member.update(user_id, body)
                member.connection.close()
                
                if response:
                    return Response.ok()
                else:
                    return Response.bad_request("DBERROR", "Failed to update profile")
                    
        except Exception as e:
            print(e)
            return Response.bad_request("DBERROR", "Service is not available")
    
    return Response.bad_request("INVALIDREQUEST", "Request is not valid")
