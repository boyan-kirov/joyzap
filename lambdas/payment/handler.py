"""
Lambda handler for payment
Payment operations and history management
"""
import json
import os
import sys

# Add parent directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from helpers.response import Response
from helpers.jwt import JWT
from database.payment import Payment
from database.payment_history import PaymentHistory
import stripe


def lambda_handler(event, context):
    """
    Lambda handler function for payment.
    
    GET /payment -> Get payment history for user
    POST /payment -> Create Stripe account link redirect
    GET /payment/pending -> Get pending balance
    
    Args:
        event: Lambda event object containing request data
        context: Lambda context object
        
    Returns:
        Response object with statusCode, headers, and body
    """
    if "conn_string" in os.environ and "jwt_secret" in os.environ and "stripe_secret_key" in os.environ:
        constr = os.environ["conn_string"]
        stripe.api_key = os.environ["stripe_secret_key"]
        jwt_helper = JWT(os.environ["jwt_secret"])
        decoded_token = jwt_helper.auth(event)
        try:
            if event.get('requestContext').get('http').get('method') == 'GET':
                if event.get('requestContext').get('http').get('path') == "/payment":
                    # Get payment history
                    payment_history = PaymentHistory(constr)
                    response = payment_history.get(decoded_token.get("user_id"))
                    payment_history.connection.close()
                    if response:
                        return Response.ok({"data": response})
                elif event.get('requestContext').get('http').get('path') == "/payment/pending":
                    # Get pending balance
                    payment_history = PaymentHistory(constr)
                    response = payment_history.get_pending_balance(decoded_token.get("user_id"))
                    payment_history.connection.close()
                    if response:
                        return Response.ok({"pending_balance": response})
                    else:
                        return Response.ok({"pending_balance": 0})
            elif event.get('requestContext').get('http').get('method') == 'POST':
                # Create Stripe account link redirect
                body = json.loads(event.get('body'))
                account_id = body.get('account_id')
                
                if not account_id:
                    return Response.bad_request("INVALIDREQUEST", "account_id is required")
                
                # Create account link for Stripe Connect onboarding/dashboard
                account_link = stripe.AccountLink.create(
                    account=account_id,
                    refresh_url=body.get('refresh_url', 'https://yourapp.com/reauth'),
                    return_url=body.get('return_url', 'https://yourapp.com/return'),
                    type=body.get('type', 'account_onboarding')
                )
                
                return Response.ok({"url": account_link.url})
                
        except stripe.error.StripeError as e:
            print(f"Stripe error: {str(e)}")
            return Response.bad_request("STRIPEERROR", str(e))
        except Exception as e:
            print(e)
            return Response.bad_request("DBERROR", "Service is not available")
    return Response.bad_request("INVALIDREQUEST", "Request is not valid")
