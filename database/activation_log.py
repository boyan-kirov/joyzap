"""
Database operations for activity logs
"""
import psycopg2
import psycopg2.extras


class Activity:
    """Helper class for activity log operations"""
    
    def __init__(self, conn_string):
        """
        Initialize the Activity helper with a database connection.
        
        Args:
            conn_string: PostgreSQL connection string
        """
        self.connection = psycopg2.connect(conn_string)
        self.cursor = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    
    def get_activity_log(self, user_id):
        """
        Get activity log for a user.
        
        Args:
            user_id: User ID
            
        Returns:
            List of activity log records
        """
        query = """
            SELECT 
                al.id,
                al.user_id,
                al.action,
                al.description,
                al.ip_address,
                al.user_agent,
                al.created_at
            FROM activity_log al
            WHERE al.user_id = %s
            ORDER BY al.created_at DESC
            LIMIT 100
        """
        self.cursor.execute(query, (user_id,))
        return self.cursor.fetchall()
    
    def create_log(self, user_id, action, description, ip_address=None, user_agent=None):
        """
        Create a new activity log entry.
        
        Args:
            user_id: User ID
            action: Action type
            description: Description of the action
            ip_address: Optional IP address
            user_agent: Optional user agent string
            
        Returns:
            Created log record
        """
        query = """
            INSERT INTO activity_log (user_id, action, description, ip_address, user_agent, created_at)
            VALUES (%s, %s, %s, %s, %s, NOW())
            RETURNING *
        """
        self.cursor.execute(query, (user_id, action, description, ip_address, user_agent))
        result = self.cursor.fetchone()
        self.connection.commit()
        return result
    
    def __del__(self):
        """Close cursor and connection when object is destroyed"""
        try:
            if hasattr(self, 'cursor') and self.cursor:
                self.cursor.close()
            if hasattr(self, 'connection') and self.connection:
                self.connection.close()
        except:
            pass
