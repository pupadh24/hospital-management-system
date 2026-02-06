CREATE DATABASE IF NOT EXISTS hms;

USE hms;

DROP TABLE IF EXISTS appointments;
DROP TABLE IF EXISTS doctors;
DROP TABLE IF EXISTS patients;

CREATE TABLE patients (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    full_name VARCHAR(100),
    dob DATE,
    blood_group VARCHAR(5),
    emergency_contact VARCHAR(15)
) AUTO_INCREMENT = 1001;

CREATE TABLE doctors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    name VARCHAR(100),
    specialization VARCHAR(50),
    contact VARCHAR(15)
) AUTO_INCREMENT = 501;

CREATE TABLE appointments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT,
    doctor_id INT,
    appointment_date DATETIME,
    status VARCHAR(20),
    FOREIGN KEY (patient_id) REFERENCES patients(id),
    FOREIGN KEY (doctor_id) REFERENCES doctors(id)
);

INSERT INTO patients (username, password, full_name, dob, blood_group, emergency_contact) VALUES 
('mchen', 'pass123', 'M Chen', '2005-04-12', 'A+', '513-555-0101'),
('sjohnson', 'pass123', 'S Johnson', '2007-11-30', 'O-', '513-555-0202'),
('dmiller', 'pass123', 'D Miller', '2002-07-22', 'B+', '513-555-0303'),
('ewilson', 'pass123', 'E Wilson', '2001-01-15', 'AB+', '513-555-0404'),
('jtaylor', 'pass123', 'J Taylor', '2006-09-05', 'O+', '513-555-0505');

INSERT INTO doctors (username, password, name, specialization, contact) VALUES 
('dr_smith', 'doc123', 'Dr. Smith', 'Cardiology', '555-0199'),
('arylie', 'pass123', 'Dr. Alex Rylie', 'General Medicine', '555-0101'),
('sttaylor', 'pass123', 'Dr. ST Taylor', 'Pediatrics', '555-0102'),
('emartinez', 'pass123', 'Dr. Elena Martinez', 'Neurology', '555-0103');


ALTER TABLE doctors ADD COLUMN salary DECIMAL(10, 2) DEFAULT 0.00;

CREATE TABLE admins (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(50) NOT NULL,
    full_name VARCHAR(100)
);

INSERT INTO admins (username, password, full_name) VALUES ('admin', 'admin', 'System Administrator');



