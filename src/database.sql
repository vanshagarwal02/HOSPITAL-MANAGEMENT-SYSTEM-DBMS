DROP DATABASE IF EXISTS Hospital;
CREATE DATABASE IF NOT EXISTS Hospital;
USE Hospital;

DROP TABLE IF EXISTS APPOINTMENT;
DROP TABLE IF EXISTS LAB_TEST;
DROP TABLE IF EXISTS BILLING;
DROP TABLE IF EXISTS PRESCRIPTION;
DROP TABLE IF EXISTS TREATMENT;
DROP TABLE IF EXISTS FACILITY;
DROP TABLE IF EXISTS EQUIPMENT;
DROP TABLE IF EXISTS INVENTORY;
DROP TABLE IF EXISTS NURSE;
DROP TABLE IF EXISTS DOCTOR;
DROP TABLE IF EXISTS PATIENT;
DROP TABLE IF EXISTS EMPLOYEE;
DROP TABLE IF EXISTS DEPARTMENT;

--auto increment it sets the numbering from 1 by default and whenever a new record is added then value is increased by 1

CREATE TABLE DEPARTMENT (
    DepartmentID INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(50) NOT NULL,
    Location VARCHAR(100) NOT NULL,
    HeadOfDepartment INTEGER,
    ContactNo VARCHAR(10) NOT NULL
);

CREATE TABLE EMPLOYEE (
    EmployeeID INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
    Fname VARCHAR(30) NOT NULL,
    Lname VARCHAR(30) NOT NULL,
    Bdate DATE NOT NULL,
    Role ENUM('Doctor', 'Nurse', 'Administrator', 'Support Staff') NOT NULL,
    ContactNo VARCHAR(10) NOT NULL,
    Gender ENUM('Male', 'Female', 'Other') NOT NULL,
    DepartmentID INTEGER,
    SupervisorID INTEGER,
    JoiningDate DATE NOT NULL
);

CREATE TABLE PATIENT (
    PatientID INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
    Fname VARCHAR(30) NOT NULL,
    Lname VARCHAR(30) NOT NULL,
    Bdate DATE NOT NULL,
    Gender ENUM('Male', 'Female', 'Other') NOT NULL,
    ContactNo VARCHAR(10) NOT NULL,
    AadharNo VARCHAR(12) UNIQUE NOT NULL,
    InsuranceID VARCHAR(20),
    BloodType ENUM('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-') NOT NULL,
    EmergencyContact VARCHAR(15) NOT NULL
);

CREATE TABLE DOCTOR (
    EmployeeID INTEGER NOT NULL PRIMARY KEY,
    Specialization VARCHAR(50) NOT NULL,
    LicenseNumber INTEGER NOT NULL,
    MedicalQualifications VARCHAR(100) NOT NULL
);

CREATE TABLE NURSE (
    EmployeeID INTEGER NOT NULL PRIMARY KEY,
    Specialization VARCHAR(50) NOT NULL,
    MedicalQualifications VARCHAR(100) NOT NULL
);

CREATE TABLE INVENTORY (
    InventoryID INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
    DepartmentID INTEGER,
    Name VARCHAR(50) NOT NULL,
    Quantity INTEGER NOT NULL,
    ManufactureDate DATE NOT NULL,
    ExpiryDate DATE
);

CREATE TABLE EQUIPMENT (
    EquipmentID INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
    DepartmentID INTEGER,
    Name VARCHAR(50) NOT NULL,
    Type ENUM('Diagnostic', 'Surgical', 'Therapeutic') NOT NULL,
    PurchaseDate DATE NOT NULL,
    EquipmentCondition ENUM('New', 'Good', 'Fair', 'Poor') NOT NULL
);

CREATE TABLE FACILITY (
    FacilityID INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
    Type ENUM('Room', 'ICU', 'Ambulance', 'Operation Theater', 'Waiting Area') NOT NULL,
    Capacity INTEGER NOT NULL,
    Location VARCHAR(100) NOT NULL,
    DepartmentID INTEGER,
    Status ENUM('Available', 'Under Maintenance', 'Out of Service') NOT NULL
);

CREATE TABLE TREATMENT (
    TreatmentID INTEGER NOT NULL,
    PatientID INTEGER NOT NULL,
    DoctorID INTEGER NOT NULL,
    StartDate DATE NOT NULL,
    EndDate DATE,
    TreatmentNotes TEXT,
    PRIMARY KEY (TreatmentID, PatientID, DoctorID)
);

CREATE TABLE PRESCRIPTION (
    PrescriptionID INTEGER NOT NULL,
    PrescribedBy INTEGER NOT NULL,
    DosageInstructions VARCHAR(100) NOT NULL,
    DatePrescribed DATE NOT NULL,
    PRIMARY KEY (PrescriptionID, PrescribedBy)
);

CREATE TABLE PRESCRIPTION_INVENTORY(
    PrescriptionID INTEGER NOT NULL,
    PrescribedBy INTEGER NOT NULL,
    InventoryID INTEGER NOT NULL,
    Quantity INTEGER NOT NULL,
    PRIMARY KEY (PrescriptionID, PrescribedBy, InventoryID)
);

CREATE TABLE BILLING (
    BillID INTEGER NOT NULL,
    PatientID INTEGER NOT NULL,
    TreatmentID INTEGER NOT NULL,
    PrescriptionID INTEGER NOT NULL,
    TotalAmount DECIMAL(10, 2) NOT NULL,
    PaymentStatus ENUM('Pending', 'Paid', 'Overdue') NOT NULL,
    DateIssued DATE NOT NULL,
    DatePaid DATE,
    PRIMARY KEY (BillID, PatientID, TreatmentID, PrescriptionID)
);

CREATE TABLE LAB_TEST (
    TestID INTEGER NOT NULL,
    PatientID INTEGER NOT NULL,
    LabName VARCHAR(50) NOT NULL,
    DepartmentID INTEGER NOT NULL,
    TestName VARCHAR(50) NOT NULL,
    TestDate DATE NOT NULL,
    Results TEXT,
    PRIMARY KEY (TestID, PatientID)
);

CREATE TABLE APPOINTMENT (
    AppointmentID INTEGER NOT NULL,
    PatientID INTEGER NOT NULL,
    DoctorID INTEGER NOT NULL,
    AppointmentDate DATE NOT NULL,
    AppointmentTime TIME NOT NULL,
    Status ENUM('Scheduled', 'Completed', 'Cancelled') NOT NULL,
    PRIMARY KEY (AppointmentID, PatientID)
);


-- Add foreign key constraints
ALTER TABLE DEPARTMENT
ADD CONSTRAINT fk_head_of_department
FOREIGN KEY (HeadOfDepartment) REFERENCES EMPLOYEE(EmployeeID)
    ON DELETE SET NULL
    ON UPDATE CASCADE; --this is basically when u do changes in parent is showcases in child too

ALTER TABLE EMPLOYEE
ADD CONSTRAINT fk_department
FOREIGN KEY (DepartmentID) REFERENCES DEPARTMENT(DepartmentID)
    ON DELETE SET NULL
    ON UPDATE CASCADE,
ADD CONSTRAINT fk_supervisor
FOREIGN KEY (SupervisorID) REFERENCES EMPLOYEE(EmployeeID)
    ON DELETE SET NULL
    ON UPDATE CASCADE;

ALTER TABLE DOCTOR
ADD CONSTRAINT fk_doctor_employee
FOREIGN KEY (EmployeeID) REFERENCES EMPLOYEE(EmployeeID)
    ON DELETE CASCADE
    ON UPDATE CASCADE;

ALTER TABLE NURSE
ADD CONSTRAINT fk_nurse_employee
FOREIGN KEY (EmployeeID) REFERENCES EMPLOYEE(EmployeeID)
    ON DELETE CASCADE
    ON UPDATE CASCADE;

ALTER TABLE INVENTORY
ADD CONSTRAINT fk_inventory_department
FOREIGN KEY (DepartmentID) REFERENCES DEPARTMENT(DepartmentID)
    ON DELETE SET NULL
    ON UPDATE CASCADE;

ALTER TABLE EQUIPMENT
ADD CONSTRAINT fk_equipment_department
FOREIGN KEY (DepartmentID) REFERENCES DEPARTMENT(DepartmentID)
    ON DELETE SET NULL
    ON UPDATE CASCADE;

ALTER TABLE FACILITY
ADD CONSTRAINT fk_facility_department
FOREIGN KEY (DepartmentID) REFERENCES DEPARTMENT(DepartmentID)
    ON DELETE SET NULL
    ON UPDATE CASCADE;

ALTER TABLE TREATMENT
ADD CONSTRAINT fk_treatment_patient
FOREIGN KEY (PatientID) REFERENCES PATIENT(PatientID)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
ADD CONSTRAINT fk_treatment_doctor
FOREIGN KEY (DoctorID) REFERENCES DOCTOR(EmployeeID)
    ON DELETE CASCADE
    ON UPDATE CASCADE;

ALTER TABLE PRESCRIPTION
ADD CONSTRAINT fk_prescription_prescribed_by
FOREIGN KEY (PrescribedBy) REFERENCES DOCTOR(EmployeeID)
    ON DELETE CASCADE
    ON UPDATE CASCADE;

ALTER TABLE PRESCRIPTION_INVENTORY
ADD CONSTRAINT fk_prescription_inventory_prescription
FOREIGN KEY (PrescriptionID) REFERENCES PRESCRIPTION(PrescriptionID)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
ADD CONSTRAINT fk_prescription_inventory_prescribed_by
FOREIGN KEY (PrescribedBy) REFERENCES DOCTOR(EmployeeID)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
ADD CONSTRAINT fk_prescription_inventory_inventory
FOREIGN KEY (InventoryID) REFERENCES INVENTORY(InventoryID)
    ON DELETE CASCADE
    ON UPDATE CASCADE;

ALTER TABLE BILLING
ADD CONSTRAINT fk_billing_patient
FOREIGN KEY (PatientID) REFERENCES PATIENT(PatientID)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
ADD CONSTRAINT fk_billing_treatment
FOREIGN KEY (TreatmentID) REFERENCES TREATMENT(TreatmentID)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
ADD CONSTRAINT fk_billing_prescription
FOREIGN KEY (PrescriptionID) REFERENCES PRESCRIPTION(PrescriptionID)
    ON DELETE CASCADE
    ON UPDATE CASCADE;

ALTER TABLE LAB_TEST
ADD CONSTRAINT fk_lab_test_patient
FOREIGN KEY (PatientID) REFERENCES PATIENT(PatientID)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
ADD CONSTRAINT fk_lab_test_department
FOREIGN KEY (DepartmentID) REFERENCES DEPARTMENT(DepartmentID)
    ON DELETE CASCADE
    ON UPDATE CASCADE;

ALTER TABLE APPOINTMENT
ADD CONSTRAINT fk_appointment_patient
FOREIGN KEY (PatientID) REFERENCES PATIENT(PatientID)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
ADD CONSTRAINT fk_appointment_doctor
FOREIGN KEY (DoctorID) REFERENCES DOCTOR(EmployeeID)
    ON DELETE CASCADE
    ON UPDATE CASCADE;

--foreign key for me will be directly while declaring the tables 

-- Populate the tables with values
INSERT INTO DEPARTMENT (Name, Location, HeadOfDepartment, ContactNo) VALUES
('Cardiology', 'Building A', NULL, '1234567890'), -- HeadOfDepartment is a doctor
('Neurology', 'Building B', NULL, '0987654321'), -- HeadOfDepartment is a doctor
('Orthopedics', 'Building C', NULL, '1122334455'), -- HeadOfDepartment is a doctor
('Pediatrics', 'Building D', NULL, '2233445566'), -- HeadOfDepartment is a doctor
('Oncology', 'Building E', NULL, '3344556677'), -- HeadOfDepartment is a doctor
('Dermatology', 'Building F', NULL, '4455667788'), -- HeadOfDepartment is a doctor
('Gastroenterology', 'Building G', NULL, '5566778899'); -- HeadOfDepartment is a doctor

INSERT INTO EMPLOYEE (Fname, Lname, Bdate, Role, ContactNo, Gender, DepartmentID, SupervisorID, JoiningDate) VALUES
('John', 'Doe', '1980-01-01', 'Doctor', '9876543210', 'Male', 1, NULL, '2010-01-01'),
('Jane', 'Smith', '1985-02-02', 'Nurse', '9988776655', 'Female', 2, 1, '2015-02-02'),
('Emily', 'Johnson', '1990-03-03', 'Doctor', '1112223334', 'Female', 3, 1, '2018-03-03'),
('Michael', 'Williams', '1982-04-04', 'Nurse', '2223334445', 'Male', 4, 2, '2016-04-04'),
('David', 'Brown', '1975-05-05', 'Administrator', '3334445556', 'Male', 5, NULL, '2005-05-05'),
('Sarah', 'Davis', '1988-06-06', 'Support Staff', '4445556667', 'Female', 6, 5, '2012-06-06'),
('James', 'Miller', '1992-07-07', 'Doctor', '5556667778', 'Male', 7, 3, '2020-07-07'),
('Laura', 'Wilson', '1983-08-08', 'Nurse', '6667778889', 'Female', 1, 2, '2017-08-08'),
('Robert', 'Moore', '1979-09-09', 'Doctor', '7778889990', 'Male', 2, 1, '2009-09-09'),
('Linda', 'Taylor', '1986-10-10', 'Support Staff', '8889990001', 'Female', 3, 6, '2013-10-10'),
('Charles', 'Anderson', '1991-11-11', 'Administrator', '9990001112', 'Male', 4, 5, '2011-11-11'),
('Barbara', 'Thomas', '1984-12-12', 'Nurse', '0001112223', 'Female', 5, 4, '2014-12-12'),
('Daniel', 'Jackson', '1987-01-13', 'Doctor', '1112223335', 'Male', 6, 3, '2019-01-13'),
('Jennifer', 'White', '1993-02-14', 'Support Staff', '2223334446', 'Female', 7, 6, '2021-02-14'),
('Paul', 'Harris', '1981-03-15', 'Doctor', '3334445557', 'Male', 1, 1, '2008-03-15'),
('Nancy', 'Martinez', '1985-04-16', 'Doctor', '4445556668', 'Female', 4, 1, '2011-04-16'),
('Kevin', 'Garcia', '1989-05-17', 'Doctor', '5556667779', 'Male', 5, 1, '2012-05-17'),
('Karen', 'Rodriguez', '1991-06-18', 'Nurse', '6667778880', 'Female', 6, 1, '2013-06-18'),
('Steven', 'Martinez', '1983-07-19', 'Doctor', '7778889991', 'Male', 7, 1, '2014-07-19'),
('Betty', 'Hernandez', '1987-08-20', 'Nurse', '8889990002', 'Female', 3, 1, '2015-08-20');

INSERT INTO PATIENT (Fname, Lname, Bdate, Gender, ContactNo, AadharNo, InsuranceID, BloodType, EmergencyContact) VALUES
('Alice', 'Brown', '1990-03-03', 'Female', '1231231234', '123412341234', 'INS123', 'A+', '9876543210'),
('Bob', 'Green', '1988-04-04', 'Male', '3213214321', '432143214321', 'INS456', 'B+', '8765432109'),
('Charlie', 'Black', '1992-05-05', 'Male', '4321432143', '543215432154', 'INS789', 'O+', '7654321098'),
('Diana', 'White', '1987-06-06', 'Female', '5432543254', '654326543265', 'INS012', 'AB+', '6543210987'),
('Edward', 'Gray', '1995-07-07', 'Male', '6543654365', '765437654376', 'INS345', 'B-', '5432109876'),
('Fiona', 'Blue', '1993-08-08', 'Female', '7654765476', '876548765487', 'INS678', 'A-', '4321098765'),
('George', 'Red', '1986-09-09', 'Male', '8765876587', '987659876598', 'INS901', 'O-', '3210987654'),
('Hannah', 'Yellow', '1991-10-10', 'Female', '9876987698', '098760987609', 'INS234', 'AB-', '2109876543'),
('Ian', 'Purple', '1984-11-11', 'Male', '0987098709', '109871098710', 'INS567', 'A+', '1098765432'),
('Julia', 'Pink', '1996-12-12', 'Female', '1098109810', '210982109821', 'INS890', 'B+', '0987654321');

INSERT INTO DOCTOR (EmployeeID, Specialization, LicenseNumber, MedicalQualifications) VALUES
(1, 'Cardiology', 12345, 'MBBS, MD'),
(3, 'Orthopedics', 67890, 'MBBS, MS'),
(7, 'Gastroenterology', 11223, 'MBBS, MD'),
(9, 'Neurology', 33445, 'MBBS, MD'),
(13, 'Dermatology', 55667, 'MBBS, MD'),
(15, 'Cardiology', 77889, 'MBBS, MD'),
(16, 'Pediatrics', 88990, 'MBBS, MD'),
(17, 'Oncology', 99001, 'MBBS, MD'),
(19, 'Gastroenterology', 10112, 'MBBS, MD');

INSERT INTO NURSE (EmployeeID, Specialization, MedicalQualifications) VALUES
(2, 'Neurology', 'BSc Nursing'),
(4, 'Pediatrics', 'BSc Nursing'),
(8, 'Cardiology', 'BSc Nursing'),
(12, 'Oncology', 'BSc Nursing'),
(18, 'Dermatology', 'BSc Nursing'),
(20, 'Orthopedics', 'BSc Nursing');

INSERT INTO INVENTORY (DepartmentID, Name, Quantity, ManufactureDate, ExpiryDate) VALUES
(1, 'Stent', 100, '2022-01-01', '2025-01-01'),
(2, 'Syringe', 200, '2022-02-01', '2024-02-01'),
(3, 'Bandage', 150, '2022-03-01', '2024-03-01'),
(4, 'Thermometer', 50, '2022-04-01', '2025-04-01'),
(5, 'Chemotherapy Drugs', 75, '2022-05-01', '2023-05-01'),
(6, 'Skin Cream', 120, '2022-06-01', '2024-06-01'),
(7, 'Endoscope', 30, '2022-07-01', '2025-07-01');

INSERT INTO EQUIPMENT (DepartmentID, Name, Type, PurchaseDate, EquipmentCondition) VALUES
(1, 'ECG Machine', 'Diagnostic', '2020-01-01', 'Good'),
(2, 'MRI Machine', 'Diagnostic', '2019-01-01', 'Fair'),
(3, 'X-Ray Machine', 'Diagnostic', '2018-01-01', 'Good'),
(4, 'Ultrasound Machine', 'Diagnostic', '2017-01-01', 'Fair'),
(5, 'Radiation Therapy Machine', 'Therapeutic', '2016-01-01', 'Good'),
(6, 'Laser Treatment Machine', 'Therapeutic', '2015-01-01', 'Fair'),
(7, 'Colonoscope', 'Diagnostic', '2014-01-01', 'Good');

INSERT INTO FACILITY (Type, Capacity, Location, DepartmentID, Status) VALUES
('Room', 2, 'Building A, Floor 1', 1, 'Available'),
('ICU', 1, 'Building B, Floor 2', 2, 'Under Maintenance'),
('Ambulance', 1, 'Building C, Parking Lot', 3, 'Available'),
('Operation Theater', 1, 'Building D, Floor 3', 4, 'Out of Service'),
('Waiting Area', 10, 'Building E, Ground Floor', 5, 'Available'),
('Room', 2, 'Building F, Floor 2', 6, 'Available'),
('ICU', 1, 'Building G, Floor 1', 7, 'Under Maintenance');

INSERT INTO TREATMENT (TreatmentID, PatientID, DoctorID, StartDate, EndDate, TreatmentNotes) VALUES
(1, 1, 1, '2023-01-01', '2023-01-10', 'Treatment for heart condition'),
(2, 2, 1, '2023-02-01', '2023-02-15', 'Follow-up for heart condition'),
(1, 3, 3, '2023-03-01', '2023-03-10', 'Treatment for broken leg'),
(2, 4, 16, '2023-04-01', '2023-04-15', 'Treatment for flu'), -- Changed to valid doctor ID
(3, 5, 17, '2023-05-01', '2023-05-10', 'Treatment for cancer'), -- Changed to valid doctor ID
(4, 6, 13, '2023-06-01', '2023-06-15', 'Treatment for skin condition'), -- Changed to valid doctor ID
(5, 7, 7, '2023-07-01', '2023-07-10', 'Treatment for stomach issues'),
(6, 8, 1, '2023-08-01', '2023-08-15', 'Treatment for heart condition'),
(7, 9, 9, '2023-09-01', '2023-09-10', 'Treatment for neurological issues'),
(8, 10, 3, '2023-10-01', '2023-10-15', 'Treatment for broken arm'),
(9, 1, 1, '2023-11-01', '2023-11-10', 'Follow-up for heart condition'),
(10, 2, 16, '2023-12-01', '2023-12-15', 'Follow-up for flu'); -- Changed to valid doctor ID

INSERT INTO PRESCRIPTION (PrescriptionID, PrescribedBy, DosageInstructions, DatePrescribed) VALUES
(1, 1, 'Take one daily', '2023-01-01'),
(2, 1, 'Use as needed', '2023-02-01'),
(3, 3, 'Apply twice daily', '2023-03-01'),
(4, 16, 'Take one tablet after meal', '2023-04-01'), -- Changed to valid doctor ID
(5, 17, 'Use once daily', '2023-05-01'), -- Changed to valid doctor ID
(6, 13, 'Take one capsule before bed', '2023-06-01'), -- Changed to valid doctor ID
(7, 7, 'Apply on affected area', '2023-07-01'),
(8, 1, 'Take two tablets daily', '2023-08-01'),
(1, 9, 'Use as directed', '2023-09-01'),
(10, 3, 'Take one tablet every 8 hours', '2023-10-01');

INSERT INTO PRESCRIPTION_INVENTORY (PrescriptionID, PrescribedBy, InventoryID, Quantity) VALUES
(1, 1, 1, 1),
(2, 1, 2, 2),
(3, 3, 3, 1),
(4, 16, 4, 1),
(5, 17, 5, 1),
(6, 13, 6, 1),
(7, 7, 7, 1),
(8, 1, 1, 2),
(1, 9, 2, 2),
(10, 3, 3, 2);

INSERT INTO BILLING (BillID, PatientID, TreatmentID, PrescriptionID, TotalAmount, PaymentStatus, DateIssued, DatePaid) VALUES
(1, 1, 1, 1, 5000.00, 'Paid', '2023-01-15', '2023-01-20'),
(2, 2, 2, 2, 3000.00, 'Pending', '2023-02-20', NULL),
(3, 3, 1, 3, 4500.00, 'Paid', '2023-03-15', '2023-03-20'),
(4, 4, 2, 4, 2500.00, 'Overdue', '2023-04-20', NULL),
(5, 5, 3, 5, 6000.00, 'Paid', '2023-05-15', '2023-05-20'),
(6, 6, 4, 6, 3500.00, 'Pending', '2023-06-20', NULL),
(7, 7, 5, 7, 4000.00, 'Paid', '2023-07-15', '2023-07-20'),
(8, 8, 6, 8, 5500.00, 'Overdue', '2023-08-20', NULL),
(1, 1, 7, 1, 3000.00, 'Paid', '2023-09-15', '2023-09-20'),
(10, 10, 8, 10, 7000.00, 'Pending', '2023-10-20', NULL);

INSERT INTO LAB_TEST (TestID, PatientID, LabName, DepartmentID, TestName, TestDate, Results) VALUES
(1, 1, 'Lab A', 1, 'Blood Test', '2023-01-05', 'Normal'),
(2, 2, 'Lab B', 2, 'MRI Scan', '2023-02-10', 'Abnormal'),
(3, 3, 'Lab C', 3, 'X-Ray', '2023-03-15', 'Normal'),
(4, 4, 'Lab D', 4, 'Ultrasound', '2023-04-20', 'Normal'),
(5, 5, 'Lab E', 5, 'CT Scan', '2023-05-25', 'Abnormal'),
(6, 6, 'Lab F', 6, 'Biopsy', '2023-06-30', 'Normal'),
(7, 7, 'Lab G', 7, 'Endoscopy', '2023-07-05', 'Normal'),
(8, 8, 'Lab H', 1, 'Blood Test', '2023-08-10', 'Normal'),
(9, 9, 'Lab I', 2, 'MRI Scan', '2023-09-15', 'Abnormal'),
(10, 10, 'Lab J', 3, 'X-Ray', '2023-10-20', 'Normal');

INSERT INTO APPOINTMENT (AppointmentID, PatientID, DoctorID, AppointmentDate, AppointmentTime, Status) VALUES
(1, 1, 1, '2023-03-01', '10:00:00', 'Scheduled'),
(2, 2, 1, '2023-03-02', '11:00:00', 'Completed'),
(3, 3, 3, '2023-03-03', '12:00:00', 'Scheduled'),
(4, 4, 1, '2023-03-04', '13:00:00', 'Completed'),
(5, 5, 1, '2023-03-05', '14:00:00', 'Scheduled'),
(6, 6, 1, '2023-03-06', '15:00:00', 'Completed'),
(7, 7, 7, '2023-03-07', '16:00:00', 'Scheduled'),
(8, 8, 1, '2023-03-08', '17:00:00', 'Completed'),
(9, 9, 9, '2023-03-09', '18:00:00', 'Scheduled'),
(10, 10, 3, '2023-03-10', '19:00:00', 'Completed');

UPDATE DEPARTMENT SET HeadOfDepartment = 1 WHERE DepartmentID = 1;
UPDATE DEPARTMENT SET HeadOfDepartment = 9 WHERE DepartmentID = 2;
UPDATE DEPARTMENT SET HeadOfDepartment = 3 WHERE DepartmentID = 3; 
UPDATE DEPARTMENT SET HeadOfDepartment = 16 WHERE DepartmentID = 4;
UPDATE DEPARTMENT SET HeadOfDepartment = 17 WHERE DepartmentID = 5;
UPDATE DEPARTMENT SET HeadOfDepartment = 13 WHERE DepartmentID = 6; 
UPDATE DEPARTMENT SET HeadOfDepartment = 7 WHERE DepartmentID = 7;

