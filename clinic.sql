-- Create database
CREATE DATABASE IF NOT EXISTS clinic_db;
USE clinic_db;

-- Users table (Role based access: admin, receptionist)
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(64) NOT NULL, -- SHA-256 hash length is 64 hex characters
    role ENUM('admin', 'receptionist') NOT NULL DEFAULT 'receptionist'
);

-- Patients table
CREATE TABLE IF NOT EXISTS patients (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    dob DATE NOT NULL,
    phone VARCHAR(20),
    email VARCHAR(100),
    gender ENUM('Male', 'Female', 'Other') NOT NULL
);

-- Doctors table
CREATE TABLE IF NOT EXISTS doctors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    speciality VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    email VARCHAR(100)
);

-- Appointments table
CREATE TABLE IF NOT EXISTS appointments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    doctor_id INT NOT NULL,
    date DATE NOT NULL,
    time TIME NOT NULL,
    status ENUM('scheduled', 'done', 'cancelled') NOT NULL DEFAULT 'scheduled',
    FOREIGN KEY (patient_id) REFERENCES patients(id) ON DELETE CASCADE,
    FOREIGN KEY (doctor_id) REFERENCES doctors(id) ON DELETE CASCADE
);

-- Prescriptions table
CREATE TABLE IF NOT EXISTS prescriptions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    appointment_id INT NOT NULL,
    diagnosis TEXT NOT NULL,
    medication TEXT NOT NULL,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (appointment_id) REFERENCES appointments(id) ON DELETE CASCADE
);

-- Insert default admin user (password: admin123, hashed in SHA-256)
-- 'admin123' -> 240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9
INSERT INTO users (username, password_hash, role) 
VALUES ('admin', '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9', 'admin')
ON DUPLICATE KEY UPDATE username=username;

-- Insert realistic test data
INSERT INTO patients (first_name, last_name, dob, phone, email, gender) VALUES
('John', 'Doe', '1985-06-15', '1234567890', 'john.doe@email.com', 'Male'),
('Jane', 'Smith', '1992-09-21', '0987654321', 'jane.smith@email.com', 'Female'),
('Michael', 'Johnson', '1978-03-30', '5551234567', 'michael.j@email.com', 'Male');

INSERT INTO doctors (first_name, last_name, speciality, phone, email) VALUES
('Gregory', 'House', 'Diagnostician', '555-0101', 'house@clinic.com'),
('Allison', 'Cameron', 'Immunologist', '555-0102', 'cameron@clinic.com'),
('James', 'Wilson', 'Oncologist', '555-0103', 'wilson@clinic.com');

INSERT INTO appointments (patient_id, doctor_id, date, time, status) VALUES
(1, 1, CURDATE() + INTERVAL 1 DAY, '10:00:00', 'scheduled'),
(2, 2, CURDATE(), '14:30:00', 'done'),
(3, 3, CURDATE() + INTERVAL 2 DAY, '09:15:00', 'scheduled');

INSERT INTO prescriptions (appointment_id, diagnosis, medication, notes) VALUES
(2, 'Common Cold', 'Paracetamol 500mg, twice a day', 'Rest for 3 days and drink plenty of fluids.');
