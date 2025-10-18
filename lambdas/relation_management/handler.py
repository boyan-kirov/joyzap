"""
Lambda handler for relation_management
Handles friend request operations (create, accept, reject, delete)
"""
import os
import sys
import json
import psycopg2

# Add parent directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from helpers.jwt import JWT, AuthorizationError
from helpers.response import Response
from database.relation import Relation
from dto.relation_dto import RelationBody


def lambda_handler(event, context):
    """
    Lambda handler function for relation_management.
    
    POST /relation -> Send friend request
    PUT /relation -> Accept friend request
    PATCH /relation -> Reject friend request
    DELETE /relation -> Delete friendship
    
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
        user_id = decoded_token.get("user_id")
        
        # Parse request body
        body_data = {}
        if isinstance(event.get("body"), dict):
            body_data = event["body"]
        elif isinstance(event.get("body"), str):
            body_data = json.loads(event["body"])
        
        # Validate DTO
        relation_dto = RelationBody.from_dict(body_data)
        
        # Connect to database
        conn = psycopg2.connect(
            host=os.environ["db_host"],
            port=os.environ["db_port"],
            dbname=os.environ["db_name"],
            user=os.environ["db_user"],
            password=os.environ["db_password"]
        )
        
        # Route based on HTTP method
        http_method = event.get("httpMethod", event.get("requestContext", {}).get("http", {}).get("method", ""))
        
        if http_method == "POST":
            # Send friend request
            Relation.create(user_id, relation_dto.friend_id, conn)
            conn.close()
            return Response.created({"message": "Friend request sent"})
            
        elif http_method == "PUT":
            # Accept friend request
            Relation.accept_relation(user_id, relation_dto.friend_id, conn)
            conn.close()
            return Response.ok({"message": "Friend request accepted"})
            
        elif http_method == "PATCH":
            # Reject friend request
            Relation.reject_friend_request(user_id, relation_dto.friend_id, conn)
            conn.close()
            return Response.ok({"message": "Friend request rejected"})
            
        elif http_method == "DELETE":
            # Delete friendship
            Relation.delete_relation(user_id, relation_dto.friend_id, conn)
            conn.close()
            return Response.no_content()
        
        else:
            conn.close()
            return Response.error(405, "", "Method not allowed")
        
    except AuthorizationError as e:
        return Response.error(e.status_code, "", "Unauthorized")
    except json.JSONDecodeError as e:
        return Response.error(400, str(e), "Invalid JSON in request body")
    except ValueError as e:
        return Response.bad_request(str(e))
    except Exception as e:
        return Response.error(500, str(e), "Internal server error")
