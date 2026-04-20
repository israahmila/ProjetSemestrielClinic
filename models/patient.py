
from database.db_connection import get_connection

class Patient:
    @staticmethod
    def add(first_name, last_name, dob, phone, email, gender):
        conn = get_connection()
        if not conn: return False
        try:
            cursor = conn.cursor()
            query = """INSERT INTO patients (first_name, last_name, dob, phone, email, gender) 
                       VALUES (%s, %s, %s, %s, %s, %s)"""
            cursor.execute(query, (first_name, last_name, dob, phone, email, gender))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error adding patient: {e}")
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
            cursor.execute("SELECT * FROM patients ORDER BY id DESC")
            return cursor.fetchall()
        except Exception as e:
            print(f"Error fetching patients: {e}")
            return []
        finally:
            if 'cursor' in locals(): cursor.close()
            if 'conn' in locals() and conn.is_connected(): conn.close()

    @staticmethod
    def update(patient_id, first_name, last_name, dob, phone, email, gender):
        conn = get_connection()
        if not conn: return False
        try:
            cursor = conn.cursor()
            query = """UPDATE patients SET first_name=%s, last_name=%s, dob=%s, 
                       phone=%s, email=%s, gender=%s WHERE id=%s"""
            cursor.execute(query, (first_name, last_name, dob, phone, email, gender, patient_id))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error updating patient: {e}")
            return False
        finally:
            if 'cursor' in locals(): cursor.close()
            if 'conn' in locals() and conn.is_connected(): conn.close()

    @staticmethod
    def delete(patient_id):
        conn = get_connection()
        if not conn: return False
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM patients WHERE id=%s", (patient_id,))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error deleting patient: {e}")
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
            query = """SELECT * FROM patients WHERE 
                       first_name LIKE %s OR last_name LIKE %s OR 
                       phone LIKE %s OR email LIKE %s"""
            cursor.execute(query, (search_pattern, search_pattern, search_pattern, search_pattern))
            return cursor.fetchall()
        except Exception as e:
            print(f"Error searching patients: {e}")
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
            cursor.execute("SELECT COUNT(*) FROM patients")
            return cursor.fetchone()[0]
        except Exception as e:
            print(f"Error counting patients: {e}")
            return 0
        finally:
            if 'cursor' in locals(): cursor.close()
            if 'conn' in locals() and conn.is_connected(): conn.close()
