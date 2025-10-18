"""
Database helper for payment history operations
"""
import psycopg2
import psycopg2.extras
from datetime import datetime


class PaymentHistory:
    """Helper class for managing payment history in the database"""
    
    def __init__(self, conn_string):
        """
        Initialize the PaymentHistory helper with a database connection.
        
        Args:
            conn_string: PostgreSQL connection string
        """
        self.connection = psycopg2.connect(conn_string)
        self.cursor = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    
    def create(self, transaction_type, amount, user_id, email, description=None, metadata=None):
        """
        Create a new payment history record.
        
        Args:
            transaction_type: Type of transaction (e.g., 'check_in', 'purchase', 'refund')
            amount: Amount of transaction
            user_id: User ID (can be None)
            email: User email
            description: Optional description
            metadata: Optional metadata (JSON)
            
        Returns:
            Created payment history record
        """
        query = """
            INSERT INTO payment_history 
            (transaction_type, amount, user_id, email, description, metadata, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING *
        """
        
        self.cursor.execute(query, (
            transaction_type,
            amount,
            user_id,
            email,
            description,
            metadata,
            datetime.now()
        ))
        result = self.cursor.fetchone()
        self.connection.commit()
        return result
    
    def get_by_email(self, email, limit=100):
        """
        Get payment history for a user by email.
        
        Args:
            email: User email
            limit: Maximum number of records to return
            
        Returns:
            List of payment history records
        """
        query = """
            SELECT * FROM payment_history 
            WHERE email = %s 
            ORDER BY created_at DESC 
            LIMIT %s
        """
        self.cursor.execute(query, (email, limit))
        return self.cursor.fetchall()
    
    def get_by_user_id(self, user_id, limit=100):
        """
        Get payment history for a user by user ID.
        
        Args:
            user_id: User ID
            limit: Maximum number of records to return
            
        Returns:
            List of payment history records
        """
        query = """
            SELECT * FROM payment_history 
            WHERE user_id = %s 
            ORDER BY created_at DESC 
            LIMIT %s
        """
        self.cursor.execute(query, (user_id, limit))
        return self.cursor.fetchall()
    
    def get_by_type(self, transaction_type, limit=100):
        """
        Get payment history by transaction type.
        
        Args:
            transaction_type: Type of transaction
            limit: Maximum number of records to return
            
        Returns:
            List of payment history records
        """
        query = """
            SELECT * FROM payment_history 
            WHERE transaction_type = %s 
            ORDER BY created_at DESC 
            LIMIT %s
        """
        self.cursor.execute(query, (transaction_type, limit))
        return self.cursor.fetchall()
    
    def get_pending_balance(self, user_id):
        """
        Get pending balance for a user.
        
        Args:
            user_id: User ID
            
        Returns:
            Pending balance information
        """
        query = """
            SELECT 
                COALESCE(SUM(CASE WHEN status = 'pending' THEN amount ELSE 0 END), 0) as pending_balance,
                COALESCE(SUM(CASE WHEN status = 'completed' THEN amount ELSE 0 END), 0) as completed_balance,
                COUNT(*) as total_transactions
            FROM payment_history 
            WHERE user_id = %s
        """
        self.cursor.execute(query, (user_id,))
        return self.cursor.fetchone()
    
    def update_deposited_money(self):
        """
        Update deposited money status for completed transactions.
        
        Returns:
            Number of rows affected
        """
        query = """
            UPDATE payment_history 
            SET status = 'deposited', updated_at = NOW()
            WHERE status = 'completed' AND updated_at < NOW() - INTERVAL '24 hours'
        """
        self.cursor.execute(query)
        rows_affected = self.cursor.rowcount
        self.connection.commit()
        return rows_affected
    
    def __del__(self):
        """Close cursor and connection when object is destroyed"""
        try:
            if hasattr(self, 'cursor') and self.cursor:
                self.cursor.close()
            if hasattr(self, 'connection') and self.connection:
                self.connection.close()
        except:
            pass
