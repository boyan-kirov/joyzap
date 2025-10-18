"""
Database operations for login and authentication
"""
import psycopg2
import psycopg2.extras
import hashlib
import uuid
from datetime import datetime, timedelta


class Login:
    """Helper class for login and authentication operations"""
    
    def __init__(self, conn_string):
        """
        Initialize the Login helper with a database connection.
        
        Args:
            conn_string: PostgreSQL connection string
        """
        self.connection = psycopg2.connect(conn_string)
        self.cursor = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    
    @staticmethod
    def validate(login_body):
        """
        Validate login credentials.
        
        Args:
            login_body: Dictionary with 'email' and 'password'
            
        Returns:
            Boolean indicating if validation passed
        """
        return 'email' in login_body and 'password' in login_body
    
    def login(self, login_body):
        """
        Authenticate user login.
        
        Args:
            login_body: Dictionary with 'email' and 'password'
            
        Returns:
            Tuple of (success: bool, user_data: dict or None)
        """
        email = login_body.get('email')
        password = login_body.get('password')
        
        # Hash password (assuming you use SHA256 or similar)
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        query = """
            SELECT * FROM users 
            WHERE email = %s AND password = %s
        """
        self.cursor.execute(query, (email, password_hash))
        user = self.cursor.fetchone()
        
        if user:
            return (True, dict(user))
        else:
            return (False, None)
    
    def activate(self, activation_token):
        """
        Activate a user account with activation token.
        
        Args:
            activation_token: Activation token string
            
        Returns:
            Tuple of (success: bool, user_data: dict or None)
        """
        query = """
            UPDATE users 
            SET is_activate = true, updated_at = NOW()
            WHERE activation_token = %s
            RETURNING *
        """
        self.cursor.execute(query, (activation_token,))
        user = self.cursor.fetchone()
        self.connection.commit()
        
        if user:
            return (True, dict(user))
        else:
            return (False, None)
    
    def reset_token_generate(self, email):
        """
        Generate password reset token for email.
        
        Args:
            email: User email address
            
        Returns:
            Tuple of (success: bool, message: str)
        """
        reset_token = str(uuid.uuid4())
        expiry = datetime.now() + timedelta(hours=24)
        
        query = """
            UPDATE users 
            SET reset_token = %s, reset_token_expiry = %s, updated_at = NOW()
            WHERE email = %s
            RETURNING id
        """
        self.cursor.execute(query, (reset_token, expiry, email))
        result = self.cursor.fetchone()
        self.connection.commit()
        
        if result:
            return (True, reset_token)
        else:
            return (False, "User not found")
    
    def reset_password(self, path_parameters):
        """
        Reset user password with token.
        
        Args:
            path_parameters: Dictionary with 'id', 'reset_token', and 'password'
            
        Returns:
            Boolean indicating success
        """
        user_id = path_parameters.get('id')
        reset_token = path_parameters.get('reset_token')
        password = path_parameters.get('password')
        
        # Hash the new password
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        query = """
            UPDATE users 
            SET password = %s, reset_token = NULL, reset_token_expiry = NULL, updated_at = NOW()
            WHERE id = %s AND reset_token = %s AND reset_token_expiry > NOW()
            RETURNING id
        """
        self.cursor.execute(query, (password_hash, user_id, reset_token))
        result = self.cursor.fetchone()
        self.connection.commit()
        
        return result is not None
    
    def takeover_token_generate(self, contact):
        """
        Generate takeover token for contact (phone or email).
        
        Args:
            contact: User contact (phone or email)
            
        Returns:
            Tuple of (success: bool, token: str or error message)
        """
        takeover_token = str(uuid.uuid4())
        expiry = datetime.now() + timedelta(hours=24)
        
        query = """
            UPDATE users 
            SET takeover_token = %s, takeover_token_expiry = %s, updated_at = NOW()
            WHERE email = %s OR phone = %s
            RETURNING id
        """
        self.cursor.execute(query, (takeover_token, expiry, contact, contact))
        result = self.cursor.fetchone()
        self.connection.commit()
        
        if result:
            return (True, takeover_token)
        else:
            return (False, "Contact not found")
    
    def takeover_reset_password(self, body):
        """
        Reset password using takeover token.
        
        Args:
            body: Dictionary with 'takeover_token' and 'password'
            
        Returns:
            Boolean indicating success
        """
        takeover_token = body.get('takeover_token')
        password = body.get('password')
        
        # Hash the new password
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        query = """
            UPDATE users 
            SET password = %s, takeover_token = NULL, takeover_token_expiry = NULL, updated_at = NOW()
            WHERE takeover_token = %s AND takeover_token_expiry > NOW()
            RETURNING id
        """
        self.cursor.execute(query, (password_hash, takeover_token))
        result = self.cursor.fetchone()
        self.connection.commit()
        
        return result is not None
    
    def __del__(self):
        """Close cursor and connection when object is destroyed"""
        try:
            if hasattr(self, 'cursor') and self.cursor:
                self.cursor.close()
            if hasattr(self, 'connection') and self.connection:
                self.connection.close()
        except:
            pass
