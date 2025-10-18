"""
Lambda handler for calendar_events
Handles calendar event CRUD operations
"""
import os
import sys
import json
import psycopg2

# Add parent directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from helpers.jwt import JWT, AuthorizationError
from helpers.response import Response
from database.calendars import Calendar
from dto.calendar_dto import CalendarBody


def lambda_handler(event, context):
    """
    Lambda handler function for calendar_events.
    
    POST /calendar -> Create calendar event
    GET /calendar -> Search/list calendar events
    GET /calendar/{id} -> Get event detail
    PUT /calendar -> Update calendar event
    DELETE /calendar/{id} -> Delete calendar event
    
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
        
        # Connect to database
        conn = psycopg2.connect(
            host=os.environ["db_host"],
            port=os.environ["db_port"],
            dbname=os.environ["db_name"],
            user=os.environ["db_user"],
            password=os.environ["db_password"]
        )
        
        # Route based on HTTP method and path
        http_method = event.get("httpMethod", event.get("requestContext", {}).get("http", {}).get("method", ""))
        path_parameters = event.get("pathParameters") or {}
        event_id = path_parameters.get("id")
        
        if http_method == "GET":
            if event_id:
                # Get event detail
                event_detail = Calendar.get_event_detail(event_id, user_id, conn)
                conn.close()
                return Response.ok(event_detail)
            else:
                # Search/list events
                query_params = event.get("queryStringParameters") or {}
                keyword = query_params.get("keyword", "")
                events = Calendar.search(user_id, keyword, conn)
                conn.close()
                return Response.ok(events)
                
        elif http_method == "POST":
            # Create calendar event
            body_data = {}
            if isinstance(event.get("body"), dict):
                body_data = event["body"]
            elif isinstance(event.get("body"), str):
                body_data = json.loads(event["body"])
            
            calendar_dto = CalendarBody.from_dict(body_data)
            new_event = Calendar.create(user_id, calendar_dto, conn)
            conn.close()
            return Response.created(new_event)
            
        elif http_method == "PUT":
            # Update calendar event
            body_data = {}
            if isinstance(event.get("body"), dict):
                body_data = event["body"]
            elif isinstance(event.get("body"), str):
                body_data = json.loads(event["body"])
            
            calendar_dto = CalendarBody.from_dict(body_data)
            updated_event = Calendar.edit_event(calendar_dto.id, user_id, calendar_dto, conn)
            conn.close()
            return Response.ok(updated_event)
            
        elif http_method == "DELETE":
            if not event_id:
                conn.close()
                return Response.bad_request("Missing event ID")
            
            # Delete calendar event
            Calendar.delete_event(event_id, user_id, conn)
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
    except KeyError as e:
        return Response.error(400, str(e), f"Missing required field: {str(e)}")
    except Exception as e:
        return Response.error(500, str(e), "Internal Server Error")
