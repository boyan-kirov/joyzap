"""
Database operations for reports
"""
import psycopg2
import psycopg2.extras


class Report:
    """Helper class for report operations"""
    
    def __init__(self, conn_string):
        """
        Initialize the Report helper with a database connection.
        
        Args:
            conn_string: PostgreSQL connection string
        """
        self.connection = psycopg2.connect(conn_string)
        self.cursor = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    
    def create(self, title, description, event_id, reported_by, report_to):
        """
        Create a new report.
        
        Args:
            title: Report title
            description: Report description
            event_id: ID of the event being reported
            reported_by: User ID who created the report
            report_to: User ID being reported
            
        Returns:
            Created report record
        """
        query = """
            INSERT INTO reports (title, description, event_id, reported_by, report_to, status, created_at)
            VALUES (%s, %s, %s, %s, %s, 'pending', NOW())
            RETURNING *
        """
        self.cursor.execute(query, (title, description, event_id, reported_by, report_to))
        result = self.cursor.fetchone()
        self.connection.commit()
        return result
    
    def get_all(self, query_strings):
        """
        Get all reports with optional filtering.
        
        Args:
            query_strings: Dictionary with optional filter parameters
            
        Returns:
            List of report records
        """
        status = query_strings.get('status')
        
        if status:
            query = """
                SELECT 
                    r.*,
                    u_by.name as reported_by_name,
                    u_to.name as report_to_name
                FROM reports r
                LEFT JOIN users u_by ON r.reported_by = u_by.id
                LEFT JOIN users u_to ON r.report_to = u_to.id
                WHERE r.status = %s
                ORDER BY r.created_at DESC
            """
            self.cursor.execute(query, (status,))
        else:
            query = """
                SELECT 
                    r.*,
                    u_by.name as reported_by_name,
                    u_to.name as report_to_name
                FROM reports r
                LEFT JOIN users u_by ON r.reported_by = u_by.id
                LEFT JOIN users u_to ON r.report_to = u_to.id
                ORDER BY r.created_at DESC
            """
            self.cursor.execute(query)
        
        return self.cursor.fetchall()
    
    def update_status(self, report_id, status):
        """
        Update report status.
        
        Args:
            report_id: Report ID
            status: New status
            
        Returns:
            Updated report record
        """
        query = """
            UPDATE reports 
            SET status = %s, updated_at = NOW()
            WHERE id = %s
            RETURNING *
        """
        self.cursor.execute(query, (status, report_id))
        result = self.cursor.fetchone()
        self.connection.commit()
        return result
    
    def __del__(self):
        """Close cursor and connection when object is destroyed"""
        try:
            if hasattr(self, 'cursor') and self.cursor:
                self.cursor.close()
            if hasattr(self, 'connection') and self.connection:
                self.connection.close()
        except:
            pass
