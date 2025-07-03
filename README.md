# Hospital Management System

This project is a Hospital Management System that allows users to manage various aspects of a hospital, including employees, patients, appointments, inventory, and billing. The system is implemented using Python and MySQL.

## Requirements
The `Requirements.pdf` showcases our initial requirements with the database along with purpose, users, application, database requirements (entities and relationships) and functional requirements.

## Entity-Realtionship (ER) Model
The `Entity_Realtionship_Model.pdf` showcases the database in the standard EER (extended ER) model with the respective entities and relationships while following the min-max constraints.

## Relational Model
The `Relational_Model.pdf` showcases the database in the relational model form and follows the normalisation through initial -> 1NF -> 2NF -> 3NF.
The final normalization is the one the databse is based upon.

## Database Schema

The database schema is defined in `database.sql` and includes the following tables:

- `DEPARTMENT`: Stores information about hospital departments.
- `EMPLOYEE`: Stores information about employees, including doctors and nurses.
- `PATIENT`: Stores information about patients.
- `DOCTOR`: Stores additional information specific to doctors.
- `NURSE`: Stores additional information specific to nurses.
- `INVENTORY`: Stores information about inventory items.
- `EQUIPMENT`: Stores information about hospital equipment.
- `FACILITY`: Stores information about hospital facilities.
- `TREATMENT`: Stores information about treatments provided to patients.
- `PRESCRIPTION`: Stores information about prescriptions issued by doctors.
- `PRESCRIPTION_INVENTORY`: Stores information about inventory items associated with prescriptions.
- `BILLING`: Stores information about billing records.
- `LAB_TEST`: Stores information about lab tests conducted for patients.
- `APPOINTMENT`: Stores information about appointments between patients and doctors.

## Commands

The `script.py` script provides the following commands to interact with the database:

1. **List employees by department**: Lists all employees from a specified department.
2. **List patients by doctor**: Lists all patients treated by a specified doctor.
3. **List appointments by date range**: Lists all appointments between two given dates.
4. **List low inventory items**: Lists inventory items with the lowest quantity.
5. **Search doctors by name**: Searches for doctors whose names match a given string.
6. **List patients with overdue payments**: Lists patients who have overdue billing payment status.
7. **List patients by medicine and doctor**: Lists patients who have been prescribed a specific medicine by a specific doctor.
8. **Add new employee**: Adds a new employee to the database.
9. **Register new patient**: Registers a new patient in the database.
10. **Add new equipment**: Adds new equipment to the database.
11. **Add new prescription**: Adds a new prescription and its associated inventory items to the database.
12. **Add new billing**: Adds a new billing record to the database.
13. **Update patient contact number**: Updates the contact number of a specified patient.
14. **Update appointment date, time, and status**: Updates the date, time, and/or status of a specified appointment.
15. **Update inventory quantity**: Updates the quantity of a specified inventory item.
16. **Delete equipment**: Deletes a specified equipment from the database.
17. **Delete inventory item**: Deletes a specified inventory item from the database.
18. **Exit**: Exits the program.

## Usage

To use the Hospital Management System, run the `script.py` script and follow the on-screen prompts to select and execute the desired command.
The user eill have to update the user and password to match the mysql password.
```
connection = pymysql.connect(
            host='localhost',
            user='user',
            password='password',
            database='Hospital'
        )
```

```
$ python script.py
```

Make sure you have the following dependencies installed.
```
pip install pymysql
pip install prettytable
```
