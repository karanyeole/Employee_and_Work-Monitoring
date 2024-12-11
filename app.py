from flask import Flask, render_template, request, redirect, url_for, flash,Response,jsonify
import secrets
import os
import cv2
import numpy as np
import time
from capture_img import capture_image_stream, create_face_database

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
employee_id=None

import sqlite3
def init_leave_requests_db():
    # Connect to the SQLite database (it will create the database if it doesn't exist)
    conn = sqlite3.connect('leave_requests.db')
    cursor = conn.cursor()

    # Create a table for storing leave requests if it doesn't exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS leave_requests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        employee_name TEXT NOT NULL,
        employee_id TEXT NOT NULL,
        leave_type TEXT NOT NULL,
        start_date TEXT NOT NULL,
        end_date TEXT NOT NULL,
        reason TEXT NOT NULL,
        contact_info TEXT NOT NULL
    )
    ''')

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

# Function to store leave request data into the database
def store_leave_request(employee_name, employee_id, leave_type, start_date, end_date, reason, contact_info):
    # Connect to the SQLite database
    conn = sqlite3.connect('leave_requests.db')
    cursor = conn.cursor()

    # Insert the data into the database
    cursor.execute('''
    INSERT INTO leave_requests (employee_name, employee_id, leave_type, start_date, end_date, reason, contact_info)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (employee_name, employee_id, leave_type, start_date, end_date, reason, contact_info))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()
def init_db():
    conn = sqlite3.connect('employees.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT,
            last_name TEXT,
            dob TEXT,
            gender TEXT,
            email TEXT,
            phone TEXT,
            address TEXT,
            job_title TEXT,
            department TEXT,
            salary REAL,
            emergency_contact_name TEXT,
            emergency_contact_phone TEXT
        )
    ''')
    conn.commit()
    conn.close()
init_db()
# Run this function once to initialize the database

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/faq')
def faq():
    return render_template('faq.html')

@app.route('/gallery')
def gallery():
    return render_template('gallery.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/hr_services')
def hr_services():
    return render_template("hr_services.html")

@app.route('/emp_services')
def emp_services():
    return render_template("emp_services.html")


@app.route('/add_employee', methods=['GET', 'POST'])
def add_employee():
    if request.method == 'POST':
        global employee_id
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        dob = request.form['dob']
        gender = request.form['gender']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
        job_title = request.form['job_title']
        department = request.form['department']
        salary = request.form['salary']
        emergency_contact_name = request.form['emergency_contact_name']
        emergency_contact_phone = request.form['emergency_contact_phone']

        # Connect to the database
        conn = sqlite3.connect('employees.db')
        cursor = conn.cursor()

        # Insert the new employee
        cursor.execute('''
            INSERT INTO employees (
                first_name, last_name, dob, gender, email, phone, address,
                job_title, department, salary, emergency_contact_name, emergency_contact_phone
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (first_name, last_name, dob, gender, email, phone, address, job_title, department, salary,
              emergency_contact_name, emergency_contact_phone))

        # Commit and get the generated employee_id
        conn.commit()
        employee_id = cursor.lastrowid
        conn.close()

        # Return a JSON response with the employee_id
        return jsonify({"success": True, "employee_id": employee_id})

    return render_template("add_employee.html")
@app.route('/capture_images', methods=['POST', 'GET'])

def capture_images():
    if request.method == 'GET':
        # Example: Fetch the employee name from DB (you can modify the logic)
        conn = sqlite3.connect('employees.db')
        cursor = conn.cursor()
        cursor.execute("SELECT First_name, Last_name FROM employees WHERE id = ?", (employee_id,))
        r = cursor.fetchone()
        r=r[0]+r[1]
        # Return a valid response with the image stream
        return Response(capture_image_stream(r), mimetype='multipart/x-mixed-replace; boundary=frame')

# Rename the leave_request function for employees
@app.route('/leave_request', methods=['GET', 'POST'])
def leave_request():
    if request.method == 'POST':
        # Get the form data
        employee_name = request.form['employee_name']
        employee_id = request.form['employee_id']
        leave_type = request.form['leave_type']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        reason = request.form['reason']
        contact_info = request.form['contact_info']

        # Insert the data into the database
        conn = sqlite3.connect('leave_requests.db')
        c = conn.cursor()
        c.execute('''
            INSERT INTO leave_requests (employee_name, employee_id, leave_type, start_date, end_date, reason, contact_info)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (employee_name, employee_id, leave_type, start_date, end_date, reason, contact_info))
        conn.commit()
        conn.close()

        # Redirect to a success page or return a success message
        return render_template('leave_request_success.html', message="Leave request submitted successfully!")

    return render_template('leave_request.html')


# Rename the leave_request function for HR leave requests
@app.route('/leave_request_hr', methods=['GET', 'POST'])
def leave_request_hr():
    if request.method == 'POST':
        # Handle form submission logic for HR leave request (if needed)
        # You can save leave data to the database or send email notifications here
        flash("Leave request submitted successfully!")
        return redirect(url_for("leave_request_hr"))  # You can redirect to a confirmation page or back to the form

    return render_template("leave_request_hr.html")  # The HR page where leave requests are managed

# Route to display the list of employees
@app.route('/manage_employees', methods=['GET'])
def manage_employees():
    conn = sqlite3.connect('employees.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM employees")
    employees = cursor.fetchall()
    conn.close()
    return render_template("manage_employees.html", employees=employees)

# Route to edit an employee's details
@app.route('/edit_employee/<int:employee_id>', methods=['GET', 'POST'])
def edit_employee(employee_id):
    conn = sqlite3.connect('employees.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        # Collect form data
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        dob = request.form['dob']
        gender = request.form['gender']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
        job_title = request.form['job_title']
        department = request.form['department']
        salary = request.form['salary']
        emergency_contact_name = request.form['emergency_contact_name']
        emergency_contact_phone = request.form['emergency_contact_phone']
        
        # Update employee in the database
        cursor.execute('''
            UPDATE employees SET first_name=?, last_name=?, dob=?, gender=?, email=?, phone=?, 
            address=?, job_title=?, department=?, salary=?, emergency_contact_name=?, 
            emergency_contact_phone=? WHERE id=?
        ''', (first_name, last_name, dob, gender, email, phone, address, job_title, department, salary, emergency_contact_name, emergency_contact_phone, employee_id))
        conn.commit()
        conn.close()
        flash("Employee details updated successfully!")
        return redirect(url_for('manage_employees'))
    
    # Fetch current employee data to populate the form
    cursor.execute("SELECT * FROM employees WHERE id=?", (employee_id,))
    employee = cursor.fetchone()
    conn.close()
    return render_template("manage_employees.html", employee=employee)


# Route to delete an employee's details
@app.route('/delete_employee/<int:employee_id>', methods=['POST'])
def delete_employee(employee_id):
    conn = sqlite3.connect('employees.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM employees WHERE id=?", (employee_id,))
    conn.commit()
    conn.close()
    flash("Employee deleted successfully!")
    return redirect(url_for('manage_employees'))

@app.route("/training", methods=['POST'])
def training():
    global employee_id
    print(employee_id)
    conn = sqlite3.connect('employees.db')
    cursor = conn.cursor()

    # Fetch the employee's first and last name from the database
    cursor.execute("SELECT First_name, Last_name FROM employees WHERE id = ?", (employee_id,))
    result = cursor.fetchone()
    if not result:
        return jsonify({"error": "Employee not found"}), 404
    
    # Combine first and last names
    r = result[0] + result[1]
    print(r)
    # Assuming trainer function is defined and returns two lists
    create_face_database(r)
    
    # Close the database connection
    conn.close()
    
    return jsonify({"message": "Training completed successfully!"}), 200



@app.route('/employee/<int:employee_id>')
def view_employee(employee_id):
    # Connect to the database and fetch employee details
    conn = sqlite3.connect('employees.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM employees WHERE id = ?", (employee_id,))
    employee = cursor.fetchone()
    conn.close()
    
    # Check if the employee exists
    if not employee:
        return "Employee not found", 404

    # Map the fetched data to relevant fields
    employee_data = {
        "first_name": employee[1],
        "last_name": employee[2],
        "dob": employee[3],
        "gender": employee[4],
        "email": employee[5],
        "phone": employee[6],
        "address": employee[7],
        "job_title": employee[8],
        "department": employee[9],
        "salary": employee[10],
        "emergency_contact_name": employee[11],
        "emergency_contact_phone": employee[12]
    }

    return render_template("employee_details.html", employee=employee_data)
    
@app.route('/validate_employee', methods=['POST'])
def validate_employee():
    data = request.get_json()
    email = data.get("email")
    employee_id = data.get("password")  # Assume employee ID is being used as the password

    # Connect to the database
    conn = sqlite3.connect('employees.db')
    cursor = conn.cursor()

    # Query to check if the email and employee_id match
    cursor.execute("SELECT * FROM employees WHERE email = ? AND id = ?", (email, employee_id))
    employee = cursor.fetchone()
    conn.close()
    print(employee)
    if employee:
        return jsonify({"success": True})  # Matching record found
    else:
        return jsonify({"success": False})  # No matching record





if __name__ == "__main__":
    app.run(debug=True)