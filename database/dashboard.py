"""
Dashboard database operations for statistics
"""
import psycopg2
import os


class Dashboard:
    """Dashboard statistics operations"""
    
    @staticmethod
    def get_statistics(user_id):
        """
        Get dashboard statistics for a user
        
        Args:
            user_id: User ID
            
        Returns:
            dict: Dashboard statistics
        """
        conn = psycopg2.connect(
            host=os.environ["db_host"],
            port=os.environ["db_port"],
            dbname=os.environ["db_name"],
            user=os.environ["db_user"],
            password=os.environ["db_password"]
        )
        
        cursor = conn.cursor()
        
        # Get friends count
        cursor.execute("""
            SELECT COUNT(*) FROM relations 
            WHERE (from_user = %s OR to_user = %s) AND status = 'accepted'
        """, (user_id, user_id))
        friends_count = cursor.fetchone()[0]
        
        # Get notifications count
        cursor.execute("""
            SELECT COUNT(*) FROM notification 
            WHERE user_id = %s AND is_read = false
        """, (user_id,))
        notifications_count = cursor.fetchone()[0]
        
        # Get gifts sent count
        cursor.execute("""
            SELECT COUNT(*) FROM payment 
            WHERE from_user = %s
        """, (user_id,))
        gifts_sent = cursor.fetchone()[0]
        
        # Get gifts received count
        cursor.execute("""
            SELECT COUNT(*) FROM payment 
            WHERE to_user = %s
        """, (user_id,))
        gifts_received = cursor.fetchone()[0]
        
        # Get joy dollars balance
        cursor.execute("""
            SELECT joy_dollar FROM users 
            WHERE id = %s
        """, (user_id,))
        result = cursor.fetchone()
        joy_dollar = result[0] if result else 0
        
        cursor.close()
        conn.close()
        
        return {
            "friends_count": friends_count,
            "notifications_count": notifications_count,
            "gifts_sent": gifts_sent,
            "gifts_received": gifts_received,
            "joy_dollar": joy_dollar
        }
    
    @staticmethod
    def get_trascation_statistics(user_id):
        """
        Get transaction statistics for a user
        
        Args:
            user_id: User ID
            
        Returns:
            list: Transaction history
        """
        conn = psycopg2.connect(
            host=os.environ["db_host"],
            port=os.environ["db_port"],
            dbname=os.environ["db_name"],
            user=os.environ["db_user"],
            password=os.environ["db_password"]
        )
        
        cursor = conn.cursor()
        
        # Get transaction history
        cursor.execute("""
            SELECT 
                ph.id,
                ph.payment_id,
                ph.action,
                ph.amount,
                ph.created_at,
                p.from_user,
                p.to_user,
                u_from.name as from_user_name,
                u_to.name as to_user_name
            FROM payment_history ph
            LEFT JOIN payment p ON ph.payment_id = p.id
            LEFT JOIN users u_from ON p.from_user = u_from.id
            LEFT JOIN users u_to ON p.to_user = u_to.id
            WHERE ph.user_id = %s
            ORDER BY ph.created_at DESC
            LIMIT 50
        """, (user_id,))
        
        rows = cursor.fetchall()
        transactions = []
        
        for row in rows:
            transactions.append({
                "id": row[0],
                "payment_id": row[1],
                "action": row[2],
                "amount": float(row[3]) if row[3] else 0,
                "created_at": row[4].isoformat() if row[4] else None,
                "from_user": row[5],
                "to_user": row[6],
                "from_user_name": row[7],
                "to_user_name": row[8]
            })
        
        cursor.close()
        conn.close()
        
        return transactions
