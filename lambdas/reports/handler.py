"""
Lambda handler for reports
Report management (create and retrieve)
"""
import json
import os
import sys

# Add parent directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from helpers.response import Response
from helpers.jwt import JWT
from database.reports import Report as ReportDB
from dto.report_dto import Report


def lambda_handler(event, context):
    """
    Lambda handler function for reports.
    
    POST /reports -> Create new report
    GET /reports -> Get all reports for user
    
    Args:
        event: Lambda event object containing request data
        context: Lambda context object
        
    Returns:
        Response object with statusCode, headers, and body
    """
    if "conn_string" in os.environ and "jwt_secret" in os.environ:
        constr = os.environ["conn_string"]
        jwt_helper = JWT(os.environ["jwt_secret"])
        decoded_token = jwt_helper.auth(event)
        try:
            if event.get('requestContext').get('http').get('method') == 'POST':
                # Create new report
                body = json.loads(event.get('body'))
                report = Report(body)
                
                if report.validate():
                    report_db = ReportDB(constr)
                    response = report_db.create(decoded_token.get("user_id"), report)
                    report_db.connection.close()
                    
                    if response:
                        return Response.ok()
                    else:
                        return Response.bad_request("DBERROR", "Failed to create report")
                else:
                    return Response.validate_error()
                    
            elif event.get('requestContext').get('http').get('method') == 'GET':
                # Get all reports
                report_db = ReportDB(constr)
                response = report_db.get_all(decoded_token.get("user_id"))
                report_db.connection.close()
                
                if response:
                    return Response.ok({"data": response})
                else:
                    return Response.ok({"data": []})
                    
        except Exception as e:
            print(e)
            return Response.bad_request("DBERROR", "Service is not available")
    
    return Response.bad_request("INVALIDREQUEST", "Request is not valid")
