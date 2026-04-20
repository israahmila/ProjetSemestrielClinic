
from database.db_connection import get_connection
import hashlib

class User:
    @staticmethod
    def authenticate(username, password):
        
        conn = get_connection()
        if not conn: return {"error": "DB_DOWN"}
        try:
            cursor = conn.cursor(dictionary=True)
            hashed_pw = hashlib.sha256(password.encode()).hexdigest()
            query = "SELECT id, username, role FROM users WHERE username=%s AND password_hash=%s"
            cursor.execute(query, (username, hashed_pw))
            return cursor.fetchone()
        except Exception as e:
            print(f"Error authenticating user: {e}")
            return None
        finally:
            if 'cursor' in locals(): cursor.close()
            if 'conn' in locals() and conn.is_connected(): conn.close()
