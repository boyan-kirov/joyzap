"""
Data Transfer Objects for joyzap operations
"""


class Present:
    """DTO for present joyzaps"""
    
    def __init__(self, title, message, gift_id, amount, receiver_id=None, receiver_email=None, receiver_phone=None, **kwargs):
        self.title = title
        self.message = message
        self.gift_id = gift_id
        self.amount = amount
        self.receiver_id = receiver_id
        self.receiver_email = receiver_email
        self.receiver_phone = receiver_phone


class Card:
    """DTO for card joyzaps"""
    
    def __init__(self, title, message, design, receiver_id=None, receiver_email=None, receiver_phone=None, **kwargs):
        self.title = title
        self.message = message
        self.design = design
        self.receiver_id = receiver_id
        self.receiver_email = receiver_email
        self.receiver_phone = receiver_phone


class TimeCapsule:
    """DTO for time capsule joyzaps"""
    
    def __init__(self, title, message, unlock_date, receiver_id=None, receiver_email=None, receiver_phone=None, **kwargs):
        self.title = title
        self.message = message
        self.unlock_date = unlock_date
        self.receiver_id = receiver_id
        self.receiver_email = receiver_email
        self.receiver_phone = receiver_phone


class MistyPresent:
    """DTO for mystery present joyzaps"""
    
    def __init__(self, title, message, gift_id, amount, receiver_email=None, receiver_phone=None, **kwargs):
        self.title = title
        self.message = message
        self.gift_id = gift_id
        self.amount = amount
        self.receiver_email = receiver_email
        self.receiver_phone = receiver_phone


class MistyCard:
    """DTO for mystery card joyzaps"""
    
    def __init__(self, title, message, design, receiver_email=None, receiver_phone=None, **kwargs):
        self.title = title
        self.message = message
        self.design = design
        self.receiver_email = receiver_email
        self.receiver_phone = receiver_phone


class MistyTimeCapsule:
    """DTO for mystery time capsule joyzaps"""
    
    def __init__(self, title, message, unlock_date, receiver_email=None, receiver_phone=None, **kwargs):
        self.title = title
        self.message = message
        self.unlock_date = unlock_date
        self.receiver_email = receiver_email
        self.receiver_phone = receiver_phone
