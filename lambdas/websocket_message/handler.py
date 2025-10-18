"""
Lambda handler for websocket_message
Handles WebSocket messages including socket ID saving and notifications
"""
import json
import datetime
import os
import sys
import boto3

# Add parent directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from database.joyzaps import Joyzap
from database.members import Member
from helpers.response import Response
from helpers.jwt import JWT, AuthorizationError


def default(o):
    if isinstance(o, (datetime.date, datetime.datetime)):
        return o.isoformat()


client = boto3.client('apigatewaymanagementapi', endpoint_url="https://w3b171a34j.execute-api.eu-central-1.amazonaws.com/Prod/")


def lambda_handler(event, context):
    """
    Lambda handler function for websocket_message.
    
    POST /message -> Handle WebSocket messages
    
    Args:
        event: Lambda event object containing request data
        context: Lambda context object
        
    Returns:
        Response object with statusCode
    """
    print("event ************************", event)
    try:
        print(type(event.get("body")))
        body = event.get("body") if isinstance(event.get("body"), dict) else json.loads(event.get("body"))
        if body.get("path") == '/save-socket-id':
            constr = os.environ["conn_string"]
            jwt_helper = JWT(os.environ["jwt_secret"])
            event["headers"] = {
                "Authorization" : 'Bearer ' + body.get("token")
            }
            print("event", event)
            user = jwt_helper.auth(event)
            member_search_body_json = {}
            member_search_body_json["user_id"] = user["id"]
            member_search_body_json["socket_id"] = event["requestContext"].get("connectionId")
            print("member_search_body_json", member_search_body_json)
            member_db = Member(constr)
            res = member_db.search(member_search_body_json)
            member_db.connection.close()
            return {
                "statusCode": 200
            }
        elif body.get("path") == '/notification-send':
            print("body.get('socket_id')", body.get('socket_id'))
            if body.get('socket_id') is not None:
                client.post_to_connection(ConnectionId=body.get('socket_id'), Data=json.dumps('zapped').encode('utf-8'))
            return {
                "statusCode": 200
            }
    except Exception as e:
        print(e)
        return Response.bad_request("DBERROR", "Service is not available")
    except AuthorizationError as e:
        return Response.error(e.status_code,"", "Unauthorized")
