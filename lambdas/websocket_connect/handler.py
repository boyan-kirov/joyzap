"""
Lambda handler for websocket_connect
Handles WebSocket connection establishment
"""
import os
import sys
import psycopg2

# Add parent directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from database.members import Member


def lambda_handler(event, context):
    """
    Lambda handler function for websocket_connect.
    
    Stores WebSocket connection ID when client connects.
    
    Args:
        event: Lambda event object containing requestContext with connectionId
        context: Lambda context object
        
    Returns:
        Response object with statusCode
    """
    try:
        # Get connection ID from WebSocket event
        connection_id = event['requestContext']['connectionId']
        
        # Get user_id from query string parameters
        user_id = event.get('queryStringParameters', {}).get('user_id')
        
        if not user_id:
            return {'statusCode': 400, 'body': 'Missing user_id'}
        
        # Connect to database
        conn = psycopg2.connect(
            host=os.environ["db_host"],
            port=os.environ["db_port"],
            dbname=os.environ["db_name"],
            user=os.environ["db_user"],
            password=os.environ["db_password"]
        )
        
        # Update user's socket_id
        Member.set_socket_id(user_id, connection_id, conn)
        
        conn.close()
        
        return {'statusCode': 200, 'body': 'Connected'}
        
    except KeyError as e:
        print(f"Missing required field: {str(e)}")
        return {'statusCode': 400, 'body': f'Missing required field: {str(e)}'}
    except Exception as e:
        print(f"Error connecting WebSocket: {str(e)}")
        return {'statusCode': 500, 'body': 'Internal Server Error'}
