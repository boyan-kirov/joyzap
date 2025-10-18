"""
Database helper for member/user operations
"""
import psycopg2
import psycopg2.extras


class Member:
    """Helper class for member/user database operations"""
    
    @staticmethod
    def get_connection(conn_string):
        """
        Create a database connection.
        
        Args:
            conn_string: PostgreSQL connection string
            
        Returns:
            Database connection object
        """
        return psycopg2.connect(conn_string)
    
    @staticmethod
    def get_cursor(connection):
        """
        Get a cursor for database operations.
        
        Args:
            connection: Database connection object
            
        Returns:
            Cursor with RealDictCursor factory
        """
        return connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    
    @staticmethod
    def clear_socket_id(connection, socket_id):
        """
        Clear socket_id from users table.
        
        Args:
            connection: Database connection
            socket_id: The socket ID to clear
            
        Returns:
            Number of rows affected
        """
        cursor = connection.cursor()
        query = "UPDATE users SET socket_id = NULL WHERE socket_id = %s"
        cursor.execute(query, (socket_id,))
        rows_affected = cursor.rowcount
        connection.commit()
        cursor.close()
        return rows_affected
    
    @staticmethod
    def update_socket_id(connection, user_id, socket_id):
        """
        Update socket_id for a user.
        
        Args:
            connection: Database connection
            user_id: The user ID
            socket_id: The new socket ID
            
        Returns:
            Number of rows affected
        """
        cursor = connection.cursor()
        query = "UPDATE users SET socket_id = %s WHERE id = %s"
        cursor.execute(query, (socket_id, user_id))
        rows_affected = cursor.rowcount
        connection.commit()
        cursor.close()
        return rows_affected
    
    @staticmethod
    def get_user_by_id(connection, user_id):
        """
        Get user by ID.
        
        Args:
            connection: Database connection
            user_id: The user ID
            
        Returns:
            User record as dictionary or None
        """
        cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "SELECT * FROM users WHERE id = %s"
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()
        cursor.close()
        return result
    
    @staticmethod
    def get_user_by_socket_id(connection, socket_id):
        """
        Get user by socket ID.
        
        Args:
            connection: Database connection
            socket_id: The socket ID
            
        Returns:
            User record as dictionary or None
        """
        cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "SELECT * FROM users WHERE socket_id = %s"
        cursor.execute(query, (socket_id,))
        result = cursor.fetchone()
        cursor.close()
        return result
    
    @staticmethod
    def add(conn_string, amount, email):
        """
        Add joy dollars to a user's account.
        
        Args:
            conn_string: Database connection string
            amount: Amount to add
            email: User email
            
        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            connection = psycopg2.connect(conn_string)
            cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            
            query = """
                UPDATE users 
                SET joy_dollar = joy_dollar + %s, updated_at = NOW()
                WHERE email = %s
                RETURNING *
            """
            cursor.execute(query, (amount, email))
            result = cursor.fetchone()
            connection.commit()
            cursor.close()
            connection.close()
            
            if result:
                return (True, f"Successfully added {amount} JD to {email}")
            else:
                return (False, f"User not found: {email}")
        except Exception as e:
            return (False, str(e))
    
    @staticmethod
    def sub(conn_string, amount, identifier):
        """
        Subtract joy dollars from a user's account.
        
        Args:
            conn_string: Database connection string
            amount: Amount to subtract
            identifier: User email or ID
            
        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            connection = psycopg2.connect(conn_string)
            cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            
            query = """
                UPDATE users 
                SET joy_dollar = joy_dollar - %s, updated_at = NOW()
                WHERE email = %s OR id = %s
                RETURNING *
            """
            cursor.execute(query, (amount, identifier, identifier))
            result = cursor.fetchone()
            connection.commit()
            cursor.close()
            connection.close()
            
            if result:
                return (True, f"Successfully subtracted {amount} JD from {identifier}")
            else:
                return (False, f"User not found: {identifier}")
        except Exception as e:
            return (False, str(e))
    
    @staticmethod
    def set_socket_id(user_id, socket_id, conn):
        """
        Set socket_id for a user (alias for update_socket_id with different param order).
        
        Args:
            user_id: The user ID
            socket_id: The socket ID to set
            conn: Database connection
            
        Returns:
            Number of rows affected
        """
        cursor = conn.cursor()
        query = "UPDATE users SET socket_id = %s WHERE id = %s"
        cursor.execute(query, (socket_id, user_id))
        rows_affected = cursor.rowcount
        conn.commit()
        cursor.close()
        return rows_affected
    
    @staticmethod
    def find_by_email(email, conn):
        """
        Find user by email address.
        
        Args:
            email: Email address
            conn: Database connection
            
        Returns:
            User record as dictionary or None
        """
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "SELECT * FROM users WHERE email = %s"
        cursor.execute(query, (email,))
        result = cursor.fetchone()
        cursor.close()
        return result
    
    @staticmethod
    def create_for_google(email, name, google_id, picture, conn):
        """
        Create a new user from Google OAuth information.
        
        Args:
            email: User email from Google
            name: User name from Google
            google_id: Google user ID
            picture: Profile picture URL
            conn: Database connection
            
        Returns:
            Created user record as dictionary
        """
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        
        query = """
            INSERT INTO users (email, name, google_id, picture, joy_dollar, created_at, updated_at)
            VALUES (%s, %s, %s, %s, 0, NOW(), NOW())
            RETURNING *
        """
        cursor.execute(query, (email, name, google_id, picture))
        result = cursor.fetchone()
        conn.commit()
        cursor.close()
        
        return result
    
    def __init__(self, conn_string):
        """
        Initialize Member instance with database connection.
        
        Args:
            conn_string: PostgreSQL connection string
        """
        self.connection = psycopg2.connect(conn_string)
        self.cursor = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    
    @staticmethod
    def validate(member_body):
        """
        Validate member registration data.
        
        Args:
            member_body: Dictionary with member data
            
        Returns:
            Boolean indicating if validation passed
        """
        required_fields = ['email', 'password', 'name']
        return all(field in member_body for field in required_fields)
    
    def create(self, member_body):
        """
        Create a new member/user.
        
        Args:
            member_body: Dictionary with member data
            
        Returns:
            Tuple of (success: bool, error_code: str or None, error_message: str or None)
        """
        try:
            import hashlib
            import uuid
            
            email = member_body.get('email')
            password = member_body.get('password')
            name = member_body.get('name')
            phone = member_body.get('phone', '')
            
            # Check if email already exists
            self.cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
            if self.cursor.fetchone():
                return (False, "EMAILEXISTS", "Email already registered")
            
            # Hash password
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            
            # Generate activation token
            activation_token = str(uuid.uuid4())
            
            query = """
                INSERT INTO users (email, password, name, phone, activation_token, is_activate, joy_dollar, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, false, 0, NOW(), NOW())
                RETURNING *
            """
            self.cursor.execute(query, (email, password_hash, name, phone, activation_token))
            self.connection.commit()
            return (True, None, None)
        except Exception as e:
            return (False, "DBERROR", str(e))
    
    def search(self, search_body):
        """
        Search/update user information.
        
        Args:
            search_body: Dictionary with search/update criteria
            
        Returns:
            Tuple of (success: bool, user_data or error_message)
        """
        try:
            user_id = search_body.get('user_id')
            socket_id = search_body.get('socket_id')
            phone = search_body.get('phone')
            
            # Check if phone is being updated and if it's duplicate
            if phone:
                self.cursor.execute(
                    "SELECT id FROM users WHERE phone = %s AND id != %s",
                    (phone, user_id)
                )
                if self.cursor.fetchone():
                    return (False, "Phone number already in use")
            
            # Update user
            update_fields = []
            params = []
            
            if socket_id is not None:
                update_fields.append("socket_id = %s")
                params.append(socket_id)
            if phone is not None:
                update_fields.append("phone = %s")
                params.append(phone)
            
            if update_fields:
                update_fields.append("updated_at = NOW()")
                params.append(user_id)
                
                query = f"UPDATE users SET {', '.join(update_fields)} WHERE id = %s RETURNING *"
                self.cursor.execute(query, params)
                result = self.cursor.fetchone()
                self.connection.commit()
                return (True, dict(result))
            
            # Just fetch user if no updates
            self.cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
            result = self.cursor.fetchone()
            return (True, dict(result) if result else None)
        except Exception as e:
            return (False, str(e))
    
    def get_user(self, body_json):
        """
        Get user information.
        
        Args:
            body_json: Dictionary with user_id
            
        Returns:
            User record
        """
        user_id = body_json.get('user_id')
        self.cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        return self.cursor.fetchone()
    
    def get_user_profile_with_event(self, body_json):
        """
        Get user profile with associated events.
        
        Args:
            body_json: Dictionary with user_id and optional date filters
            
        Returns:
            User profile with events
        """
        user_id = body_json.get('user_id')
        profile_id = body_json.get('id')
        start_date = body_json.get('start_date')
        end_date = body_json.get('end_date')
        
        # Get user profile
        self.cursor.execute("SELECT * FROM users WHERE id = %s", (profile_id,))
        user = self.cursor.fetchone()
        
        if not user:
            return None
        
        # Get user events
        if start_date and end_date:
            self.cursor.execute("""
                SELECT * FROM calendars 
                WHERE user_id = %s AND event_date BETWEEN %s AND %s
                ORDER BY event_date DESC
            """, (profile_id, start_date, end_date))
        else:
            self.cursor.execute("""
                SELECT * FROM calendars 
                WHERE user_id = %s
                ORDER BY event_date DESC
                LIMIT 10
            """, (profile_id,))
        
        events = self.cursor.fetchall()
        
        return {
            **dict(user),
            'events': [dict(e) for e in events]
        }
