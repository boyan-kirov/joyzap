"""
Lambda handler for parameters
Manages system parameters and configuration (gift categories, joy dollar payroll)
"""
import os
import sys

# Add parent directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from database.parameters import Parameters
from helpers.response import Response
from helpers.jwt import JWT, AuthorizationError


def lambda_handler(event, context):
    """
    Lambda handler function for parameters.
    
    GET /parameters/giftcats -> Get gift items by category
    DELETE /parameters/giftcats/{id} -> Delete gift item
    PATCH /parameters/giftcats/{id} -> Update gift category
    GET /parameters/joydollar -> Get joy dollar payroll
    
    Args:
        event: Lambda event object containing request data
        context: Lambda context object
        
    Returns:
        Response object with statusCode, headers, and body
    """
    print('event : ', event)
    try:
        if "conn_string" in os.environ and "jwt_secret" in os.environ:
            constr = os.environ["conn_string"]
            jwt_helper = JWT(os.environ["jwt_secret"])
            user = jwt_helper.auth(event)
            try:
                path_parameters = event.get("pathParameters") or {}
                print(path_parameters)
                param_db = Parameters(constr)
                if path_parameters.get("type") == "giftcats":
                    if event.get("httpMethod") == "GET":
                        res = param_db.get_gift_items_by_category()
                        return Response.ok(res)
                    elif event.get("httpMethod") == "DELETE":
                        path_parameters = event.get("pathParameters") or {}
                        print("path_parameters : ", path_parameters)
                        res = param_db.delete_gift_items(path_parameters)
                        return Response.ok()
                    elif event.get("httpMethod") == "PATCH":
                        path_parameters = event.get("pathParameters") or {}
                        print("path_parameters : ", path_parameters)
                        status, msg = param_db.update_gift_category(path_parameters)
                        if status:
                            return Response.ok()
                        else:
                            return Response.bad_request(400, msg)
                elif path_parameters.get("type") == "joydollar":
                    if event.get("httpMethod") == "GET":
                        res = param_db.payroll_joydollar()
                        return Response.ok(res)
            except Exception as e:
                print(e)
                return Response.bad_request("DBERROR", "Service is not available")
    except AuthorizationError as e:
        return Response.error(e.status_code,"", "Unauthorized")
