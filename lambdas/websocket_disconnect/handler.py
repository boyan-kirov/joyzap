"""
Lambda handler for WebSocket disconnect
Clears socket_id from user when they disconnect
"""
import os
import sys
import json
import datetime
import psycopg2
import psycopg2.extras

# Add parent directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from helpers.jwt import JWT, AuthorizationError
from helpers.response import Response


def default(o):
    """JSON serializer for datetime objects"""
    if isinstance(o, (datetime.date, datetime.datetime)):
        return o.isoformat()


def lambda_handler(event, context):
    """
    Lambda handler for WebSocket disconnection.
    Clears the socket_id from the users table when a WebSocket connection is closed.
    
    Args:
        event: Lambda event object containing WebSocket connection info
        context: Lambda context object
        
    Returns:
        Response object with statusCode and body
    """
    print("event ************************", event)
    
    try:
        # Get database connection string
        constr = os.environ["conn_string"]
        
        # Get socket ID from WebSocket connection context
        socket_id = event["requestContext"].get("connectionId")
        
        # Connect to PostgreSQL database
        connection = psycopg2.connect(constr)
        cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        
        # Clear socket_id for disconnected user
        query = f"UPDATE users SET socket_id = null WHERE socket_id = '{socket_id}'"
        cursor.execute(query)
        connection.commit()
        connection.close()
        
        return {
            'statusCode': 200,
            'body': json.dumps('WebSocket disconnected successfully')
        }
        
    except Exception as e:
        print(e)
        return Response.bad_request("DBERROR", "Service is not available")
    except AuthorizationError as e:
        return Response.error(e.status_code, "", "Unauthorized")
