"""
Lambda handler for joyzaps
Complex joyzap operations (presents, cards, time capsules)
Handles multiple event types and joyzap types with mystery variants
"""
import json
import os
import sys

# Add parent directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from helpers.response import Response
from helpers.jwt import JWT
from database.joyzaps import Joyzap
from dto.joyzap_dto import Present, Card, TimeCapsule, MistyPresent, MistyCard, MistyTimeCapsule


def lambda_handler(event, context):
    """
    Lambda handler function for joyzaps.
    
    POST /joyzaps -> Add joyzap (present/card/timecapsule with/without user)
    GET /joyzaps -> Get joyzaps (present/card/timecapsule with/without user)
    
    Event types: add-present, add-card, add-timecapsule, add-present-without-user,
                 add-card-without-user, add-timecapsule-without-user,
                 get-presents, get-cards, get-timecamps, get-presents-without-user,
                 get-cards-without-user, get-timecamps-without-user
    
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
            body = json.loads(event.get('body'))
            event_type = body.get('event')
            joyzap = Joyzap(constr)
            
            if event.get('requestContext').get('http').get('method') == 'POST':
                # Add joyzap operations
                if event_type == 'add-present':
                    present = Present(body)
                    if present.validate():
                        response = joyzap.add_present(decoded_token.get("user_id"), present)
                        joyzap.connection.close()
                        if response:
                            return Response.ok()
                        else:
                            return Response.bad_request("DBERROR", "Service is not available")
                    else:
                        return Response.validate_error()
                        
                elif event_type == 'add-card':
                    card = Card(body)
                    if card.validate():
                        response = joyzap.add_card(decoded_token.get("user_id"), card)
                        joyzap.connection.close()
                        if response:
                            return Response.ok()
                        else:
                            return Response.bad_request("DBERROR", "Service is not available")
                    else:
                        return Response.validate_error()
                        
                elif event_type == 'add-timecapsule':
                    timecapsule = TimeCapsule(body)
                    if timecapsule.validate():
                        response = joyzap.add_timecapsule(decoded_token.get("user_id"), timecapsule)
                        joyzap.connection.close()
                        if response:
                            return Response.ok()
                        else:
                            return Response.bad_request("DBERROR", "Service is not available")
                    else:
                        return Response.validate_error()
                        
                elif event_type == 'add-present-without-user':
                    present = MistyPresent(body)
                    if present.validate():
                        response = joyzap.add_present_without_user(decoded_token.get("user_id"), present)
                        joyzap.connection.close()
                        if response:
                            return Response.ok()
                        else:
                            return Response.bad_request("DBERROR", "Service is not available")
                    else:
                        return Response.validate_error()
                        
                elif event_type == 'add-card-without-user':
                    card = MistyCard(body)
                    if card.validate():
                        response = joyzap.add_card_without_user(decoded_token.get("user_id"), card)
                        joyzap.connection.close()
                        if response:
                            return Response.ok()
                        else:
                            return Response.bad_request("DBERROR", "Service is not available")
                    else:
                        return Response.validate_error()
                        
                elif event_type == 'add-timecapsule-without-user':
                    timecapsule = MistyTimeCapsule(body)
                    if timecapsule.validate():
                        response = joyzap.add_timecapsule_without_user(decoded_token.get("user_id"), timecapsule)
                        joyzap.connection.close()
                        if response:
                            return Response.ok()
                        else:
                            return Response.bad_request("DBERROR", "Service is not available")
                    else:
                        return Response.validate_error()
                        
            elif event.get('requestContext').get('http').get('method') == 'GET':
                # Get joyzap operations
                if event_type == 'get-presents':
                    response = joyzap.get_presents(decoded_token.get("user_id"))
                    joyzap.connection.close()
                    if response:
                        return Response.ok({"data": response})
                    else:
                        return Response.ok({"data": []})
                        
                elif event_type == 'get-cards':
                    response = joyzap.get_cards(decoded_token.get("user_id"))
                    joyzap.connection.close()
                    if response:
                        return Response.ok({"data": response})
                    else:
                        return Response.ok({"data": []})
                        
                elif event_type == 'get-timecamps':
                    response = joyzap.get_timecapsules(decoded_token.get("user_id"))
                    joyzap.connection.close()
                    if response:
                        return Response.ok({"data": response})
                    else:
                        return Response.ok({"data": []})
                        
                elif event_type == 'get-presents-without-user':
                    response = joyzap.get_presents_without_user(decoded_token.get("user_id"))
                    joyzap.connection.close()
                    if response:
                        return Response.ok({"data": response})
                    else:
                        return Response.ok({"data": []})
                        
                elif event_type == 'get-cards-without-user':
                    response = joyzap.get_cards_without_user(decoded_token.get("user_id"))
                    joyzap.connection.close()
                    if response:
                        return Response.ok({"data": response})
                    else:
                        return Response.ok({"data": []})
                        
                elif event_type == 'get-timecamps-without-user':
                    response = joyzap.get_timecapsules_without_user(decoded_token.get("user_id"))
                    joyzap.connection.close()
                    if response:
                        return Response.ok({"data": response})
                    else:
                        return Response.ok({"data": []})
                        
        except Exception as e:
            print(e)
            return Response.bad_request("DBERROR", "Service is not available")
    return Response.bad_request("INVALIDREQUEST", "Request is not valid")
