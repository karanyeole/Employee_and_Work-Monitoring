
from flask import Flask, render_template, request, redirect, url_for, flash,Response,jsonify
import secrets
import os
import cv2
import time
from capture_img import capture_image_stream

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
employee_id=None

import sqlite3

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
        ''', (first_name, last_name, dob, gender, email, phone, address, job_title, department, salary, emergency_contact_name, emergency_contact_phone))
        
        # Commit and get the generated employee_id
        conn.commit()
        employee_id = cursor.lastrowid
        conn.close()
        
        # Return a JSON response with the employee_id
        return jsonify({"success": True, "employee_id": employee_id})
    
    return render_template("add_employee.html")


@app.route('/leave_request', methods=['GET', 'POST'])
def leave_request():
    if request.method == 'POST':
        leave_data = {
            "employee_name": request.form.get("employee_name"),
            "employee_id": request.form.get("employee_id"),
            "leave_type": request.form.get("leave_type"),
            "start_date": request.form.get("start_date"),
            "end_date": request.form.get("end_date"),
            "reason": request.form.get("reason"),
            "contact_info": request.form.get("contact_info")
        }
        
        # Process or save `leave_data` as needed

        flash("Leave request submitted successfully!")
        return redirect(url_for("emp_services.html"))

    return render_template("leave_request.html")

@app.route('/capture_images', methods=['POST', 'GET'])
def capture_images():
    if request.method == 'GET':
        # Example: Fetch the employee name from DB (you can modify the logic)
        conn = sqlite3.connect('employees.db')
        cursor = conn.cursor()
        employee_id = 1  # Example employee_id, replace with actual logic
        cursor.execute("SELECT First_name, Last_name FROM employees WHERE id = ?", (employee_id,))
        r = cursor.fetchone()
        
        # Return a valid response with the image stream
        return Response(capture_image_stream(str(r)), mimetype='multipart/x-mixed-replace; boundary=frame')


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

if __name__ == "__main__":
    app.run(debug=True)
