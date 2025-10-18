"""
Data Transfer Object for Calendar operations
"""
from datetime import datetime


class CalendarBody:
    """DTO for calendar event requests"""
    
    def __init__(self, title, description, event_date, location, id=None):
        """
        Initialize CalendarBody
        
        Args:
            title: Event title
            description: Event description
            event_date: Event date/time
            location: Event location
            id: Optional event ID (for updates)
        """
        self.id = id
        self.title = title
        self.description = description
        self.event_date = event_date
        self.location = location
        
        # Validate required fields
        if not title:
            raise ValueError("title is required")
        if not event_date:
            raise ValueError("event_date is required")
    
    @classmethod
    def from_dict(cls, data):
        """
        Create CalendarBody from dictionary
        
        Args:
            data: Dictionary with calendar data
            
        Returns:
            CalendarBody instance
        """
        return cls(
            id=data.get('id'),
            title=data.get('title'),
            description=data.get('description', ''),
            event_date=data.get('event_date'),
            location=data.get('location', '')
        )
    
    def to_dict(self):
        """
        Convert CalendarBody to dictionary
        
        Returns:
            dict: Calendar data
        """
        result = {
            'title': self.title,
            'description': self.description,
            'event_date': self.event_date,
            'location': self.location
        }
        
        if self.id is not None:
            result['id'] = self.id
            
        return result
