"""
Database helper for notification operations
"""
import psycopg2
import psycopg2.extras
from datetime import datetime


class Notification:
    """Helper class for managing notifications in the database"""
    
    def __init__(self, conn_string):
        """
        Initialize the Notification helper with a database connection.
        
        Args:
            conn_string: PostgreSQL connection string
        """
        self.connection = psycopg2.connect(conn_string)
        self.cursor = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    
    def get_user(self, params):
        """
        Get all notifications for a user.
        
        Args:
            params: Dictionary containing user_id
            
        Returns:
            List of notification records
        """
        user_id = params.get("user_id")
        
        query = """
            SELECT * FROM notifications 
            WHERE user_id = %s 
            ORDER BY created_at DESC
        """
        self.cursor.execute(query, (user_id,))
        return self.cursor.fetchall()
    
    def get_unread(self, user_id):
        """
        Get unread notifications for a user.
        
        Args:
            user_id: User ID
            
        Returns:
            List of unread notification records
        """
        query = """
            SELECT * FROM notifications 
            WHERE user_id = %s AND is_read = FALSE 
            ORDER BY created_at DESC
        """
        self.cursor.execute(query, (user_id,))
        return self.cursor.fetchall()
    
    def get_unread_count(self, user_id):
        """
        Get count of unread notifications for a user.
        
        Args:
            user_id: User ID
            
        Returns:
            Count of unread notifications
        """
        query = """
            SELECT COUNT(*) as count FROM notifications 
            WHERE user_id = %s AND is_read = FALSE
        """
        self.cursor.execute(query, (user_id,))
        result = self.cursor.fetchone()
        return result['count'] if result else 0
    
    def update(self, params):
        """
        Update a notification (typically to mark as read).
        
        Args:
            params: Dictionary containing notification update data
                    Expected keys: user_id, notification_id, and fields to update
            
        Returns:
            Updated notification record
        """
        user_id = params.get("user_id")
        notification_id = params.get("notification_id") or params.get("id")
        
        # Build update query dynamically based on provided fields
        update_fields = []
        update_values = []
        
        if "is_read" in params:
            update_fields.append("is_read = %s")
            update_values.append(params["is_read"])
        
        if "is_deleted" in params:
            update_fields.append("is_deleted = %s")
            update_values.append(params["is_deleted"])
        
        # Always update the updated_at timestamp
        update_fields.append("updated_at = %s")
        update_values.append(datetime.now())
        
        # Add WHERE clause parameters
        update_values.extend([notification_id, user_id])
        
        query = f"""
            UPDATE notifications 
            SET {', '.join(update_fields)}
            WHERE id = %s AND user_id = %s
            RETURNING *
        """
        
        self.cursor.execute(query, update_values)
        result = self.cursor.fetchone()
        self.connection.commit()
        return result
    
    def mark_as_read(self, notification_id, user_id):
        """
        Mark a notification as read.
        
        Args:
            notification_id: Notification ID
            user_id: User ID (for security)
            
        Returns:
            Updated notification record
        """
        query = """
            UPDATE notifications 
            SET is_read = TRUE, updated_at = %s
            WHERE id = %s AND user_id = %s
            RETURNING *
        """
        self.cursor.execute(query, (datetime.now(), notification_id, user_id))
        result = self.cursor.fetchone()
        self.connection.commit()
        return result
    
    def mark_all_as_read(self, user_id):
        """
        Mark all notifications as read for a user.
        
        Args:
            user_id: User ID
            
        Returns:
            Number of rows affected
        """
        query = """
            UPDATE notifications 
            SET is_read = TRUE, updated_at = %s
            WHERE user_id = %s AND is_read = FALSE
        """
        self.cursor.execute(query, (datetime.now(), user_id))
        rows_affected = self.cursor.rowcount
        self.connection.commit()
        return rows_affected
    
    def create(self, params):
        """
        Create a new notification.
        
        Args:
            params: Dictionary containing notification data
                    Expected keys: user_id, type, title, message, data (optional)
            
        Returns:
            Created notification record
        """
        query = """
            INSERT INTO notifications 
            (user_id, type, title, message, data, is_read, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, FALSE, %s, %s)
            RETURNING *
        """
        
        now = datetime.now()
        self.cursor.execute(query, (
            params.get("user_id"),
            params.get("type"),
            params.get("title"),
            params.get("message"),
            params.get("data"),
            now,
            now
        ))
        result = self.cursor.fetchone()
        self.connection.commit()
        return result
    
    def delete(self, notification_id, user_id):
        """
        Delete a notification (or mark as deleted).
        
        Args:
            notification_id: Notification ID
            user_id: User ID (for security)
            
        Returns:
            Number of rows affected
        """
        # Soft delete
        query = """
            UPDATE notifications 
            SET is_deleted = TRUE, updated_at = %s
            WHERE id = %s AND user_id = %s
        """
        self.cursor.execute(query, (datetime.now(), notification_id, user_id))
        rows_affected = self.cursor.rowcount
        self.connection.commit()
        return rows_affected
    
    def delete_all(self, user_id):
        """
        Delete all notifications for a user (soft delete).
        
        Args:
            user_id: User ID
            
        Returns:
            Number of rows affected
        """
        query = """
            UPDATE notifications 
            SET is_deleted = TRUE, updated_at = %s
            WHERE user_id = %s AND is_deleted = FALSE
        """
        self.cursor.execute(query, (datetime.now(), user_id))
        rows_affected = self.cursor.rowcount
        self.connection.commit()
        return rows_affected
    
    def get_by_type(self, user_id, notification_type):
        """
        Get notifications by type for a user.
        
        Args:
            user_id: User ID
            notification_type: Type of notification
            
        Returns:
            List of notification records
        """
        query = """
            SELECT * FROM notifications 
            WHERE user_id = %s AND type = %s AND is_deleted = FALSE
            ORDER BY created_at DESC
        """
        self.cursor.execute(query, (user_id, notification_type))
        return self.cursor.fetchall()
    
    def __del__(self):
        """Close cursor and connection when object is destroyed"""
        try:
            if hasattr(self, 'cursor') and self.cursor:
                self.cursor.close()
            if hasattr(self, 'connection') and self.connection:
                self.connection.close()
        except:
            pass
