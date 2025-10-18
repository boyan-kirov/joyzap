"""
Data Transfer Object for Report operations
"""


class Report:
    """DTO for report requests"""
    
    def __init__(self, title, description, event_id, report_to, **kwargs):
        """
        Initialize Report DTO
        
        Args:
            title: Report title
            description: Report description
            event_id: ID of the event being reported
            report_to: User ID being reported
        """
        self.title = title
        self.description = description
        self.event_id = event_id
        self.report_to = report_to
        
        # Validate required fields
        if not title:
            raise ValueError("title is required")
        if not description:
            raise ValueError("description is required")
        if not event_id:
            raise ValueError("event_id is required")
        if not report_to:
            raise ValueError("report_to is required")
