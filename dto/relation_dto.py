"""
Data Transfer Object for Relation operations
"""


class RelationBody:
    """DTO for friend relation requests"""
    
    def __init__(self, friend_id):
        """
        Initialize RelationBody
        
        Args:
            friend_id: ID of the friend user
        """
        self.friend_id = friend_id
        
        # Validate required fields
        if not friend_id:
            raise ValueError("friend_id is required")
    
    @classmethod
    def from_dict(cls, data):
        """
        Create RelationBody from dictionary
        
        Args:
            data: Dictionary with relation data
            
        Returns:
            RelationBody instance
        """
        return cls(
            friend_id=data.get('friend_id')
        )
    
    def to_dict(self):
        """
        Convert RelationBody to dictionary
        
        Returns:
            dict: Relation data
        """
        return {
            'friend_id': self.friend_id
        }
