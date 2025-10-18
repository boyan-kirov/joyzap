"""
Database helper for gift operations
"""
import psycopg2
import psycopg2.extras
from datetime import datetime


class Gift:
    """Helper class for managing gifts in the database"""
    
    def __init__(self, conn_string):
        """
        Initialize the Gift helper with a database connection.
        
        Args:
            conn_string: PostgreSQL connection string
        """
        self.connection = psycopg2.connect(conn_string)
        self.cursor = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    
    def get_gift_categories(self):
        """
        Get all gift categories.
        
        Returns:
            List of gift category records
        """
        query = """
            SELECT * FROM gift_categories 
            ORDER BY name
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def create_gift_item(self, gift_body):
        """
        Create a new gift item.
        
        Args:
            gift_body: GiftBody object containing gift data
            
        Returns:
            Created gift record
        """
        query = """
            INSERT INTO gifts 
            (name, description, category_id, price, image_url, stock_quantity, is_active, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING *
        """
        
        now = datetime.now()
        self.cursor.execute(query, (
            gift_body.name,
            gift_body.description,
            gift_body.category_id,
            gift_body.price,
            gift_body.image_url,
            getattr(gift_body, 'stock_quantity', 0),
            getattr(gift_body, 'is_active', True),
            now,
            now
        ))
        result = self.cursor.fetchone()
        self.connection.commit()
        return result
    
    def update_gift_item(self, data):
        """
        Update a gift item.
        
        Args:
            data: Dictionary containing gift update data (must include 'id')
            
        Returns:
            Updated gift record
        """
        gift_id = data.get("id")
        
        # Build update query dynamically
        update_fields = []
        update_values = []
        
        if "name" in data:
            update_fields.append("name = %s")
            update_values.append(data["name"])
        
        if "description" in data:
            update_fields.append("description = %s")
            update_values.append(data["description"])
        
        if "category_id" in data:
            update_fields.append("category_id = %s")
            update_values.append(data["category_id"])
        
        if "price" in data:
            update_fields.append("price = %s")
            update_values.append(data["price"])
        
        if "image_url" in data:
            update_fields.append("image_url = %s")
            update_values.append(data["image_url"])
        
        if "stock_quantity" in data:
            update_fields.append("stock_quantity = %s")
            update_values.append(data["stock_quantity"])
        
        if "is_active" in data:
            update_fields.append("is_active = %s")
            update_values.append(data["is_active"])
        
        # Always update updated_at
        update_fields.append("updated_at = %s")
        update_values.append(datetime.now())
        
        # Add WHERE clause parameter
        update_values.append(gift_id)
        
        query = f"""
            UPDATE gifts 
            SET {', '.join(update_fields)}
            WHERE id = %s
            RETURNING *
        """
        
        self.cursor.execute(query, update_values)
        result = self.cursor.fetchone()
        self.connection.commit()
        return result
    
    def multiple_update(self, ids, update_type):
        """
        Perform bulk update on multiple gifts.
        
        Args:
            ids: List of gift IDs
            update_type: Type of update to perform
            
        Returns:
            True if successful, False otherwise
        """
        if not ids or not update_type:
            return False
        
        # Handle different update types
        if update_type == "activate":
            query = """
                UPDATE gifts 
                SET is_active = TRUE, updated_at = %s
                WHERE id = ANY(%s)
            """
        elif update_type == "deactivate":
            query = """
                UPDATE gifts 
                SET is_active = FALSE, updated_at = %s
                WHERE id = ANY(%s)
            """
        elif update_type == "delete":
            query = """
                DELETE FROM gifts 
                WHERE id = ANY(%s)
            """
            self.cursor.execute(query, (ids,))
            self.connection.commit()
            return True
        else:
            return False
        
        self.cursor.execute(query, (datetime.now(), ids))
        self.connection.commit()
        return True
    
    def get_gift_by_id(self, gift_id):
        """
        Get a gift by ID.
        
        Args:
            gift_id: Gift ID
            
        Returns:
            Gift record or None
        """
        query = """
            SELECT g.*, gc.name as category_name 
            FROM gifts g
            LEFT JOIN gift_categories gc ON g.category_id = gc.id
            WHERE g.id = %s
        """
        self.cursor.execute(query, (gift_id,))
        return self.cursor.fetchone()
    
    def get_all_gifts(self, category_id=None, is_active=None):
        """
        Get all gifts with optional filters.
        
        Args:
            category_id: Optional category filter
            is_active: Optional active status filter
            
        Returns:
            List of gift records
        """
        conditions = []
        params = []
        
        if category_id is not None:
            conditions.append("g.category_id = %s")
            params.append(category_id)
        
        if is_active is not None:
            conditions.append("g.is_active = %s")
            params.append(is_active)
        
        where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""
        
        query = f"""
            SELECT g.*, gc.name as category_name 
            FROM gifts g
            LEFT JOIN gift_categories gc ON g.category_id = gc.id
            {where_clause}
            ORDER BY g.created_at DESC
        """
        
        self.cursor.execute(query, params)
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
