"""
Database operations for parameters and system configuration
"""
import psycopg2
import psycopg2.extras


class Parameters:
    """Helper class for system parameters and configuration"""
    
    def __init__(self, conn_string):
        """
        Initialize the Parameters helper with a database connection.
        
        Args:
            conn_string: PostgreSQL connection string
        """
        self.connection = psycopg2.connect(conn_string)
        self.cursor = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    
    def get_gift_items_by_category(self):
        """
        Get all gift items grouped by category.
        
        Returns:
            List of gift items with categories
        """
        query = """
            SELECT 
                g.id,
                g.name,
                g.description,
                g.price,
                g.image_url,
                g.category_id,
                gc.name as category_name
            FROM gifts g
            LEFT JOIN gift_categories gc ON g.category_id = gc.id
            ORDER BY gc.name, g.name
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def delete_gift_items(self, path_parameters):
        """
        Delete a gift item.
        
        Args:
            path_parameters: Dictionary containing 'id' of gift to delete
            
        Returns:
            Number of rows affected
        """
        gift_id = path_parameters.get('id')
        query = "DELETE FROM gifts WHERE id = %s"
        self.cursor.execute(query, (gift_id,))
        rows_affected = self.cursor.rowcount
        self.connection.commit()
        return rows_affected
    
    def update_gift_category(self, path_parameters):
        """
        Update a gift category.
        
        Args:
            path_parameters: Dictionary with category update data
            
        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            category_id = path_parameters.get('id')
            name = path_parameters.get('name')
            description = path_parameters.get('description', '')
            
            query = """
                UPDATE gift_categories 
                SET name = %s, description = %s, updated_at = NOW()
                WHERE id = %s
                RETURNING *
            """
            self.cursor.execute(query, (name, description, category_id))
            result = self.cursor.fetchone()
            self.connection.commit()
            
            if result:
                return (True, "Category updated successfully")
            else:
                return (False, "Category not found")
        except Exception as e:
            return (False, str(e))
    
    def payroll_joydollar(self):
        """
        Get joy dollar payroll information.
        
        Returns:
            List of payroll records
        """
        query = """
            SELECT 
                u.id,
                u.name,
                u.email,
                u.joy_dollar,
                COUNT(p.id) as transaction_count,
                SUM(p.amount) as total_amount
            FROM users u
            LEFT JOIN payment p ON u.id = p.from_user OR u.id = p.to_user
            GROUP BY u.id, u.name, u.email, u.joy_dollar
            ORDER BY u.name
        """
        self.cursor.execute(query)
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
