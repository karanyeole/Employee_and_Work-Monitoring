from flask import Flask, render_template, request, redirect, url_for, flash, Response, jsonify
import secrets
import os
from collections import defaultdict
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename
import threading
import shutil
from capture_img import capture_image_stream, create_face_database
from try1 import load_known_faces, recognize_faces_from_webcam

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
employee_id = None
is_running = False
recognition_thread = None

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
        contact_info TEXT NOT NULL,
        status BOOLEAN
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
            emergency_contact_phone TEXT,
            Password TEXT
        )
    ''')
    conn.commit()
    conn.close()


init_db()
init_leave_requests_db()

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
        password = request.form['password']

        # Connect to the database
        conn = sqlite3.connect('employees.db')
        cursor = conn.cursor()

        # Check if the email already exists
        cursor.execute("SELECT COUNT(*) FROM employees WHERE email = ?", (email,))
        email_exists = cursor.fetchone()[0]


        if email_exists > 0:
            conn.close()
            return jsonify({"success": False, "message": "Email must be unique"})
        # Check if the email already exists


        cursor.execute("SELECT COUNT(*) FROM employees WHERE first_name = ? and last_name=? ", (first_name,last_name,))
        name = cursor.fetchone()[0]

        if name > 0:
            conn.close()
            return jsonify({"success": False, "message": "name already exists, must be unique"})

        # Insert the new employee
        cursor.execute('''
            INSERT INTO employees (
                first_name, last_name, dob, gender, email, phone, address,
                job_title, department, salary, emergency_contact_name, emergency_contact_phone, password
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (first_name, last_name, dob, gender, email, phone, address, job_title, department, salary,
              emergency_contact_name, emergency_contact_phone, password))

        # Commit and get the generated employee_id
        conn.commit()
        employee_id = cursor.lastrowid
        conn.close()

        # Return a JSON response with the employee_id
        return jsonify({"success": True, "employee_id": employee_id})

    return render_template("add_employee.html")


@app.route('/capture_images', methods=['POST'])
def capture_images():
    if 'image' not in request.files:
        return jsonify({"error": "No image file in the request"}), 400
    image_file = request.files['image']
    if image_file:
        conn = sqlite3.connect('employees.db')
        cursor = conn.cursor()
        cursor.execute("SELECT First_name, Last_name FROM employees WHERE id = ?", (employee_id,))
        r = cursor.fetchone()
        r = r[0] + r[1]
        output_folder = os.path.join("employee_images", r)
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = secure_filename(f"image_{timestamp}.png")
        filepath = os.path.join(output_folder, filename)
        image_file.save(filepath)
        return jsonify({"message": f"Image saved as {filename}"}), 200

    return jsonify({"error": "Failed to save image"}), 500


# Rename the leave_request function for employees
@app.route('/leave_request', methods=['GET', 'POST'])
def leave_request():
    if request.method == 'POST':
        # Get the form data
        leave_type = request.form['leave_type']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        reason = request.form['reason']
        conn = sqlite3.connect('employees.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM employees WHERE id = ?", (employee_id,))
        employees = cursor.fetchone()
        employee_name=employees[1]+employees[2]
        contact_info=employees[6]
        # Insert the data into the database

        conn = sqlite3.connect('leave_requests.db')
        c = conn.cursor()
        c.execute('''
            INSERT INTO leave_requests (employee_name, employee_id, leave_type, start_date, end_date, reason, contact_info,status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (employee_name, employee_id, leave_type, start_date, end_date, reason,contact_info, False,))
        conn.commit()
        conn.close()

        # Redirect to a success page or return a success message
        return render_template('leave_request_success.html', message="Leave request submitted successfully!")

    return render_template('leave_request.html')


# Rename the leave_request function for HR leave requests
@app.route('/leave_request_hr', methods=['GET', 'POST'])
def leave_request_hr():
    conn = sqlite3.connect('leave_requests.db')
    cursor = conn.cursor()
    # For GET request, fetch leave requests from the database
    cursor.execute("SELECT * FROM leave_requests where status=0")
    leave_requests = cursor.fetchall()
    conn.close()

    return render_template("leave_request_hr.html", leave_requests=leave_requests)



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
        ''', (first_name, last_name, dob, gender, email, phone, address, job_title, department, salary,
              emergency_contact_name, emergency_contact_phone, employee_id))
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
    cursor.execute("SELECT First_name, Last_name FROM employees WHERE id = ?", (employee_id,))
    result = cursor.fetchone()
    if result:
        name = result[0] + result[1]
        employee = os.path.join("employee_images", name)
        if os.path.exists(employee):
            try:
                set_permissions(employee)  # Ensure write permissions
                shutil.rmtree(employee)
            except Exception as e:
                flash(f"Error deleting folder: {str(e)}")
                return redirect(url_for('manage_employees'))
        cursor.execute("DELETE FROM employees WHERE id=?", (employee_id,))
        conn.commit()
        flash("Employee deleted successfully!")
    else:
        flash("Employee not found.")
    conn.close()
    return redirect(url_for('manage_employees'))

def set_permissions(folder_path):
    import stat
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            os.chmod(file_path, stat.S_IWRITE)  # Set write permissions
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            os.chmod(dir_path, stat.S_IWRITE)
    os.chmod(folder_path, stat.S_IWRITE)


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


@app.route('/employee')
def view_employee():
    # Connect to the database and fetch employee details
    conn = sqlite3.connect('employees.db')
    global employee_id
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
    global employee_id
    data = request.get_json()
    email = data.get("email")
    employee_id = data.get("password")  # Assume employee ID is being used as the password

    # Connect to the database
    conn = sqlite3.connect('employees.db')
    cursor = conn.cursor()
    # Query to check if the email and employee_id match
    cursor.execute("SELECT * FROM employees WHERE email = ? AND password = ?", (email, employee_id))
    employee = cursor.fetchone()
    conn.close()
    print(employee)
    if employee:
        employee_id=employee[0]
        return jsonify({"success": True})  # Matching record found
    else:
        return jsonify({"success": False})  # No matching record

@app.route('/start_work')
def start_work():
    return render_template("start_work.html")


@app.route('/start_it', methods=['POST'])
def start_it():
    global is_running, recognition_thread
    conn = sqlite3.connect('employees.db')
    cursor = conn.cursor()
    cursor.execute("SELECT first_name, last_name FROM employees WHERE id = ?", (employee_id,))
    employees = cursor.fetchone()
    employee=employees[0]+employees[1]
    employee = os.path.join("employee_images",employee)
    conn.close()

    if is_running:
        return jsonify({"status": "Already running"})

    is_running = True
    known_encodings, known_names,k = load_known_faces(employee)
    k = os.path.join(k,"report.db")
    recognition_thread = threading.Thread(target=recognize_faces_from_webcam, args=(known_encodings, known_names, lambda: is_running,k))
    recognition_thread.start()

    return jsonify({"status": "Started"})

@app.route('/end_it', methods=['POST'])
def end_it():
    global is_running
    if not is_running:
        return jsonify({"status": "Not running"})

    is_running = False
    return jsonify({"status": "Stopped"})

# Route to display leave requests
DATABASE = 'leave_requests.db'

def get_db_connection():
    conn = sqlite3.connect('leave_requests.db')  # Your SQLite database file
    conn.row_factory = sqlite3.Row  # This allows us to return rows as dictionaries
    return conn

# Route to display HR dashboard with leave requests
@app.route('/dashboard')
def hr_dashboard():
    conn = get_db_connection()
    leave_requests = conn.execute('SELECT * FROM leave_requests').fetchall()  # Ensure this matches your table name
    conn.close()
    return render_template('leave_request_hr.html', leave_requests=leave_requests)


@app.route("/work_insights")
def work_insights():
    conn = sqlite3.connect('employees.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, first_name, last_name, email, department FROM employees')
    employee_list=cursor.fetchall()
    return render_template('work_insights.html', employee_list=employee_list)



@app.route('/show_report/<int:employee_id>', methods=['GET', 'POST'])
def show_report(employee_id):
    conn = sqlite3.connect('employees.db')
    cursor = conn.cursor()

    # Fetch the employee's first and last name from the database
    cursor.execute("SELECT First_name, Last_name FROM employees WHERE id = ?", (employee_id,))
    result = cursor.fetchone()
    name = result[0] + result[1]
    employee = os.path.join("employee_images", name)
    employee = os.path.join(employee, "report.db")
    conn = sqlite3.connect(employee)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM report")
    data = cursor.fetchall()

    # Group data by date
    grouped_data = defaultdict(list)
    for row in data:
        grouped_data[row[0]].append(row[1:])

    # Determine the selected date (default to current date)
    current_date = datetime.now().strftime('%Y-%m-%d')
    selected_date = request.form.get('selected_date', current_date)

    # Filter data for the selected date
    filtered_data = grouped_data.get(selected_date, [])

    return render_template('show_report.html', grouped_data={selected_date: filtered_data}, current_date=current_date, selected_date=selected_date)


@app.route('/approve/<int:employee_id>', methods=['GET', 'POST'])
def approve(employee_id):
    conn = sqlite3.connect('leave_requests.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE leave_requests SET status = ? WHERE employee_id = ?", (1 , employee_id ))
    cursor.execute("SELECT * FROM leave_requests where status=0")
    leave_requests = cursor.fetchall()
    conn.close()
    return render_template("leave_request_hr.html", leave_requests=leave_requests)



@app.route('/reject/<int:employee_id>', methods=['GET', 'POST'])
def reject(employee_id):
    pass
if __name__ == "__main__":
    app.run(debug=True)
