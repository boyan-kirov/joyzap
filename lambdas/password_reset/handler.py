"""
Lambda handler for password_reset
Password reset operations (similar structure to login)
"""
import json
import os
import sys

# Add parent directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from helpers.response import Response
from database.logins import Login


def lambda_handler(event, context):
    """
    Lambda handler function for password_reset.
    
    POST /password-reset/{id}/{reset_token} -> Reset password with token
    PUT /password-reset -> Generate password reset token
    
    Args:
        event: Lambda event object containing request data
        context: Lambda context object
        
    Returns:
        Response object with statusCode, headers, and body
    """
    if "conn_string" in os.environ:
        constr = os.environ["conn_string"]
        try:
            if event.get('requestContext').get('http').get('method') == 'POST':
                # Reset password with token
                login = Login(constr)
                path_parameters = event.get('pathParameters') or {}
                if path_parameters.get('id', None) is not None and path_parameters.get('reset_token', None) is not None:
                    body = json.loads(event.get('body'))
                    path_parameters['password'] = body.get('password')
                    print('path_parameters', path_parameters)
                    response = login.reset_password(path_parameters)
                    print('response', response)
                    login.connection.close()
                    if response:
                        return Response.ok()
                    else:
                        return Response.bad_request("INVALIDCREDENTIALS", "Invalid credential")
                else:
                    return Response.bad_request("INVALIDREQUEST", "Missing id or reset_token")
            elif event.get('requestContext').get('http').get('method') == 'PUT':
                # Generate reset token
                body = json.loads(event.get('body'))
                print('body', body)
                login = Login(constr)
                res = login.reset_token_generate(body.get('email'))
                print('res', res)
                login.connection.close()
                if res[0]:
                    return Response.ok()
                else:
                    return Response.bad_request("INVALIDCREDENTIALS", "E-Mail is incorrect")
        except Exception as e:
            print(e)
            return Response.bad_request("DBERROR", "Service is not available")
    return Response.bad_request("INVALIDREQUEST", "Request is not valid")
