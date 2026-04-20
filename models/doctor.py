
from database.db_connection import get_connection

class Doctor:
    @staticmethod
    def add(first_name, last_name, speciality, phone, email):
        conn = get_connection()
        if not conn: return False
        try:
            cursor = conn.cursor()
            query = """INSERT INTO doctors (first_name, last_name, speciality, phone, email) 
                       VALUES (%s, %s, %s, %s, %s)"""
            cursor.execute(query, (first_name, last_name, speciality, phone, email))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error adding doctor: {e}")
            return False
        finally:
            if 'cursor' in locals(): cursor.close()
            if 'conn' in locals() and conn.is_connected(): conn.close()

    @staticmethod
    def get_all():
        conn = get_connection()
        if not conn: return []
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM doctors ORDER BY id DESC")
            return cursor.fetchall()
        except Exception as e:
            print(f"Error fetching doctors: {e}")
            return []
        finally:
            if 'cursor' in locals(): cursor.close()
            if 'conn' in locals() and conn.is_connected(): conn.close()

    @staticmethod
    def update(doctor_id, first_name, last_name, speciality, phone, email):
        conn = get_connection()
        if not conn: return False
        try:
            cursor = conn.cursor()
            query = """UPDATE doctors SET first_name=%s, last_name=%s, speciality=%s, 
                       phone=%s, email=%s WHERE id=%s"""
            cursor.execute(query, (first_name, last_name, speciality, phone, email, doctor_id))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error updating doctor: {e}")
            return False
        finally:
            if 'cursor' in locals(): cursor.close()
            if 'conn' in locals() and conn.is_connected(): conn.close()

    @staticmethod
    def delete(doctor_id):
        conn = get_connection()
        if not conn: return False
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM doctors WHERE id=%s", (doctor_id,))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error deleting doctor: {e}")
            return False
        finally:
            if 'cursor' in locals(): cursor.close()
            if 'conn' in locals() and conn.is_connected(): conn.close()

    @staticmethod
    def search(keyword):
        conn = get_connection()
        if not conn: return []
        try:
            cursor = conn.cursor(dictionary=True)
            search_pattern = f"%{keyword}%"
            query = """SELECT * FROM doctors WHERE 
                       first_name LIKE %s OR last_name LIKE %s OR 
                       speciality LIKE %s OR phone LIKE %s OR email LIKE %s"""
            cursor.execute(query, (search_pattern, search_pattern, search_pattern, search_pattern, search_pattern))
            return cursor.fetchall()
        except Exception as e:
            print(f"Error searching doctors: {e}")
            return []
        finally:
            if 'cursor' in locals(): cursor.close()
            if 'conn' in locals() and conn.is_connected(): conn.close()

    @staticmethod
    def get_count():
        conn = get_connection()
        if not conn: return 0
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM doctors")
            return cursor.fetchone()[0]
        except Exception as e:
            print(f"Error counting doctors: {e}")
            return 0
        finally:
            if 'cursor' in locals(): cursor.close()
            if 'conn' in locals() and conn.is_connected(): conn.close()
