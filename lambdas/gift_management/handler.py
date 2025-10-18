"""
Lambda handler for gift_management
Handles CRUD operations for gifts including categories, items, and updates
"""
import os
import sys
import json

# Add parent directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from helpers.jwt import JWT, AuthorizationError
from helpers.response import Response
from database.gifts import Gift
from dto.gift_dto import GiftBody


def lambda_handler(event, context):
    """
    Lambda handler function for gift management.
    Handles GET (categories), POST (create), PATCH (update), and PUT (bulk update).
    
    Args:
        event: Lambda event object containing request data
        context: Lambda context object
        
    Returns:
        Response object with statusCode, headers, and body
    """
    constr = os.environ["conn_string"]
    
    try:
        jwt_helper = JWT(os.environ["jwt_secret"])
        user = jwt_helper.auth(event)
        
        try:
            # GET /gift/categories - Get gift categories
            if (
                event.get("path") == "/gift/categories"
                and event.get("httpMethod") == "GET"
            ):
                gift_db = Gift(constr)
                res = gift_db.get_gift_categories()
                gift_db.connection.close()
                return Response.ok(json.loads(json.dumps(res, allow_nan=True)))
            
            # POST - Create gift item
            elif event.get("httpMethod") == "POST":
                gift_db = Gift(constr)
                print("event.get : ", event.get("body"))
                gift_body = GiftBody(**json.loads(event.get("body")))
                res = gift_db.create_gift_item(gift_body)
                gift_db.connection.close()
                return Response.ok(json.loads(json.dumps(res, allow_nan=True)))
            
            # PATCH - Update single gift item
            elif event.get("httpMethod") == "PATCH":
                gift_db = Gift(constr)
                path_parameters = event.get("pathParameters") or {}
                body = json.loads(event.get("body"))
                body["id"] = path_parameters.get("id")
                res = gift_db.update_gift_item(body)
                gift_db.connection.close()
                return Response.ok(json.loads(json.dumps(res, allow_nan=True)))
            
            # PUT - Multiple update (bulk operation)
            elif event.get("httpMethod") == "PUT":
                gift_db = Gift(constr)
                print("event.get : ", event.get("body"))
                body = json.loads(event.get("body"))
                res = gift_db.multiple_update(body.get("ids", []), body.get("type", None))
                gift_db.connection.close()
                if res:
                    return Response.ok()
                else:
                    return Response.bad_request("DATA", "Id or type not found.")
            
            else:
                return Response.error(405, "Method not allowed", "Method not supported")
                
        except Exception as e:
            print(e)
            return Response.bad_request("DBERROR", "Service is not available")
            
    except AuthorizationError as e:
        return Response.error(e.status_code, "", "Unauthorized")
