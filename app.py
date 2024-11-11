
from flask import Flask, render_template, request, redirect, url_for, flash
import secrets
import os
import cv2
import time
from capture_img import capture

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
        conn = sqlite3.connect('employees.db')
        name = first_name
        name1 =last_name
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO employees (
                first_name, last_name, dob, gender, email, phone, address,
                job_title, department, salary, emergency_contact_name, emergency_contact_phone
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (first_name, last_name, dob, gender, email, phone, address, job_title, department, salary, emergency_contact_name, emergency_contact_phone))
        conn.commit()
        conn.close()
        employee_id = cursor.lastrowid
        print(employee_id)

        
        flash("Employee added successfully!")
        return redirect(url_for("hr_services"))

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
        return redirect(url_for("hr_services.html"))

    return render_template("leave_request.html")

@app.route('/capture_images', methods=['POST'])
def capture_images():
    if request.method == 'POST':
        conn = sqlite3.connect('employees.db')
        cursor = conn.cursor()
        # Query to fetch First_name and Last_name where ID is 1
        cursor.execute("SELECT First_name, Last_name FROM employees WHERE id = ?", (employee_id,))

        # Fetch the result
        r = cursor.fetchone() # Example of how the name might be passed.
        result = capture(str(r))  # Call the capture_image function with the user's name.
        flash(result)  # Flash the result to the user
        return redirect('/hr_services')  # Redirect to the page after the image capture


if __name__ == "__main__":
    app.run(debug=True)
