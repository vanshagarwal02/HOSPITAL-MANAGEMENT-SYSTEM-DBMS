import pymysql

# 1. Connect to the database
def connect_db():
    try:
        conn = pymysql.connect(
            host='localhost',
            user='sarvesht07',         # Change to your MySQL username
            password='Sarvesh@2005',   # Change to your MySQL password
            database='Hospital'
        )
        return conn
    except Exception as e:
        print("Could not connect to database:", e)
        return None

# 2. Print results as a simple table
def print_table(headers, rows):
    print("\n" + " | ".join(headers))
    print("-" * (len(headers) * 15))
    for row in rows:
        print(" | ".join(str(x) for x in row))
    print()

# 3. List all departments
def list_departments():
    conn = connect_db()
    if not conn:
        return
    with conn.cursor() as cur:
        cur.execute("SELECT DepartmentID, Name FROM DEPARTMENT")
        rows = cur.fetchall()
        print_table(["ID", "Department"], rows)
    conn.close()

# 4. List all employees in a department
def list_employees_by_department():
    conn = connect_db()
    if not conn:
        return
    with conn.cursor() as cur:
        cur.execute("SELECT DepartmentID, Name FROM DEPARTMENT")
        depts = cur.fetchall()
        print("\nDepartments:")
        for d in depts:
            print(f"{d[0]}: {d[1]}")
        dept_id = input("Enter Department ID: ")
        cur.execute("SELECT EmployeeID, Fname, Lname, Role FROM EMPLOYEE WHERE DepartmentID=%s", (dept_id,))
        rows = cur.fetchall()
        if rows:
            print_table(["ID", "First Name", "Last Name", "Role"], rows)
        else:
            print("No employees found in this department.")
    conn.close()

# 5. Register a new patient
def register_patient():
    print("\n--- Register New Patient ---")
    fname = input("First name: ")
    lname = input("Last name: ")
    bdate = input("Birth date (YYYY-MM-DD): ")
    gender = input("Gender (Male/Female/Other): ")
    contact = input("Contact number: ")
    aadhar = input("Aadhar number: ")
    insurance = input("Insurance ID (or leave blank): ")
    blood = input("Blood type (A+/A-/B+/B-/AB+/AB-/O+/O-): ")
    emergency = input("Emergency contact: ")
    conn = connect_db()
    if not conn:
        return
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO PATIENT (Fname, Lname, Bdate, Gender, ContactNo, AadharNo, InsuranceID, BloodType, EmergencyContact) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
            (fname, lname, bdate, gender, contact, aadhar, insurance, blood, emergency)
        )
        conn.commit()
        print("Patient registered successfully!")
    conn.close()

# 6. List all patients
def list_patients():
    conn = connect_db()
    if not conn:
        return
    with conn.cursor() as cur:
        cur.execute("SELECT PatientID, Fname, Lname, BloodType FROM PATIENT")
        rows = cur.fetchall()
        print_table(["ID", "First Name", "Last Name", "Blood Type"], rows)
    conn.close()

# 7. Search for a doctor by name
def search_doctor():
    name = input("Enter doctor name to search: ")
    conn = connect_db()
    if not conn:
        return
    with conn.cursor() as cur:
        cur.execute("""
            SELECT e.EmployeeID, e.Fname, e.Lname
            FROM EMPLOYEE e JOIN DOCTOR d ON e.EmployeeID = d.EmployeeID
            WHERE e.Fname LIKE %s OR e.Lname LIKE %s
        """, (f"%{name}%", f"%{name}%"))
        rows = cur.fetchall()
        if rows:
            print_table(["ID", "First Name", "Last Name"], rows)
        else:
            print("No doctor found with that name.")
    conn.close()

# 8. Main menu loop
def main():
    while True:
        print("\n--- Hospital Menu ---")
        print("1. List Departments")
        print("2. List Employees by Department")
        print("3. Register New Patient")
        print("4. List All Patients")
        print("5. Search Doctor by Name")
        print("6. Exit")
        choice = input("Choose an option (1-6): ")
        if choice == '1':
            list_departments()
        elif choice == '2':
            list_employees_by_department()
        elif choice == '3':
            register_patient()
        elif choice == '4':
            list_patients()
        elif choice == '5':
            search_doctor()
        elif choice == '6':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()