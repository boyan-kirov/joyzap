import jwt
import os
from datetime import datetime, timedelta


class AuthorizationError(Exception):
    """Custom exception for authorization errors"""
    def __init__(self, message, status_code=401):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class JWT:
    """JWT authentication helper for Lambda functions"""
    
    def __init__(self, secret):
        self.secret = secret
    
    def auth(self, event):
        """
        Authenticate a request using JWT token from headers.
        
        Args:
            event: Lambda event object containing headers
            
        Raises:
            AuthorizationError: If authentication fails
        """
        try:
            # Get authorization header
            headers = event.get('headers', {})
            
            # Handle case-insensitive headers
            auth_header = None
            for key, value in headers.items():
                if key.lower() == 'authorization':
                    auth_header = value
                    break
            
            if not auth_header:
                raise AuthorizationError("No authorization header provided", 401)
            
            # Extract token from "Bearer <token>" format
            parts = auth_header.split()
            if len(parts) != 2 or parts[0].lower() != 'bearer':
                raise AuthorizationError("Invalid authorization header format", 401)
            
            token = parts[1]
            
            # Decode and verify token
            decoded = jwt.decode(token, self.secret, algorithms=['HS256'])
            
            # Store decoded token in event for use by handler
            event['decoded_token'] = decoded
            
            return decoded
            
        except jwt.ExpiredSignatureError:
            raise AuthorizationError("Token has expired", 401)
        except jwt.InvalidTokenError as e:
            raise AuthorizationError(f"Invalid token: {str(e)}", 401)
        except Exception as e:
            raise AuthorizationError(f"Authentication failed: {str(e)}", 401)
    
    def generate_token(self, payload, expires_in_hours=24):
        """
        Generate a JWT token.
        
        Args:
            payload: Dictionary containing token claims
            expires_in_hours: Token expiration time in hours
            
        Returns:
            Encoded JWT token string
        """
        payload['exp'] = datetime.utcnow() + timedelta(hours=expires_in_hours)
        payload['iat'] = datetime.utcnow()
        
        return jwt.encode(payload, self.secret, algorithm='HS256')
    
    def encode(self, payload, expires_in_hours=24):
        """
        Alias for generate_token for backward compatibility.
        
        Args:
            payload: Dictionary containing token claims
            expires_in_hours: Token expiration time in hours
            
        Returns:
            Encoded JWT token string
        """
        return self.generate_token(payload, expires_in_hours)
