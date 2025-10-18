"""
Lambda handler for google_auth
Handles Google OAuth authentication and user registration
"""
import os
import sys
import json
import psycopg2
from google.oauth2 import id_token
from google.auth.transport import requests

# Add parent directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from helpers.jwt import JWT
from helpers.response import Response
from database.members import Member


def lambda_handler(event, context):
    """
    Lambda handler function for google_auth.
    
    POST /auth/google -> Authenticate with Google OAuth token
    
    Args:
        event: Lambda event object containing Google token
        context: Lambda context object
        
    Returns:
        Response object with JWT token or error
    """
    try:
        # Parse request body
        body_data = {}
        if isinstance(event.get("body"), dict):
            body_data = event["body"]
        elif isinstance(event.get("body"), str):
            body_data = json.loads(event["body"])
        
        token = body_data.get("token")
        if not token:
            return Response.bad_request("Missing Google token")
        
        # Verify Google token
        try:
            idinfo = id_token.verify_oauth2_token(
                token, 
                requests.Request(), 
                os.environ.get("GOOGLE_CLIENT_ID")
            )
            
            # Extract user info from Google
            email = idinfo['email']
            name = idinfo.get('name', '')
            google_id = idinfo['sub']
            picture = idinfo.get('picture', '')
            
        except ValueError as e:
            return Response.error(401, str(e), "Invalid Google token")
        
        # Connect to database
        conn = psycopg2.connect(
            host=os.environ["db_host"],
            port=os.environ["db_port"],
            dbname=os.environ["db_name"],
            user=os.environ["db_user"],
            password=os.environ["db_password"]
        )
        
        # Check if user exists, create if not
        user = Member.find_by_email(email, conn)
        
        if not user:
            # Create new user from Google info
            user = Member.create_for_google(
                email=email,
                name=name,
                google_id=google_id,
                picture=picture,
                conn=conn
            )
        
        conn.close()
        
        # Generate JWT token
        jwt_helper = JWT(os.environ["jwt_secret"])
        jwt_token = jwt_helper.encode({
            "user_id": user['id'],
            "email": user['email']
        })
        
        result = {
            "token": jwt_token,
            "user": {
                "id": user['id'],
                "email": user['email'],
                "name": user.get('name', ''),
                "picture": user.get('picture', '')
            }
        }
        
        return Response.ok(result)
        
    except json.JSONDecodeError as e:
        return Response.error(400, str(e), "Invalid JSON in request body")
    except KeyError as e:
        return Response.error(400, str(e), f"Missing required field: {str(e)}")
    except Exception as e:
        return Response.error(500, str(e), "Internal Server Error")
