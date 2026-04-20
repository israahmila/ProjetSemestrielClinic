# Clinic Management System

A production-quality desktop application for managing a clinic, built with Python, CustomTkinter, and MySQL.

## Requirements

- Python 3.10+
- MySQL 8.x

## Installation & Setup

1. **Install Python dependencies:**
   Open a terminal in the `clinic_app` folder and run:
   ```bash
   pip install customtkinter mysql-connector-python
   ```

2. **MySQL Database Setup:**
   - Ensure your MySQL server is running.
   - You can import the provided `clinic.sql` file via the MySQL command line or a tool like PhpMyAdmin/MySQL Workbench:
     ```bash
     mysql -u root -p < clinic.sql
     ```
   - This creates the `clinic_db` database, tables, and inserts default data.

3. **Configure Database Credentials:**
   - Open `config.py` and update the `DB_CONFIG` dictionary to match your MySQL server credentials (specifically the `password`).

## Running the Application

Execute the `main.py` entry point:
```bash
python main.py
```


## Default Login Credentials

- **Username:** `admin`
- **Password:** `admin123`
