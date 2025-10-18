"""
Database operations for joyzaps (presents, cards, time capsules)
"""
import psycopg2
import psycopg2.extras
from datetime import datetime


class Joyzap:
    """Helper class for joyzap operations"""
    
    def __init__(self, conn_string):
        """
        Initialize the Joyzap helper with a database connection.
        
        Args:
            conn_string: PostgreSQL connection string
        """
        self.connection = psycopg2.connect(conn_string)
        self.cursor = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    
    def add_present(self, sender_id, receiver_id, present_body):
        """Add a present from sender to receiver"""
        try:
            query = """
                INSERT INTO joyzaps (sender_id, receiver_id, type, title, message, gift_id, amount, created_at)
                VALUES (%s, %s, 'present', %s, %s, %s, %s, NOW())
                RETURNING *
            """
            self.cursor.execute(query, (
                sender_id, receiver_id, present_body.title, present_body.message,
                present_body.gift_id, present_body.amount
            ))
            result = self.cursor.fetchone()
            self.connection.commit()
            return (True, dict(result))
        except Exception as e:
            return (False, str(e))
    
    def add_card(self, sender_id, receiver_id, card_body):
        """Add a card from sender to receiver"""
        try:
            query = """
                INSERT INTO joyzaps (sender_id, receiver_id, type, title, message, card_design, created_at)
                VALUES (%s, %s, 'card', %s, %s, %s, NOW())
                RETURNING *
            """
            self.cursor.execute(query, (
                sender_id, receiver_id, card_body.title, card_body.message, card_body.design
            ))
            result = self.cursor.fetchone()
            self.connection.commit()
            return (True, dict(result))
        except Exception as e:
            return (False, str(e))
    
    def add_timecapsule(self, sender_id, receiver_id, timecapsule_body):
        """Add a time capsule from sender to receiver"""
        try:
            query = """
                INSERT INTO joyzaps (sender_id, receiver_id, type, title, message, unlock_date, created_at)
                VALUES (%s, %s, 'timecapsule', %s, %s, %s, NOW())
                RETURNING *
            """
            self.cursor.execute(query, (
                sender_id, receiver_id, timecapsule_body.title, 
                timecapsule_body.message, timecapsule_body.unlock_date
            ))
            result = self.cursor.fetchone()
            self.connection.commit()
            return (True, dict(result))
        except Exception as e:
            return (False, str(e))
    
    def add_present_without_user(self, sender_id, present_body):
        """Add a present without specified receiver"""
        try:
            query = """
                INSERT INTO joyzaps (sender_id, type, title, message, gift_id, amount, receiver_email, receiver_phone, created_at)
                VALUES (%s, 'present', %s, %s, %s, %s, %s, %s, NOW())
                RETURNING *
            """
            self.cursor.execute(query, (
                sender_id, present_body.title, present_body.message,
                present_body.gift_id, present_body.amount,
                getattr(present_body, 'receiver_email', None),
                getattr(present_body, 'receiver_phone', None)
            ))
            result = self.cursor.fetchone()
            self.connection.commit()
            return (True, dict(result))
        except Exception as e:
            return (False, str(e))
    
    def add_card_without_user(self, sender_id, card_body):
        """Add a card without specified receiver"""
        try:
            query = """
                INSERT INTO joyzaps (sender_id, type, title, message, card_design, receiver_email, receiver_phone, created_at)
                VALUES (%s, 'card', %s, %s, %s, %s, %s, NOW())
                RETURNING *
            """
            self.cursor.execute(query, (
                sender_id, card_body.title, card_body.message, card_body.design,
                getattr(card_body, 'receiver_email', None),
                getattr(card_body, 'receiver_phone', None)
            ))
            result = self.cursor.fetchone()
            self.connection.commit()
            return (True, dict(result))
        except Exception as e:
            return (False, str(e))
    
    def add_timecapsule_without_user(self, sender_id, timecapsule_body):
        """Add a time capsule without specified receiver"""
        try:
            query = """
                INSERT INTO joyzaps (sender_id, type, title, message, unlock_date, receiver_email, receiver_phone, created_at)
                VALUES (%s, 'timecapsule', %s, %s, %s, %s, %s, NOW())
                RETURNING *
            """
            self.cursor.execute(query, (
                sender_id, timecapsule_body.title, timecapsule_body.message,
                timecapsule_body.unlock_date,
                getattr(timecapsule_body, 'receiver_email', None),
                getattr(timecapsule_body, 'receiver_phone', None)
            ))
            result = self.cursor.fetchone()
            self.connection.commit()
            return (True, dict(result))
        except Exception as e:
            return (False, str(e))
    
    def _add_mistory_present(self, sender_id, present_body):
        """Add a mystery present"""
        return self.add_present_without_user(sender_id, present_body)
    
    def _add_mistory_card(self, sender_id, card_body):
        """Add a mystery card"""
        return self.add_card_without_user(sender_id, card_body)
    
    def _add_mistory_timecapsule(self, sender_id, timecapsule_body):
        """Add a mystery time capsule"""
        return self.add_timecapsule_without_user(sender_id, timecapsule_body)
    
    def get_card(self, card_id):
        """Get card by ID"""
        query = "SELECT * FROM joyzaps WHERE id = %s AND type = 'card'"
        self.cursor.execute(query, (card_id,))
        return self.cursor.fetchone()
    
    def get_present(self, present_id):
        """Get present by ID"""
        query = "SELECT * FROM joyzaps WHERE id = %s AND type = 'present'"
        self.cursor.execute(query, (present_id,))
        return self.cursor.fetchone()
    
    def get_timecap(self, timecap_id):
        """Get time capsule by ID"""
        query = "SELECT * FROM joyzaps WHERE id = %s AND type = 'timecapsule'"
        self.cursor.execute(query, (timecap_id,))
        return self.cursor.fetchone()
    
    def get_random_zap_person(self, query_params):
        """Get random person for zapping"""
        query = """
            SELECT id, name, email, picture 
            FROM users 
            WHERE id != %s
            ORDER BY RANDOM() 
            LIMIT 1
        """
        user_id = query_params.get('user_id')
        self.cursor.execute(query, (user_id,))
        return self.cursor.fetchone()
    
    def find_zap_user(self, phone, email):
        """Find user by phone or email"""
        email_data = None
        number_data = None
        
        if email:
            self.cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            email_data = self.cursor.fetchone()
        
        if phone:
            self.cursor.execute("SELECT * FROM users WHERE phone = %s", (phone,))
            number_data = self.cursor.fetchone()
        
        return email_data, number_data
    
    def collected_data(self, query_params):
        """Get collected joyzaps for user"""
        user_id = query_params.get('user_id')
        
        # Get presents
        self.cursor.execute("""
            SELECT * FROM joyzaps 
            WHERE receiver_id = %s AND type = 'present'
            ORDER BY created_at DESC
        """, (user_id,))
        presents = self.cursor.fetchall()
        
        # Get cards
        self.cursor.execute("""
            SELECT * FROM joyzaps 
            WHERE receiver_id = %s AND type = 'card'
            ORDER BY created_at DESC
        """, (user_id,))
        cards = self.cursor.fetchall()
        
        # Get time capsules
        self.cursor.execute("""
            SELECT * FROM joyzaps 
            WHERE receiver_id = %s AND type = 'timecapsule'
            ORDER BY created_at DESC
        """, (user_id,))
        capsules = self.cursor.fetchall()
        
        return presents, cards, capsules
    
    def collect_time_camp(self):
        """Collect expired time capsules"""
        query = """
            UPDATE joyzaps 
            SET is_collected = true 
            WHERE type = 'timecapsule' 
            AND unlock_date <= NOW() 
            AND is_collected = false
            AND receiver_id IS NOT NULL
            RETURNING *
        """
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        self.connection.commit()
        return results
    
    def collect_time_camp_without_user(self):
        """Collect expired time capsules without specified receiver"""
        query = """
            UPDATE joyzaps 
            SET is_collected = true 
            WHERE type = 'timecapsule' 
            AND unlock_date <= NOW() 
            AND is_collected = false
            AND receiver_id IS NULL
            RETURNING *
        """
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        self.connection.commit()
        return results
    
    def __del__(self):
        """Close cursor and connection when object is destroyed"""
        try:
            if hasattr(self, 'cursor') and self.cursor:
                self.cursor.close()
            if hasattr(self, 'connection') and self.connection:
                self.connection.close()
        except:
            pass
