"""
Lambda handler for stripe_checkout
Extended Stripe webhook handler v2
Handles checkout.session.completed, transfer.created, and payout events
"""
import json
import os
import sys

# Add parent directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from helpers.response import Response
from database.payment import Payment
from database.payment_history import PaymentHistory
from database.members import Member
import stripe


def lambda_handler(event, context):
    """
    Lambda handler function for stripe_checkout.
    
    POST /stripe-checkout -> Handle Stripe webhook events
    
    Event Types:
    - checkout.session.completed: Add joydollars to user payment
    - transfer.created: Update deposited money in payment history
    - payout.paid, payout.failed, payout.canceled: Update payment history status
    
    Args:
        event: Lambda event object containing request data
        context: Lambda context object
        
    Returns:
        Response object with statusCode, headers, and body
    """
    if "conn_string" in os.environ and "stripe_secret_key" in os.environ:
        constr = os.environ["conn_string"]
        stripe.api_key = os.environ["stripe_secret_key"]
        try:
            body = json.loads(event.get('body'))
            data = body['data']
            event_type = body['type']
            data_object = data['object']
            print('data_object', data_object)
            print('event_type', event_type)
            
            if event_type == 'checkout.session.completed':
                # Handle successful checkout
                checkout_session_id = data_object['id']
                customer_id = data_object['customer']
                payment_intent = data_object['payment_intent']
                
                line_items = stripe.checkout.Session.list_line_items(checkout_session_id, limit=5)
                
                joydollar = 0
                for item in line_items['data']:
                    description = item['description']
                    quantity = item['quantity']
                    print(f"description = {description}")
                    print(f"quantity = {quantity}")
                    
                    # Parse joydollar amount from description
                    if "joydollar" in description.lower():
                        # Extract number from description (e.g., "100 joydollars" -> 100)
                        words = description.split()
                        for word in words:
                            if word.isdigit():
                                joydollar += int(word) * quantity
                                break
                
                # Find customer by email
                customer = stripe.Customer.retrieve(customer_id)
                customer_email = customer['email']
                
                member = Member(constr)
                user = member.search(customer_email)
                
                if user:
                    user_id = user[0]
                    
                    # Add joydollars to user's payment
                    payment = Payment(constr)
                    payment.add(user_id, joydollar)
                    payment.connection.close()
                    
                    print(f"Added {joydollar} joydollars to user {user_id}")
                else:
                    print(f"User not found for email: {customer_email}")
                
                member.connection.close()
                
            elif event_type == 'transfer.created':
                # Handle transfer creation
                transfer_id = data_object['id']
                amount = data_object['amount']
                destination = data_object['destination']
                
                print(f"Transfer created: {transfer_id}, Amount: {amount}, Destination: {destination}")
                
                # Update deposited money in payment history
                payment_history = PaymentHistory(constr)
                payment_history.update_deposited_money(destination, amount)
                payment_history.connection.close()
                
            elif event_type in ['payout.paid', 'payout.failed', 'payout.canceled']:
                # Handle payout events
                payout_id = data_object['id']
                destination = data_object['destination']
                status = event_type.split('.')[1]  # paid, failed, or canceled
                
                print(f"Payout {status}: {payout_id}, Destination: {destination}")
                
                # Update payment history status
                payment_history = PaymentHistory(constr)
                if status == 'paid':
                    payment_history.update_status(destination, 'completed')
                elif status == 'failed':
                    payment_history.update_status(destination, 'failed')
                elif status == 'canceled':
                    payment_history.update_status(destination, 'canceled')
                payment_history.connection.close()
            
            return Response.ok()
            
        except stripe.error.StripeError as e:
            print(f"Stripe error: {str(e)}")
            return Response.bad_request("STRIPEERROR", str(e))
        except Exception as e:
            print(f"Error: {str(e)}")
            return Response.bad_request("DBERROR", "Service is not available")
    
    return Response.bad_request("INVALIDREQUEST", "Request is not valid")
