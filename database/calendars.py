"""
Calendar database operations
"""
import psycopg2
from datetime import datetime


class Calendar:
    """Calendar event operations"""
    
    @staticmethod
    def create(user_id, calendar_dto, conn):
        """
        Create a new calendar event
        
        Args:
            user_id: User ID
            calendar_dto: CalendarBody DTO with event data
            conn: Database connection
            
        Returns:
            dict: Created event
        """
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO calendars (user_id, title, description, event_date, location, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, NOW(), NOW())
            RETURNING id, user_id, title, description, event_date, location, created_at, updated_at
        """, (
            user_id,
            calendar_dto.title,
            calendar_dto.description,
            calendar_dto.event_date,
            calendar_dto.location
        ))
        
        row = cursor.fetchone()
        conn.commit()
        cursor.close()
        
        return {
            "id": row[0],
            "user_id": row[1],
            "title": row[2],
            "description": row[3],
            "event_date": row[4].isoformat() if row[4] else None,
            "location": row[5],
            "created_at": row[6].isoformat() if row[6] else None,
            "updated_at": row[7].isoformat() if row[7] else None
        }
    
    @staticmethod
    def search(user_id, keyword, conn):
        """
        Search calendar events for a user
        
        Args:
            user_id: User ID
            keyword: Search keyword for title/description
            conn: Database connection
            
        Returns:
            list: List of events matching search
        """
        cursor = conn.cursor()
        
        if keyword:
            cursor.execute("""
                SELECT id, user_id, title, description, event_date, location, created_at, updated_at
                FROM calendars
                WHERE user_id = %s AND (title ILIKE %s OR description ILIKE %s)
                ORDER BY event_date DESC
            """, (user_id, f'%{keyword}%', f'%{keyword}%'))
        else:
            cursor.execute("""
                SELECT id, user_id, title, description, event_date, location, created_at, updated_at
                FROM calendars
                WHERE user_id = %s
                ORDER BY event_date DESC
            """, (user_id,))
        
        rows = cursor.fetchall()
        events = []
        
        for row in rows:
            events.append({
                "id": row[0],
                "user_id": row[1],
                "title": row[2],
                "description": row[3],
                "event_date": row[4].isoformat() if row[4] else None,
                "location": row[5],
                "created_at": row[6].isoformat() if row[6] else None,
                "updated_at": row[7].isoformat() if row[7] else None
            })
        
        cursor.close()
        return events
    
    @staticmethod
    def get_event_detail(event_id, user_id, conn):
        """
        Get detailed information about a specific event
        
        Args:
            event_id: Event ID
            user_id: User ID (for authorization)
            conn: Database connection
            
        Returns:
            dict: Event details
        """
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, user_id, title, description, event_date, location, created_at, updated_at
            FROM calendars
            WHERE id = %s AND user_id = %s
        """, (event_id, user_id))
        
        row = cursor.fetchone()
        cursor.close()
        
        if not row:
            return None
        
        return {
            "id": row[0],
            "user_id": row[1],
            "title": row[2],
            "description": row[3],
            "event_date": row[4].isoformat() if row[4] else None,
            "location": row[5],
            "created_at": row[6].isoformat() if row[6] else None,
            "updated_at": row[7].isoformat() if row[7] else None
        }
    
    @staticmethod
    def edit_event(event_id, user_id, calendar_dto, conn):
        """
        Update an existing calendar event
        
        Args:
            event_id: Event ID
            user_id: User ID (for authorization)
            calendar_dto: CalendarBody DTO with updated data
            conn: Database connection
            
        Returns:
            dict: Updated event
        """
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE calendars
            SET title = %s, description = %s, event_date = %s, location = %s, updated_at = NOW()
            WHERE id = %s AND user_id = %s
            RETURNING id, user_id, title, description, event_date, location, created_at, updated_at
        """, (
            calendar_dto.title,
            calendar_dto.description,
            calendar_dto.event_date,
            calendar_dto.location,
            event_id,
            user_id
        ))
        
        row = cursor.fetchone()
        conn.commit()
        cursor.close()
        
        if not row:
            return None
        
        return {
            "id": row[0],
            "user_id": row[1],
            "title": row[2],
            "description": row[3],
            "event_date": row[4].isoformat() if row[4] else None,
            "location": row[5],
            "created_at": row[6].isoformat() if row[6] else None,
            "updated_at": row[7].isoformat() if row[7] else None
        }
    
    @staticmethod
    def delete_event(event_id, user_id, conn):
        """
        Delete a calendar event
        
        Args:
            event_id: Event ID
            user_id: User ID (for authorization)
            conn: Database connection
            
        Returns:
            bool: True if deleted, False if not found
        """
        cursor = conn.cursor()
        
        cursor.execute("""
            DELETE FROM calendars
            WHERE id = %s AND user_id = %s
        """, (event_id, user_id))
        
        deleted = cursor.rowcount > 0
        conn.commit()
        cursor.close()
        
        return deleted
