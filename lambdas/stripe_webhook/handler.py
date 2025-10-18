"""
Lambda handler for Stripe webhook events
Processes payment events from Stripe including checkouts, transfers, and payouts
"""
import os
import sys
import json
import datetime
import psycopg2
import psycopg2.extras
import stripe

# Add parent directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from helpers.response import Response
from database.members import Member
from database.payment_history import PaymentHistory
from database.payment import Payment


def lambda_handler(event, context):
    """
    Lambda handler for Stripe webhook events.
    Handles checkout completion, transfers, and payout events.
    
    Args:
        event: Lambda event object containing Stripe webhook data
        context: Lambda context object
        
    Returns:
        Response object with statusCode and body
    """
    constr = os.environ["conn_string"]
    endpoint_secret = os.environ["endpoint_secret"]
    profit_account_id = os.environ["profit_account_id"]
    stripe.api_key = os.environ["secret_key"]
    connection = psycopg2.connect(constr)

    try:
        try:
            print("event", event)
            stripe_event = None
            body = event.get("body").encode("utf-8")
            signature = event.get("headers")["Stripe-Signature"]

            try:
                stripe_event = stripe.Webhook.construct_event(
                    payload=body, sig_header=signature, secret=endpoint_secret
                )
            except ValueError as e:
                # Invalid payload
                print("Invalid payload", e)
                raise e
            except stripe.error.SignatureVerificationError as e:
                # Invalid signature
                print("Invalid signature", e)
                raise e

            print("stripe_event", stripe_event)
            
            # Handle the event
            if stripe_event["type"] == "checkout.session.completed":
                session = stripe_event["data"]["object"]
                print('stripe_event["data"]', stripe_event["data"])
                print('session.get("amount_total")', session.get("amount_total"), type(session.get("amount_total")))
                print('session.get("customer_details").get("email")', session.get("customer_details").get("email"))
                print('profit_account_id', profit_account_id)

                purchase_id = session.get("metadata").get("purchaseId")
                email = session.get("customer_details").get("email")

                if purchase_id is None:
                    return Response.bad_request("Purchase id not found.")
                
                if email is None:
                    return Response.bad_request("User email is not found.")

                sql = f"""
                    SELECT * FROM payload_joy_dollar_list WHERE id = '{purchase_id}';
                """
                cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
                cursor.execute(sql)
                purchase = json.loads(json.dumps(cursor.fetchone(), allow_nan=True))
                print("purchase", purchase)

                if purchase is None:
                    return Response.bad_request("Purchase not found.")
                
                jd_dollar = int(purchase.get("joy_dollar"))

                member_db = Member(constr)
                payment = Payment(constr)
                money_history = PaymentHistory(constr)

                money_history.create('check_in', jd_dollar, None, email, None, None)
                money_history.connection.close()

                payment.add(jd_dollar, email, f'On {datetime.date.today().strftime("%d.%m.%y")} you bought the JD {purchase.get("name").title()}', purchase.get("id"))
                payment.connection.close()

                res = member_db.add(jd_dollar, email)
                member_db.connection.close()
                print("res", res)

                # Optional: Transfer to profit account
                # stripe.Transfer.create(
                #     amount=int(session.get("amount_total") * 0.18),
                #     currency="bgn",
                #     destination=profit_account_id
                # )

                if res[0]:
                    return Response.ok({"message": res[1]})
                else:
                    return Response.bad_request(res[1])

            elif stripe_event["type"] == "transfer.created":
                transfer = stripe_event["data"]["object"]
                print("transfer", transfer)
                print('amount', transfer.get("metadata").get("amount"))

                amount = transfer.get("metadata").get("amount")

                if amount is not None:
                    destination = transfer.get("destination")

                    if destination is None:
                        return Response.bad_request("Destination not found.")

                    member_db = Member(constr)
                    payment = Payment(constr)

                    dollar = float(amount) * 10

                    res = member_db.sub(dollar, destination)
                    member_db.connection.close()

                    payment.sub((-1) * dollar, destination)
                    payment.connection.close()
                    
                    print("res", res)
                    if res[0]:
                        return Response.ok({"message": res[1]})
                    else:
                        return Response.bad_request(res[1])
                else:
                    return Response.ok()
                    
            elif stripe_event["type"] == "payout.created":
                payout_created = stripe_event["data"]["object"]
                print("payout_created", payout_created)
                return Response.ok(payout_created)
                
            elif stripe_event["type"] == "checkout.session.async_payment_succeeded":
                async_payment_succeeded = stripe_event["data"]["object"]
                print("async_payment_succeeded", async_payment_succeeded)
                return Response.ok(async_payment_succeeded)
                
            elif stripe_event["type"] == "payout.paid":
                payout_paid = stripe_event["data"]["object"]
                print("payout_paid", payout_paid)
                return Response.ok(payout_paid)
                
            elif stripe_event["type"] == "balance.available":
                balance_available = stripe_event["data"]["object"]
                print("balance_available", balance_available)
                return Response.ok(balance_available)
            else:
                print("Unhandled event type {}".format(stripe_event["type"]))
                return Response.ok({"message": "Event type not handled"})
                
        except Exception as e:
            print(e)
            return Response.bad_request("DBERROR", "Service is not available")
    except Exception as e:
        print(e)
        return Response.bad_request("DBERROR", "Service is not available")
