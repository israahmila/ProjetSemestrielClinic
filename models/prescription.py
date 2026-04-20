from database.db_connection import get_connection

class Prescription:
    @staticmethod
    def add(appointment_id, diagnosis, medication, notes):
        conn = get_connection()
        if not conn: return False
        try:
            cursor = conn.cursor()
            query = """INSERT INTO prescriptions (appointment_id, diagnosis, medication, notes) 
                       VALUES (%s, %s, %s, %s)"""
            cursor.execute(query, (appointment_id, diagnosis, medication, notes))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error adding prescription: {e}")
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
            query = """
                SELECT pr.id, pr.diagnosis, pr.medication, pr.notes, pr.created_at,
                       a.date as appointment_date,
                       CONCAT(p.first_name, ' ', p.last_name) as patient_name,
                       pr.appointment_id
                FROM prescriptions pr
                JOIN appointments a ON pr.appointment_id = a.id
                JOIN patients p ON a.patient_id = p.id
                ORDER BY pr.created_at DESC
            """
            cursor.execute(query)
            return cursor.fetchall()
        except Exception as e:
            print(f"Error fetching prescriptions: {e}")
            return []
        finally:
            if 'cursor' in locals(): cursor.close()
            if 'conn' in locals() and conn.is_connected(): conn.close()

    @staticmethod
    def update(prescription_id, appointment_id, diagnosis, medication, notes):
        conn = get_connection()
        if not conn: return False
        try:
            cursor = conn.cursor()
            query = """UPDATE prescriptions SET appointment_id=%s, diagnosis=%s, 
                       medication=%s, notes=%s WHERE id=%s"""
            cursor.execute(query, (appointment_id, diagnosis, medication, notes, prescription_id))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error updating prescription: {e}")
            return False
        finally:
            if 'cursor' in locals(): cursor.close()
            if 'conn' in locals() and conn.is_connected(): conn.close()

    @staticmethod
    def delete(prescription_id):
        conn = get_connection()
        if not conn: return False
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM prescriptions WHERE id=%s", (prescription_id,))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error deleting prescription: {e}")
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
            query = """
                SELECT pr.id, pr.diagnosis, pr.medication, pr.notes, pr.created_at,
                       a.date as appointment_date,
                       CONCAT(p.first_name, ' ', p.last_name) as patient_name,
                       pr.appointment_id
                FROM prescriptions pr
                JOIN appointments a ON pr.appointment_id = a.id
                JOIN patients p ON a.patient_id = p.id
                WHERE p.first_name LIKE %s OR p.last_name LIKE %s
                   OR pr.diagnosis LIKE %s OR pr.medication LIKE %s
                ORDER BY pr.created_at DESC
            """
            cursor.execute(query, (search_pattern, search_pattern, search_pattern, search_pattern))
            return cursor.fetchall()
        except Exception as e:
            print(f"Error searching prescriptions: {e}")
            return []
        finally:
            if 'cursor' in locals(): cursor.close()
            if 'conn' in locals() and conn.is_connected(): conn.close()
