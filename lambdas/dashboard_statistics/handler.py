"""
Lambda handler for dashboard_statistics
Retrieves dashboard statistics and transaction history
"""
import os
import sys
import json

# Add parent directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from helpers.jwt import JWT, AuthorizationError
from helpers.response import Response
from database.dashboard import Dashboard


def lambda_handler(event, context):
    """
    Lambda handler function for dashboard_statistics.
    
    GET /dashboard/statistics -> Get dashboard and transaction statistics
    
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
        
        # Get statistics
        dashboard_stats = Dashboard.get_statistics(user_id)
        transaction_stats = Dashboard.get_trascation_statistics(user_id)
        
        result = {
            "dashboard": dashboard_stats,
            "transactions": transaction_stats
        }
        
        return Response.ok(result)
        
    except AuthorizationError as e:
        return Response.error(e.status_code, "", "Unauthorized")
    except KeyError as e:
        return Response.error(400, str(e), f"Missing required field: {str(e)}")
    except Exception as e:
        return Response.error(500, str(e), "Internal Server Error")
