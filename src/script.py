import pymysql
from datetime import datetime
from prettytable import PrettyTable

def connect_db():
    """Establish database connection"""
    try:
        connection = pymysql.connect(
            host='localhost',
            user='sarvesht07',
            password='Sarvesh@2005',
            database='Hospital'
        )
        return connection
    except pymysql.Error as e:
        print(f"\033[1;31mError connecting to database: {e}\033[1;0m")
        return None
    
def print_table(headers, rows):
    """Prints a table with given headers and rows using PrettyTable"""
    table = PrettyTable()
    table.field_names = [f"{header}" for header in headers]
    for row in rows:
        table.add_row(row)
    print(table)

def list_employees_by_department():
    """Lists all employees from a specified department"""
    conn = connect_db()
    if not conn:
        return
    
    try:
        with conn.cursor() as cursor:
            # First show available departments
            cursor.execute("SELECT DepartmentID, Name FROM DEPARTMENT")
            departments = cursor.fetchall()
            
            print("\nAvailable Departments:")
            for dept in departments:
                print(f"{dept[0]}: {dept[1]}")
            
            dept_id = input("\nEnter Department ID: ")
            
            cursor.execute("""
                SELECT e.EmployeeID, e.Fname, e.Lname, e.Role, e.ContactNo
                FROM EMPLOYEE e
                WHERE e.DepartmentID = %s
            """, (dept_id,))
            
            employees = cursor.fetchall()
            
            if not employees:
                print("\n\033[1;31mNo employees found in this department.\033[1;0m")
                return
            
            print("\n\033[1;32mEmployees in Department:\033[1;0m")
            print_table(["ID", "First Name", "Last Name", "Role", "Contact"], employees)
                
    except pymysql.Error as e:
        print(f"\033[1;31mError: {e}\033[1;0m")
    finally:
        conn.close()

def list_patients_by_doctor():
    """Lists all patients treated by a specified doctor"""
    conn = connect_db()
    if not conn:
        return
    
    try:
        with conn.cursor() as cursor:
            # First show available doctors
            cursor.execute("""
                SELECT d.EmployeeID, e.Fname, e.Lname, d.Specialization
                FROM DOCTOR d
                JOIN EMPLOYEE e ON d.EmployeeID = e.EmployeeID
            """)
            doctors = cursor.fetchall()
            
            print("\nAvailable Doctors:")
            for doc in doctors:
                print(f"{doc[0]}: Dr. {doc[1]} {doc[2]} ({doc[3]})")
            
            doctor_id = input("\nEnter Doctor ID: ")
            
            cursor.execute("""
                SELECT DISTINCT p.PatientID, p.Fname, p.Lname
                FROM PATIENT p
                JOIN TREATMENT t ON p.PatientID = t.PatientID
                WHERE t.DoctorID = %s
            """, (doctor_id,))
            
            patients = cursor.fetchall()
            
            if not patients:
                print("\n\033[1;31mNo patients found for this doctor.\033[1;0m")
                return
            
            print("\n\033[1;32mPatients treated by Doctor:\033[1;0m")
            print_table(["ID", "First Name", "Last Name"], patients)
                
    except pymysql.Error as e:
        print(f"\033[1;31mError: {e}\033[1;0m")
    finally:
        conn.close()

def list_appointments_by_date():
    """Lists all appointments between two given dates"""
    conn = connect_db()
    if not conn:
        return
    
    try:
        with conn.cursor() as cursor:
            print("\nEnter date range (format: YYYY-MM-DD)")
            start_date = input("Start date: ")
            end_date = input("End date: ")
            
            cursor.execute("""
                SELECT a.AppointmentID, p.Fname, p.Lname, e.Fname, e.Lname, 
                        a.AppointmentDate, a.AppointmentTime, a.Status
                FROM APPOINTMENT a
                JOIN PATIENT p ON a.PatientID = p.PatientID
                JOIN EMPLOYEE e ON a.DoctorID = e.EmployeeID
                WHERE a.AppointmentDate BETWEEN %s AND %s
                ORDER BY a.AppointmentDate, a.AppointmentTime
            """, (start_date, end_date))
            
            appointments = cursor.fetchall()
            
            if not appointments:
                print("\n\033[1;31mNo appointments found in this date range.\033[1;0m")
                return
            
            print("\n\033[1;32mAppointments:\033[1;0m")
            print_table(["ID", "Patient-Fname", "Patient-Lname", "Doctor-Fname", "Doctor-Lname", "Date", "Time", "Status"], appointments)
                
    except pymysql.Error as e:
        print(f"\033[1;31mError: {e}\033[1;0m")
    finally:
        conn.close()

def list_low_inventory():
    """Lists inventory items with lowest quantity"""
    conn = connect_db()
    if not conn:
        return
    
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT i.InventoryID, i.Name, i.Quantity, d.Name as Department
                FROM INVENTORY i
                LEFT JOIN DEPARTMENT d ON i.DepartmentID = d.DepartmentID
                WHERE i.Quantity <= 50
            """)
            
            items = cursor.fetchall()
            if not items:
                print("\n\033[1;32mAll inventories restocked to Quantity above 50.\033[1;0m")
                return
            
            print("\n\033[1;32mItems with Lowest Quantity:\033[1;0m")
            print_table(["ID", "Name", "Quantity", "Department"], items)
                
    except pymysql.Error as e:
        print(f"\033[1;31mError: {e}\033[1;0m")
    finally:
        conn.close()

def search_doctors():
    """Searches for doctors whose names match a given string"""
    conn = connect_db()
    if not conn:
        return
    
    try:
        with conn.cursor() as cursor:
            search_string = input("\nEnter doctor name to search: ")
            
            cursor.execute("""
                SELECT e.EmployeeID, e.Fname, e.Lname, d.Specialization
                FROM EMPLOYEE e
                JOIN DOCTOR d ON e.EmployeeID = d.EmployeeID
                WHERE e.Fname LIKE %s OR e.Lname LIKE %s
            """, (f"%{search_string}%", f"%{search_string}%"))
            
            doctors = cursor.fetchall()
            
            if not doctors:
                print("\n\033[1;31mNo doctors found matching the search criteria.\033[1;0m")
                return
            
            print("\n\033[1;32mMatching Doctors:\033[1;0m")
            print_table(["ID", "FName", "Lname", "Specialization"], doctors)
                
    except pymysql.Error as e:
        print(f"\033[1;31mError: {e}\033[1;0m")
    finally:
        conn.close()

def list_overdue_patients():
    """Lists patients who have overdue billing payment status"""
    conn = connect_db()
    if not conn:
        return
    
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT DISTINCT p.PatientID, p.Fname, p.Lname, b.TotalAmount, b.DateIssued
                FROM PATIENT p
                JOIN BILLING b ON p.PatientID = b.PatientID
                WHERE b.PaymentStatus = 'Overdue'
            """)
            
            patients = cursor.fetchall()
            
            if not patients:
                print("\n\033[1;31mNo patients found with overdue payments.\033[1;0m")
                return
            
            print("\n\033[1;32mPatients with Overdue Payments:\033[1;0m")
            print_table(["ID", "FName", "Lname", "Amount Due", "Date Issued"], patients)
                
    except pymysql.Error as e:
        print(f"\033[1;31mError: {e}\033[1;0m")
    finally:
        conn.close()

def list_patients_by_medicine_and_doctor():
    """Lists patients who have been prescribed a specific medicine by a specific doctor"""
    conn = connect_db()
    if not conn:
        return
    
    try:
        with conn.cursor() as cursor:
            # Show available doctors first
            cursor.execute("""
                SELECT d.EmployeeID, e.Fname, e.Lname
                FROM DOCTOR d
                JOIN EMPLOYEE e ON d.EmployeeID = e.EmployeeID
            """)
            doctors = cursor.fetchall()
            
            print("\nAvailable Doctors:")
            for doc in doctors:
                print(f"{doc[0]}: Dr. {doc[1]} {doc[2]}")
            
            doctor_id = input("\nEnter Doctor ID: ")
            medicine_name = input("Enter Medicine Name: ")
            
            cursor.execute("""
                SELECT DISTINCT p.PatientID, p.Fname, p.Lname
                FROM PATIENT p
                JOIN TREATMENT t ON p.PatientID = t.PatientID
                JOIN PRESCRIPTION pr ON t.DoctorID = pr.PrescribedBy
                JOIN PRESCRIPTION_INVENTORY pi ON pr.PrescriptionID = pi.PrescriptionID
                JOIN INVENTORY i ON pi.InventoryID = i.InventoryID
                WHERE t.DoctorID = %s AND i.Name LIKE %s
            """, (doctor_id, f"%{medicine_name}%"))
            
            patients = cursor.fetchall()
            
            if not patients:
                print("\n\033[1;31mNo patients found with this prescription.\033[1;0m")
                return
            
            print("\n\033[1;32mPatients prescribed this medicine:\033[1;0m")
            print_table(["ID", "FName", "LName"], patients)
                
    except pymysql.Error as e:
        print(f"Error: {e}")
    finally:
        conn.close()

def add_employee():
    """Adds a new employee to the database"""
    conn = connect_db()
    if not conn:
        return
    
    try:
        with conn.cursor() as cursor:
            role = input("Enter role (Doctor/Nurse/Administrator/Support Staff): ")
            fname = input("Enter first name: ")
            lname = input("Enter last name: ")
            bdate = input("Enter birth date (YYYY-MM-DD): ")
            contact_no = input("Enter contact number: ")
            gender = input("Enter gender (Male/Female/Other): ")
            
            # Show available departments
            cursor.execute("SELECT DepartmentID, Name FROM DEPARTMENT")
            departments = cursor.fetchall()
            
            print("\nAvailable Departments:")
            for dept in departments:
                print(f"{dept[0]}: {dept[1]}")
            
            department_id = input("Enter department ID: ")
            supervisor_id = input("Enter supervisor ID (or leave blank): ")
            joining_date = input("Enter joining date (YYYY-MM-DD): ")
            
            cursor.execute("""
                INSERT INTO EMPLOYEE (Fname, Lname, Bdate, Role, ContactNo, Gender, DepartmentID, SupervisorID, JoiningDate)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (fname, lname, bdate, role, contact_no, gender, department_id, supervisor_id or None, joining_date))
            
            employee_id = cursor.lastrowid
            
            if role == 'Doctor':
                specialization = input("Enter specialization: ")
                license_number = input("Enter license number: ")
                medical_qualifications = input("Enter medical qualifications: ")
                
                cursor.execute("""
                    INSERT INTO DOCTOR (EmployeeID, Specialization, LicenseNumber, MedicalQualifications)
                    VALUES (%s, %s, %s, %s)
                """, (employee_id, specialization, license_number, medical_qualifications))
            
            elif role == 'Nurse':
                specialization = input("Enter specialization: ")
                medical_qualifications = input("Enter medical qualifications: ")
                
                cursor.execute("""
                    INSERT INTO NURSE (EmployeeID, Specialization, MedicalQualifications)
                    VALUES (%s, %s, %s)
                """, (employee_id, specialization, medical_qualifications))
            
            conn.commit()
            print("\033[1;32mEmployee added successfully.\033[1;0m")
                
    except pymysql.Error as e:
        print(f"Error: {e}")
    finally:
        conn.close()

def register_patient():
    """Registers a new patient in the database"""
    conn = connect_db()
    if not conn:
        return
    
    try:
        with conn.cursor() as cursor:
            fname = input("Enter first name: ")
            lname = input("Enter last name: ")
            bdate = input("Enter birth date (YYYY-MM-DD): ")
            gender = input("Enter gender (Male/Female/Other): ")
            contact_no = input("Enter contact number: ")
            aadhar_no = input("Enter Aadhar number: ")
            insurance_id = input("Enter insurance ID (or leave blank): ")
            blood_type = input("Enter blood type (A+/A-/B+/B-/AB+/AB-/O+/O-): ")
            emergency_contact = input("Enter emergency contact number: ")
            
            cursor.execute("""
                INSERT INTO PATIENT (Fname, Lname, Bdate, Gender, ContactNo, AadharNo, InsuranceID, BloodType, EmergencyContact)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (fname, lname, bdate, gender, contact_no, aadhar_no, insurance_id, blood_type, emergency_contact))
            
            conn.commit()
            print("\033[1;32mPatient registered successfully.\033[1;0m")
                
    except pymysql.Error as e:
        print(f"Error: {e}")
    finally:
        conn.close()

def add_equipment():
    """Adds new equipment to the database"""
    conn = connect_db()
    if not conn:
        return
    
    try:
        with conn.cursor() as cursor:
            # Show available departments
            cursor.execute("SELECT DepartmentID, Name FROM DEPARTMENT")
            departments = cursor.fetchall()
            
            print("\nAvailable Departments:")
            for dept in departments:
                print(f"{dept[0]}: {dept[1]}")
            
            department_id = input("Enter Department ID: ")
            name = input("Enter Equipment Name: ")
            type = input("Enter Equipment Type (Diagnostic/Surgical/Therapeutic): ")
            purchase_date = input("Enter Purchase Date (YYYY-MM-DD): ")
            condition = input("Enter Equipment Condition (New/Good/Fair/Poor): ")
            
            cursor.execute("""
                INSERT INTO EQUIPMENT (DepartmentID, Name, Type, PurchaseDate, EquipmentCondition)
                VALUES (%s, %s, %s, %s, %s)
            """, (department_id, name, type, purchase_date, condition))
            
            conn.commit()
            print("\033[1;32mEquipment added successfully.\033[1;0m")
                
    except pymysql.Error as e:
        print(f"Error: {e}")
    finally:
        conn.close()

def add_prescription():
    """Adds a new prescription and its associated inventory items to the database"""
    conn = connect_db()
    if not conn:
        return
    
    try:
        with conn.cursor() as cursor:
            # Show available doctors
            cursor.execute("SELECT d.EmployeeID, e.Fname, e.Lname FROM DOCTOR d JOIN EMPLOYEE e ON d.EmployeeID = e.EmployeeID")
            doctors = cursor.fetchall()
            
            print("\nAvailable Doctors:")
            for doc in doctors:
                print(f"{doc[0]}: Dr. {doc[1]} {doc[2]}")
            
            doctor_id = input("Enter Doctor ID: ")
            dosage_instructions = input("Enter Dosage Instructions: ")
            date_prescribed = input("Enter Date Prescribed (YYYY-MM-DD): ")
            
            # Get the next prescription ID for the doctor
            cursor.execute("SELECT COALESCE(MAX(PrescriptionID), 0) + 1 FROM PRESCRIPTION WHERE PrescribedBy = %s", (doctor_id,))
            prescription_id = cursor.fetchone()[0]
            
            cursor.execute("""
                INSERT INTO PRESCRIPTION (PrescriptionID, PrescribedBy, DosageInstructions, DatePrescribed)
                VALUES (%s, %s, %s, %s)
            """, (prescription_id, doctor_id, dosage_instructions, date_prescribed))
            
            num_medicines = int(input("Enter number of medicines: "))
            
            for _ in range(num_medicines):
                # Show available inventory items
                cursor.execute("SELECT InventoryID, Name FROM INVENTORY")
                inventory_items = cursor.fetchall()
                
                print("\nAvailable Inventory Items:")
                for item in inventory_items:
                    print(f"{item[0]}: {item[1]}")
                
                inventory_id = input("Enter Inventory ID: ")
                quantity = input("Enter Quantity: ")
                
                cursor.execute("""
                    INSERT INTO PRESCRIPTION_INVENTORY (PrescriptionID, PrescribedBy, InventoryID, Quantity)
                    VALUES (%s, %s, %s, %s)
                """, (prescription_id, doctor_id, inventory_id, quantity))
            
            conn.commit()
            print("\033[1;32mPrescription and associated inventory items added successfully.\033[1;0m")
                
    except pymysql.Error as e:
        print(f"Error: {e}")
    finally:
        conn.close()

def add_billing():
    """Adds a new billing record to the database"""
    conn = connect_db()
    if not conn:
        return
    
    try:
        with conn.cursor() as cursor:
            # Show available patients
            cursor.execute("SELECT PatientID, Fname, Lname FROM PATIENT")
            patients = cursor.fetchall()
            
            print("\nAvailable Patients:")
            for pat in patients:
                print(f"{pat[0]}: {pat[1]} {pat[2]}")
            
            patient_id = input("Enter Patient ID: ")
            
            # Show available treatments for the patient
            cursor.execute("SELECT TreatmentID, StartDate, EndDate FROM TREATMENT WHERE PatientID = %s", (patient_id,))
            treatments = cursor.fetchall()
            
            print("\nAvailable Treatments:")
            for treat in treatments:
                print(f"{treat[0]}: Start Date: {treat[1]}, End Date: {treat[2]}")
            
            treatment_id = input("Enter Treatment ID: ")
            
            # Show available prescriptions for the patient
            cursor.execute("SELECT PrescriptionID, DosageInstructions FROM PRESCRIPTION WHERE PrescribedBy IN (SELECT DoctorID FROM TREATMENT WHERE PatientID = %s)", (patient_id,))
            prescriptions = cursor.fetchall()
            
            print("\nAvailable Prescriptions:")
            for pres in prescriptions:
                print(f"{pres[0]}: {pres[1]}")
            
            prescription_id = input("Enter Prescription ID: ")
            total_amount = input("Enter Total Amount: ")
            payment_status = input("Enter Payment Status (Pending/Paid/Overdue): ")
            date_issued = input("Enter Date Issued (YYYY-MM-DD): ")
            date_paid = input("Enter Date Paid (or leave blank if not paid): ")
            
            # Get the next billing ID for the patient
            cursor.execute("SELECT COALESCE(MAX(BillID), 0) + 1 FROM BILLING WHERE PatientID = %s", (patient_id,))
            bill_id = cursor.fetchone()[0]
            
            cursor.execute("""
                INSERT INTO BILLING (BillID, PatientID, TreatmentID, PrescriptionID, TotalAmount, PaymentStatus, DateIssued, DatePaid)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (bill_id, patient_id, treatment_id, prescription_id, total_amount, payment_status, date_issued, date_paid or None))
            
            conn.commit()
            print("\033[1;32mBilling record added successfully.\033[1;0m")
                
    except pymysql.Error as e:
        print(f"Error: {e}")
    finally:
        conn.close()

def update_patient_contact():
    """Updates the contact number of a specified patient"""
    conn = connect_db()
    if not conn:
        return
    
    try:
        with conn.cursor() as cursor:
            # Show available patients
            cursor.execute("SELECT PatientID, Fname, Lname, ContactNo FROM PATIENT")
            patients = cursor.fetchall()
            
            print("\nAvailable Patients:")
            for pat in patients:
                print(f"{pat[0]}: {pat[1]} {pat[2]} (Current Contact: {pat[3]})")
            
            patient_id = input("Enter Patient ID: ")
            new_contact_no = input("Enter new contact number: ")
            
            cursor.execute("""
                UPDATE PATIENT
                SET ContactNo = %s
                WHERE PatientID = %s
            """, (new_contact_no, patient_id))
            
            conn.commit()
            print("\033[1;32mPatient contact number updated successfully.\033[1;0m")
                
    except pymysql.Error as e:
        print(f"Error: {e}")
    finally:
        conn.close()

def update_appointment():
    """Updates the date, time, and/or status of a specified appointment"""
    conn = connect_db()
    if not conn:
        return
    
    try:
        with conn.cursor() as cursor:
            # Show available appointments
            cursor.execute("""
                SELECT a.AppointmentID, p.Fname, p.Lname, a.AppointmentDate, a.AppointmentTime, a.Status
                FROM APPOINTMENT a
                JOIN PATIENT p ON a.PatientID = p.PatientID
            """)
            appointments = cursor.fetchall()
            
            print("\nAvailable Appointments:")
            for apt in appointments:
                print(f"{apt[0]}: {apt[1]} {apt[2]} (Date: {apt[3]}, Time: {apt[4]}, Status: {apt[5]})")
            
            appointment_id = input("Enter Appointment ID: ")
            new_date = input("Enter new date (YYYY-MM-DD) or leave blank to keep current: ")
            new_time = input("Enter new time (HH:MM:SS) or leave blank to keep current: ")
            new_status = input("Enter new status (Scheduled/Completed/Cancelled) or leave blank to keep current: ")
            
            if new_date:
                cursor.execute("""
                    UPDATE APPOINTMENT
                    SET AppointmentDate = %s
                    WHERE AppointmentID = %s
                """, (new_date, appointment_id))
            
            if new_time:
                cursor.execute("""
                    UPDATE APPOINTMENT
                    SET AppointmentTime = %s
                    WHERE AppointmentID = %s
                """, (new_time, appointment_id))
            
            if new_status:
                cursor.execute("""
                    UPDATE APPOINTMENT
                    SET Status = %s
                    WHERE AppointmentID = %s
                """, (new_status, appointment_id))
            
            conn.commit()
            print("\033[1;32mAppointment updated successfully.\033[1;0m")
                
    except pymysql.Error as e:
        print(f"Error: {e}")
    finally:
        conn.close()

def update_inventory_quantity():
    """Updates the quantity of a specified inventory item"""
    conn = connect_db()
    if not conn:
        return
    
    try:
        with conn.cursor() as cursor:
            # Show available inventory items
            cursor.execute("SELECT InventoryID, Name, Quantity FROM INVENTORY")
            inventory_items = cursor.fetchall()
            
            print("\nAvailable Inventory Items:")
            for item in inventory_items:
                print(f"{item[0]}: {item[1]} (Current Quantity: {item[2]})")
            
            inventory_id = input("Enter Inventory ID: ")
            new_quantity = input("Enter new quantity: ")
            
            cursor.execute("""
                UPDATE INVENTORY
                SET Quantity = %s
                WHERE InventoryID = %s
            """, (new_quantity, inventory_id))
            
            conn.commit()
            print("\033[1;32mInventory quantity updated successfully.\033[1;0m")
                
    except pymysql.Error as e:
        print(f"Error: {e}")
    finally:
        conn.close()

def delete_equipment():
    """Deletes a specified equipment from the database"""
    conn = connect_db()
    if not conn:
        return
    
    try:
        with conn.cursor() as cursor:
            # Show available equipment
            cursor.execute("SELECT EquipmentID, Name, DepartmentID FROM EQUIPMENT")
            equipment_items = cursor.fetchall()
            
            print("\nAvailable Equipment:")
            for item in equipment_items:
                print(f"{item[0]}: {item[1]} (Department ID: {item[2]})")
            
            equipment_id = input("Enter Equipment ID to delete: ")
            
            cursor.execute("DELETE FROM EQUIPMENT WHERE EquipmentID = %s", (equipment_id,))
            
            conn.commit()
            print("\033[1;32mEquipment deleted successfully.\033[1;0m")
                
    except pymysql.Error as e:
        print(f"Error: {e}")
    finally:
        conn.close()

def delete_inventory():
    """Deletes a specified inventory item from the database"""
    conn = connect_db()
    if not conn:
        return
    
    try:
        with conn.cursor() as cursor:
            # Show available inventory items
            cursor.execute("SELECT InventoryID, Name, DepartmentID FROM INVENTORY")
            inventory_items = cursor.fetchall()
            
            print("\nAvailable Inventory Items:")
            for item in inventory_items:
                print(f"{item[0]}: {item[1]} (Department ID: {item[2]})")
            
            inventory_id = input("Enter Inventory ID to delete: ")
            
            cursor.execute("DELETE FROM INVENTORY WHERE InventoryID = %s", (inventory_id,))
            
            conn.commit()
            print("\033[1;32mInventory item deleted successfully.\033[1;0m")
                
    except pymysql.Error as e:
        print(f"Error: {e}")
    finally:
        conn.close()

def main():
    while True:
        print("\n\033[1mHospital Management System\033[0m")
        print("\033[1m1.  List employees by department\033[0m")
        print("\033[1m2.  List patients by doctor\033[0m")
        print("\033[1m3.  List appointments by date range\033[0m")
        print("\033[1m4.  List low inventory items\033[0m")
        print("\033[1m5.  Search doctors by name\033[0m")
        print("\033[1m6.  List patients with overdue payments\033[0m")
        print("\033[1m7.  List patients by medicine and doctor\033[0m")
        print("\033[1m8.  Add new employee\033[0m")
        print("\033[1m9.  Register new patient\033[0m")
        print("\033[1m10. Add new equipment\033[0m")
        print("\033[1m11. Add new prescription\033[0m")
        print("\033[1m12. Add new billing\033[0m")
        print("\033[1m13. Update patient contact number\033[0m")
        print("\033[1m14. Update appointment date, time, and status\033[0m")
        print("\033[1m15. Update inventory quantity\033[0m")
        print("\033[1m16. Delete equipment\033[0m")
        print("\033[1m17. Delete inventory item\033[0m")
        print("\033[1m18. Exit\033[0m")        
        choice = input("\nEnter your choice (1-18): ")
        
        if choice == '1':
            list_employees_by_department()
        elif choice == '2':
            list_patients_by_doctor()
        elif choice == '3':
            list_appointments_by_date()
        elif choice == '4':
            list_low_inventory()
        elif choice == '5':
            search_doctors()
        elif choice == '6':
            list_overdue_patients()
        elif choice == '7':
            list_patients_by_medicine_and_doctor()
        elif choice == '8':
            add_employee()
        elif choice == '9':
            register_patient()
        elif choice == '10':
            add_equipment()
        elif choice == '11':
            add_prescription()
        elif choice == '12':
            add_billing()
        elif choice == '13':
            update_patient_contact()
        elif choice == '14':
            update_appointment()
        elif choice == '15':
            update_inventory_quantity()
        elif choice == '16':
            delete_equipment()
        elif choice == '17':
            delete_inventory()
        elif choice == '18':
            print("\nGoodbye!")
            break
        else:
            print("\n\033[1;31mInvalid choice. Please try again.\033[1;0m")

if __name__ == "__main__":
    main()