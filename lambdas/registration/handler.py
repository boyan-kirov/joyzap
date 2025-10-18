"""
Lambda handler for registration
User registration with validation
"""
import json
import os
import sys

# Add parent directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from helpers.response import Response
from database.members import Member


def lambda_handler(event, context):
    """
    Lambda handler function for registration.
    
    POST /registration -> Create new user account
    
    Args:
        event: Lambda event object containing request data
        context: Lambda context object
        
    Returns:
        Response object with statusCode, headers, and body
    """
    if "conn_string" in os.environ:
        constr = os.environ["conn_string"]
        try:
            body = json.loads(event.get('body'))
            member = Member(constr)
            print('request body : ', body)
            if member.validate(body):
                response = member.create(body)
                member.connection.close()
                if response[0]:
                    return Response.ok()
                else:
                    if response[1] == "USER_EXISTS":
                        return Response.bad_request("USERALREADYEXISTS", "The E-Mail already exists")
                    elif response[1] == "USERNAME_EXISTS":
                        return Response.bad_request("USERNAMETAKEN", "The Username already exists")
                    else:
                        return Response.bad_request("DBERROR", "Service is not available")
            else:
                return Response.validate_error()
        except Exception as e:
            print(e)
            return Response.bad_request("DBERROR", "Service is not available")
    return Response.bad_request("INVALIDREQUEST", "Request is not valid")
