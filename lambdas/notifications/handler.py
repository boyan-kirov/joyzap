"""
Lambda handler for notifications
Handles GET (retrieve) and PUT (update) operations for user notifications
"""
import os
import sys
import json
import datetime

# Add parent directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from helpers.jwt import JWT, AuthorizationError
from helpers.response import Response
from database.notification import Notification


def default(o):
    """JSON serializer for datetime objects"""
    if isinstance(o, (datetime.date, datetime.datetime)):
        return o.isoformat()


def lambda_handler(event, context):
    """
    Lambda handler function for notifications.
    Supports GET to retrieve notifications and PUT to update them.
    
    Args:
        event: Lambda event object containing request data
        context: Lambda context object
        
    Returns:
        Response object with statusCode, headers, and body
    """
    print("event ************************", event)
    
    try:
        # Get database connection string
        constr = os.environ["conn_string"]
        
        # Authenticate request and get user info
        jwt_helper = JWT(os.environ["jwt_secret"])
        user = jwt_helper.auth(event)
        
        try:
            # Handle GET request - retrieve user notifications
            if event.get('httpMethod') == 'GET':
                body_json = {}
                body_json["user_id"] = user["id"]
                
                notification_db = Notification(constr)
                res = notification_db.get_user(body_json)
                notification_db.connection.close()
                
                return Response.ok(json.loads(json.dumps(res, allow_nan=True, default=default)))
            
            # Handle PUT request - update notification
            elif event.get('httpMethod') == 'PUT':
                notification_update_body = json.loads(event.get('body'))
                notification_update_body["user_id"] = user["id"]
                
                notification_db = Notification(constr)
                res = notification_db.update(notification_update_body)
                notification_db.connection.close()
                
                return Response.ok(json.loads(json.dumps(res, allow_nan=True, default=default)))
            
            else:
                return Response.error(405, "Method not allowed", "Only GET and PUT methods are supported")
                
        except Exception as e:
            print(e)
            return Response.bad_request("DBERROR", "Service is not available")
            
    except AuthorizationError as e:
        return Response.error(e.status_code, "", "Unauthorized")
