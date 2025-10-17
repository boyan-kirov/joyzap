"""
Sample template for creating new Lambda functions
Copy this file and modify for your specific use case
"""
import os
import sys
import json

# Add parent directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from helpers.jwt import JWT, AuthorizationError
from helpers.response import Response


def lambda_handler(event, context):
    """
    Lambda handler function.
    
    Args:
        event: Lambda event object containing request data
        context: Lambda context object
        
    Returns:
        Response object with statusCode, headers, and body
    """
    try:
        # Authenticate request
        jwt_helper = JWT(os.environ["jwt_secret"])
        decoded_token = jwt_helper.auth(event)
        
        # Parse request body
        body_data = {}
        if isinstance(event.get("body"), dict):
            body_data = event["body"]
        elif isinstance(event.get("body"), str):
            body_data = json.loads(event["body"])
        
        # Your Lambda logic here
        result = {
            "message": "Success",
            "user_id": decoded_token.get("user_id"),
            "data": body_data
        }
        
        return Response.ok(result)
        
    except AuthorizationError as e:
        return Response.error(e.status_code, "", "Unauthorized")
    except json.JSONDecodeError as e:
        return Response.error(400, str(e), "Invalid JSON in request body")
    except KeyError as e:
        return Response.error(400, str(e), f"Missing required field: {str(e)}")
    except Exception as e:
        return Response.error(500, str(e), "Internal Server Error")
