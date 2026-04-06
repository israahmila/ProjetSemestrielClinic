"""
Appointment Model
Handles all database operations for Appointments.
"""
from database.db_connection import get_connection

class Appointment:
    @staticmethod
    def add(patient_id, doctor_id, date, time, status):
        conn = get_connection()
        if not conn: return False
        try:
            cursor = conn.cursor()
            query = """INSERT INTO appointments (patient_id, doctor_id, date, time, status) 
                       VALUES (%s, %s, %s, %s, %s)"""
            cursor.execute(query, (patient_id, doctor_id, date, time, status))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error adding appointment: {e}")
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
                SELECT a.id, a.date, a.time, a.status,
                       CONCAT(p.first_name, ' ', p.last_name) as patient_name,
                       CONCAT(d.first_name, ' ', d.last_name) as doctor_name,
                       a.patient_id, a.doctor_id
                FROM appointments a
                JOIN patients p ON a.patient_id = p.id
                JOIN doctors d ON a.doctor_id = d.id
                ORDER BY a.date DESC, a.time DESC
            """
            cursor.execute(query)
            return cursor.fetchall()
        except Exception as e:
            print(f"Error fetching appointments: {e}")
            return []
        finally:
            if 'cursor' in locals(): cursor.close()
            if 'conn' in locals() and conn.is_connected(): conn.close()

    @staticmethod
    def update(appointment_id, patient_id, doctor_id, date, time, status):
        conn = get_connection()
        if not conn: return False
        try:
            cursor = conn.cursor()
            query = """UPDATE appointments SET patient_id=%s, doctor_id=%s, date=%s, 
                       time=%s, status=%s WHERE id=%s"""
            cursor.execute(query, (patient_id, doctor_id, date, time, status, appointment_id))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error updating appointment: {e}")
            return False
        finally:
            if 'cursor' in locals(): cursor.close()
            if 'conn' in locals() and conn.is_connected(): conn.close()

    @staticmethod
    def delete(appointment_id):
        conn = get_connection()
        if not conn: return False
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM appointments WHERE id=%s", (appointment_id,))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error deleting appointment: {e}")
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
                SELECT a.id, a.date, a.time, a.status,
                       CONCAT(p.first_name, ' ', p.last_name) as patient_name,
                       CONCAT(d.first_name, ' ', d.last_name) as doctor_name,
                       a.patient_id, a.doctor_id
                FROM appointments a
                JOIN patients p ON a.patient_id = p.id
                JOIN doctors d ON a.doctor_id = d.id
                WHERE p.first_name LIKE %s OR p.last_name LIKE %s
                   OR d.first_name LIKE %s OR d.last_name LIKE %s
                   OR a.status LIKE %s
                ORDER BY a.date DESC
            """
            cursor.execute(query, (search_pattern, search_pattern, search_pattern, search_pattern, search_pattern))
            return cursor.fetchall()
        except Exception as e:
            print(f"Error searching appointments: {e}")
            return []
        finally:
            if 'cursor' in locals(): cursor.close()
            if 'conn' in locals() and conn.is_connected(): conn.close()

    @staticmethod
    def get_stats_today():
        conn = get_connection()
        if not conn: return 0
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM appointments WHERE date = CURDATE()")
            return cursor.fetchone()[0]
        except Exception as e:
            print(f"Error getting today's appointments: {e}")
            return 0
        finally:
            if 'cursor' in locals(): cursor.close()
            if 'conn' in locals() and conn.is_connected(): conn.close()

    @staticmethod
    def get_status_breakdown():
        conn = get_connection()
        if not conn: return []
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT status, COUNT(*) as count FROM appointments GROUP BY status")
            return cursor.fetchall()
        except Exception as e:
            print(f"Error getting status breakdown: {e}")
            return []
        finally:
            if 'cursor' in locals(): cursor.close()
            if 'conn' in locals() and conn.is_connected(): conn.close()
