"""
Lambda handler for timecapsule_collector
Scheduled task to collect expired time capsules
Runs periodically to process time capsules and update payment history
"""
import json
import os
import sys

# Add parent directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from helpers.response import Response
from database.joyzaps import Joyzap
from database.payment_history import PaymentHistory


def lambda_handler(event, context):
    """
    Lambda handler function for timecapsule_collector.
    
    Scheduled task (no authentication required)
    Collects expired time capsules and updates payment history
    
    Args:
        event: Lambda event object containing request data
        context: Lambda context object
        
    Returns:
        Response object with statusCode, headers, and body
    """
    if "conn_string" in os.environ:
        constr = os.environ["conn_string"]
        try:
            # Collect expired time capsules
            joyzap = Joyzap(constr)
            collected_capsules = joyzap.collect_time_camp()
            joyzap.connection.close()
            
            if collected_capsules:
                # Update payment history for collected capsules
                payment_history = PaymentHistory(constr)
                for capsule in collected_capsules:
                    payment_history.create({
                        'user_id': capsule.get('user_id'),
                        'amount': capsule.get('amount'),
                        'type': 'timecapsule_collection',
                        'status': 'pending'
                    })
                payment_history.connection.close()
                
                print(f"Collected {len(collected_capsules)} time capsules")
                return Response.ok({
                    "message": f"Collected {len(collected_capsules)} time capsules",
                    "count": len(collected_capsules)
                })
            else:
                print("No time capsules to collect")
                return Response.ok({
                    "message": "No time capsules to collect",
                    "count": 0
                })
                
        except Exception as e:
            print(f"Error collecting time capsules: {str(e)}")
            return Response.bad_request("DBERROR", "Service is not available")
    
    return Response.bad_request("INVALIDREQUEST", "Request is not valid")
