"""
Lambda handler for login
Multi-method authentication handler (POST/GET/PUT/PATCH)
"""
import json
import os
import sys

# Add parent directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from helpers.response import Response
from database.logins import Login
from helpers.jwt import JWT


def lambda_handler(event, context):
    """
    Lambda handler function for login.
    
    POST /login -> User login with email/password
    POST /login/{id}/{reset_token} -> Reset password with token
    GET /login?activation_token=xxx -> Activate account
    PUT /login -> Generate password reset token
    PATCH /login -> Generate takeover token
    PATCH /login/takeover -> Reset password with takeover token
    
    Args:
        event: Lambda event object containing request data
        context: Lambda context object
        
    Returns:
        Response object with statusCode, headers, and body
    """
    if "conn_string" in os.environ and "jwt_secret" in os.environ:
        constr = os.environ["conn_string"]
        print('event', event)
        try:
            if event.get('requestContext').get('http').get('method') == 'POST':
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
                    jwt_helper = JWT(os.environ["jwt_secret"])
                    login_body = json.loads(event.get('body'))
                    if login.validate(login_body):
                        login_response = login.login(login_body)
                        login.connection.close()
                        print('login_response[1]', login_response[1])
                        if login_response[0]:
                            if login_response[1].get("is_activate") == False:
                                return Response.bad_request("INVALIDAUTHENTICATION", "Check your e-mail and click on the validation link to complete registration.")
                            else:
                                jwt_token = jwt_helper.encode(login_response[1])
                                return Response.ok({"user": login_response[1], "token": jwt_token})
                        else:
                            return Response.bad_request("INVALIDCREDENTIALS", "E-Mail or Password is incorrect")
            elif event.get('requestContext').get('http').get('method') == 'GET':
                jwt_helper = JWT(os.environ["jwt_secret"])
                query_string_parameters = event.get('queryStringParameters') or {}
                print('query_string_parameters', query_string_parameters)
                if query_string_parameters.get("activation_token", None) is not None:
                    activation = Login(constr)
                    res = activation.activate(query_string_parameters.get("activation_token"))
                    print('res', res)
                    activation.connection.close()
                    if res[0]:
                        jwt_token = jwt_helper.encode(res[1])
                        return Response.ok({"user": res[1], "token": jwt_token})
                    else:
                        return Response.bad_request("INVALIDCREDENTIALS", "Service is not available")
                else:
                    return Response.bad_request("DBERROR", "Invalid input")
            elif event.get('requestContext').get('http').get('method') == 'PUT':
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
            elif event.get('requestContext').get('http').get('method') == 'PATCH':
                if event.get('requestContext').get('http').get('path') == "/login":
                    body = json.loads(event.get('body'))
                    print('body', body)
                    login = Login(constr)
                    res = login.takeover_token_generate(body.get('contact'))
                    print('res', res)
                    login.connection.close()
                    print('res : ', res)
                    if res[0]:
                        return Response.ok()
                    else:
                        return Response.bad_request("INVALIDCREDENTIALS", "Contact is not found.")
                elif event.get('requestContext').get('http').get('path') == "/login/takeover":
                    body = json.loads(event.get('body'))
                    print('body', body)
                    login = Login(constr)
                    res = login.takeover_reset_password(body)
                    print('res', res)
                    login.connection.close()
                    if res:
                        return Response.ok()
                    else:
                        return Response.bad_request("INVALIDCREDENTIALS", "Invalid credential")

        except Exception as e:
            print(e)
            return Response.bad_request("DBERROR", "Service is not available")
    return Response.bad_request("INVALIDREQUEST", "Please input e-mail and password")
