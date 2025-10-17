import json


class Response:
    """Helper class for creating standardized Lambda responses"""
    
    @staticmethod
    def ok(data, status_code=200):
        """
        Create a successful response.
        
        Args:
            data: Response data (will be JSON serialized)
            status_code: HTTP status code (default: 200)
            
        Returns:
            Lambda response object
        """
        return {
            'statusCode': status_code,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
                'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS'
            },
            'body': json.dumps({
                'success': True,
                'data': data
            }, default=str)
        }
    
    @staticmethod
    def error(status_code, error, message="An error occurred"):
        """
        Create an error response.
        
        Args:
            status_code: HTTP status code
            error: Error details
            message: Error message
            
        Returns:
            Lambda response object
        """
        return {
            'statusCode': status_code,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
                'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS'
            },
            'body': json.dumps({
                'success': False,
                'message': message,
                'error': str(error)
            })
        }
    
    @staticmethod
    def created(data, status_code=201):
        """Create a resource created response"""
        return Response.ok(data, status_code)
    
    @staticmethod
    def no_content():
        """Create a no content response"""
        return {
            'statusCode': 204,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
                'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS'
            },
            'body': ''
        }
