"""
Database helper for user relationship operations (friends, followers, etc.)
"""
import psycopg2
import psycopg2.extras


class Relation:
    """Helper class for managing user relationships in the database"""
    
    def __init__(self, conn_string):
        """
        Initialize the Relation helper with a database connection.
        
        Args:
            conn_string: PostgreSQL connection string
        """
        self.connection = psycopg2.connect(conn_string)
        self.cursor = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    
    def my_friends(self, user_id, keyword=""):
        """
        Get list of friends for a user with optional keyword search.
        
        Args:
            user_id: The ID of the user whose friends to retrieve
            keyword: Optional search keyword to filter friends by name
            
        Returns:
            List of friend records
        """
        if keyword:
            # Search friends by keyword
            query = """
                SELECT u.* 
                FROM users u
                INNER JOIN friendships f ON (f.user_id = %s AND f.friend_id = u.id) 
                    OR (f.friend_id = %s AND f.user_id = u.id)
                WHERE f.status = 'accepted'
                    AND (u.name ILIKE %s OR u.email ILIKE %s OR u.username ILIKE %s)
                ORDER BY u.name
            """
            search_pattern = f"%{keyword}%"
            self.cursor.execute(query, (user_id, user_id, search_pattern, search_pattern, search_pattern))
        else:
            # Get all friends
            query = """
                SELECT u.* 
                FROM users u
                INNER JOIN friendships f ON (f.user_id = %s AND f.friend_id = u.id) 
                    OR (f.friend_id = %s AND f.user_id = u.id)
                WHERE f.status = 'accepted'
                ORDER BY u.name
            """
            self.cursor.execute(query, (user_id, user_id))
        
        return self.cursor.fetchall()
    
    def get_friendship_status(self, user_id, friend_id):
        """
        Get friendship status between two users.
        
        Args:
            user_id: First user ID
            friend_id: Second user ID
            
        Returns:
            Friendship record or None
        """
        query = """
            SELECT * FROM friendships 
            WHERE (user_id = %s AND friend_id = %s) 
               OR (user_id = %s AND friend_id = %s)
        """
        self.cursor.execute(query, (user_id, friend_id, friend_id, user_id))
        return self.cursor.fetchone()
    
    def send_friend_request(self, user_id, friend_id):
        """
        Send a friend request.
        
        Args:
            user_id: User sending the request
            friend_id: User receiving the request
            
        Returns:
            Created friendship record
        """
        query = """
            INSERT INTO friendships (user_id, friend_id, status, created_at)
            VALUES (%s, %s, 'pending', NOW())
            RETURNING *
        """
        self.cursor.execute(query, (user_id, friend_id))
        result = self.cursor.fetchone()
        self.connection.commit()
        return result
    
    def accept_friend_request(self, user_id, friend_id):
        """
        Accept a friend request.
        
        Args:
            user_id: User accepting the request
            friend_id: User who sent the request
            
        Returns:
            Updated friendship record
        """
        query = """
            UPDATE friendships 
            SET status = 'accepted', updated_at = NOW()
            WHERE friend_id = %s AND user_id = %s AND status = 'pending'
            RETURNING *
        """
        self.cursor.execute(query, (user_id, friend_id))
        result = self.cursor.fetchone()
        self.connection.commit()
        return result
    
    def reject_friend_request(self, user_id, friend_id):
        """
        Reject a friend request.
        
        Args:
            user_id: User rejecting the request
            friend_id: User who sent the request
            
        Returns:
            Number of rows affected
        """
        query = """
            DELETE FROM friendships 
            WHERE friend_id = %s AND user_id = %s AND status = 'pending'
        """
        self.cursor.execute(query, (user_id, friend_id))
        rows_affected = self.cursor.rowcount
        self.connection.commit()
        return rows_affected
    
    def remove_friend(self, user_id, friend_id):
        """
        Remove a friendship (unfriend).
        
        Args:
            user_id: First user ID
            friend_id: Second user ID
            
        Returns:
            Number of rows affected
        """
        query = """
            DELETE FROM friendships 
            WHERE (user_id = %s AND friend_id = %s) 
               OR (user_id = %s AND friend_id = %s)
        """
        self.cursor.execute(query, (user_id, friend_id, friend_id, user_id))
        rows_affected = self.cursor.rowcount
        self.connection.commit()
        return rows_affected
    
    def get_pending_requests(self, user_id):
        """
        Get pending friend requests for a user.
        
        Args:
            user_id: User ID to get pending requests for
            
        Returns:
            List of pending friend requests
        """
        query = """
            SELECT u.*, f.created_at as request_date
            FROM users u
            INNER JOIN friendships f ON f.user_id = u.id
            WHERE f.friend_id = %s AND f.status = 'pending'
            ORDER BY f.created_at DESC
        """
        self.cursor.execute(query, (user_id,))
        return self.cursor.fetchall()
    
    def get_mutual_friends(self, user_id, other_user_id):
        """
        Get mutual friends between two users.
        
        Args:
            user_id: First user ID
            other_user_id: Second user ID
            
        Returns:
            List of mutual friends
        """
        query = """
            SELECT u.* FROM users u
            WHERE u.id IN (
                SELECT CASE 
                    WHEN f1.user_id = %s THEN f1.friend_id 
                    ELSE f1.user_id 
                END
                FROM friendships f1
                WHERE ((f1.user_id = %s OR f1.friend_id = %s) AND f1.status = 'accepted')
                INTERSECT
                SELECT CASE 
                    WHEN f2.user_id = %s THEN f2.friend_id 
                    ELSE f2.user_id 
                END
                FROM friendships f2
                WHERE ((f2.user_id = %s OR f2.friend_id = %s) AND f2.status = 'accepted')
            )
            ORDER BY u.name
        """
        self.cursor.execute(query, (user_id, user_id, user_id, other_user_id, other_user_id, other_user_id))
        return self.cursor.fetchall()
    
    @staticmethod
    def create(user_id, friend_id, conn):
        """
        Create a new friend request (static method for use in lambdas).
        
        Args:
            user_id: User sending the request
            friend_id: User receiving the request
            conn: Database connection
            
        Returns:
            Created friendship record
        """
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = """
            INSERT INTO relations (from_user, to_user, status, created_at)
            VALUES (%s, %s, 'pending', NOW())
            RETURNING *
        """
        cursor.execute(query, (user_id, friend_id))
        result = cursor.fetchone()
        conn.commit()
        cursor.close()
        return result
    
    @staticmethod
    def accept_relation(user_id, friend_id, conn):
        """
        Accept a friend request (static method for use in lambdas).
        
        Args:
            user_id: User accepting the request
            friend_id: User who sent the request
            conn: Database connection
            
        Returns:
            Updated friendship record
        """
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = """
            UPDATE relations 
            SET status = 'accepted', updated_at = NOW()
            WHERE to_user = %s AND from_user = %s AND status = 'pending'
            RETURNING *
        """
        cursor.execute(query, (user_id, friend_id))
        result = cursor.fetchone()
        conn.commit()
        cursor.close()
        return result
    
    @staticmethod
    def delete_relation(user_id, friend_id, conn):
        """
        Delete a friendship (static method for use in lambdas).
        
        Args:
            user_id: First user ID
            friend_id: Second user ID
            conn: Database connection
            
        Returns:
            Number of rows affected
        """
        cursor = conn.cursor()
        query = """
            DELETE FROM relations 
            WHERE (from_user = %s AND to_user = %s) 
               OR (from_user = %s AND to_user = %s)
        """
        cursor.execute(query, (user_id, friend_id, friend_id, user_id))
        rows_affected = cursor.rowcount
        conn.commit()
        cursor.close()
        return rows_affected
    
    def my_followers(self, user_id, keyword=""):
        """
        Get list of followers for a user.
        
        Args:
            user_id: The ID of the user whose followers to retrieve
            keyword: Optional search keyword to filter followers by name
            
        Returns:
            List of follower records
        """
        if keyword:
            query = """
                SELECT u.* 
                FROM users u
                INNER JOIN relations r ON r.from_user = u.id
                WHERE r.to_user = %s AND r.status = 'pending'
                    AND (u.name ILIKE %s OR u.email ILIKE %s)
                ORDER BY u.name
            """
            search_pattern = f"%{keyword}%"
            self.cursor.execute(query, (user_id, search_pattern, search_pattern))
        else:
            query = """
                SELECT u.* 
                FROM users u
                INNER JOIN relations r ON r.from_user = u.id
                WHERE r.to_user = %s AND r.status = 'pending'
                ORDER BY u.name
            """
            self.cursor.execute(query, (user_id,))
        
        return self.cursor.fetchall()
    
    def my_follows(self, user_id, keyword=""):
        """
        Get list of users this user follows.
        
        Args:
            user_id: The ID of the user
            keyword: Optional search keyword
            
        Returns:
            List of followed user records
        """
        if keyword:
            query = """
                SELECT u.* 
                FROM users u
                INNER JOIN relations r ON r.to_user = u.id
                WHERE r.from_user = %s AND r.status = 'pending'
                    AND (u.name ILIKE %s OR u.email ILIKE %s)
                ORDER BY u.name
            """
            search_pattern = f"%{keyword}%"
            self.cursor.execute(query, (user_id, search_pattern, search_pattern))
        else:
            query = """
                SELECT u.* 
                FROM users u
                INNER JOIN relations r ON r.to_user = u.id
                WHERE r.from_user = %s AND r.status = 'pending'
                ORDER BY u.name
            """
            self.cursor.execute(query, (user_id,))
        
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
