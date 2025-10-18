"""
Database helper for payment operations
"""
import psycopg2
import psycopg2.extras
from datetime import datetime


class Payment:
    """Helper class for managing payments in the database"""
    
    def __init__(self, conn_string):
        """
        Initialize the Payment helper with a database connection.
        
        Args:
            conn_string: PostgreSQL connection string
        """
        self.connection = psycopg2.connect(conn_string)
        self.cursor = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    
    def add(self, amount, email, description, purchase_id=None):
        """
        Add a payment record (credit).
        
        Args:
            amount: Amount to add
            email: User email
            description: Payment description
            purchase_id: Optional purchase ID
            
        Returns:
            Created payment record
        """
        query = """
            INSERT INTO payments 
            (amount, email, description, purchase_id, transaction_type, created_at)
            VALUES (%s, %s, %s, %s, 'credit', %s)
            RETURNING *
        """
        
        self.cursor.execute(query, (
            amount,
            email,
            description,
            purchase_id,
            datetime.now()
        ))
        result = self.cursor.fetchone()
        self.connection.commit()
        return result
    
    def sub(self, amount, identifier):
        """
        Subtract a payment record (debit).
        
        Args:
            amount: Amount to subtract (should be negative)
            identifier: User email or ID
            
        Returns:
            Created payment record
        """
        query = """
            INSERT INTO payments 
            (amount, email, description, transaction_type, created_at)
            VALUES (%s, %s, %s, 'debit', %s)
            RETURNING *
        """
        
        description = f"Transfer out: {abs(amount)} JD"
        
        self.cursor.execute(query, (
            amount,
            identifier,
            description,
            datetime.now()
        ))
        result = self.cursor.fetchone()
        self.connection.commit()
        return result
    
    def get_by_email(self, email, limit=100):
        """
        Get payment records for a user by email.
        
        Args:
            email: User email
            limit: Maximum number of records to return
            
        Returns:
            List of payment records
        """
        query = """
            SELECT * FROM payments 
            WHERE email = %s 
            ORDER BY created_at DESC 
            LIMIT %s
        """
        self.cursor.execute(query, (email, limit))
        return self.cursor.fetchall()
    
    def get_total_by_email(self, email):
        """
        Get total payment amount for a user.
        
        Args:
            email: User email
            
        Returns:
            Total payment amount
        """
        query = """
            SELECT COALESCE(SUM(amount), 0) as total 
            FROM payments 
            WHERE email = %s
        """
        self.cursor.execute(query, (email,))
        result = self.cursor.fetchone()
        return result['total'] if result else 0
    
    def add(self, amount, email, description, purchase_id=None):
        """
        Add payment record.
        
        Args:
            amount: Payment amount
            email: User email
            description: Payment description
            purchase_id: Optional purchase ID
            
        Returns:
            Created payment record
        """
        query = """
            INSERT INTO payment (amount, email, description, purchase_id, status, created_at)
            VALUES (%s, %s, %s, %s, 'completed', NOW())
            RETURNING *
        """
        self.cursor.execute(query, (amount, email, description, purchase_id))
        result = self.cursor.fetchone()
        self.connection.commit()
        return result
    
    def sub(self, amount, identifier):
        """
        Subtract from payment (negative amount).
        
        Args:
            amount: Amount to subtract (can be negative)
            identifier: User identifier (email or ID)
            
        Returns:
            Created payment record
        """
        query = """
            INSERT INTO payment (amount, email, description, status, created_at)
            VALUES (%s, %s, 'Withdrawal', 'completed', NOW())
            RETURNING *
        """
        self.cursor.execute(query, (amount, identifier))
        result = self.cursor.fetchone()
        self.connection.commit()
        return result
    
    def get_payment(self, user_id):
        """
        Get payment history for user.
        
        Args:
            user_id: User ID
            
        Returns:
            List of payment records
        """
        query = """
            SELECT p.*, u.name as user_name, u.email
            FROM payment p
            LEFT JOIN users u ON p.from_user = u.id OR p.to_user = u.id
            WHERE p.from_user = %s OR p.to_user = %s
            ORDER BY p.created_at DESC
            LIMIT 50
        """
        self.cursor.execute(query, (user_id, user_id))
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
