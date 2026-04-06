"""
Database Connection Module
"""
import mysql.connector
from mysql.connector import Error
import sys
import os

# Add the parent directory (clinic_app) to sys.path to find config.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

def get_connection():
    """
    Establishes and returns a connection to the MySQL database.
    Returns:
        mysql.connector.connection.MySQLConnection or None if failed.
    """
    try:
        conn = mysql.connector.connect(
            host=config.DB_CONFIG['host'],
            user=config.DB_CONFIG['user'],
            password=config.DB_CONFIG['password'],
            database=config.DB_CONFIG['database'],
            port=config.DB_CONFIG['port']
        )
        if conn.is_connected():
            return conn
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None
    return None
