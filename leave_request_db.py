import sqlite3

# Function to initialize the database and create the table
def init_leave_requests_db():
    # Connect to the SQLite database (it will create the database if it doesn't exist)
    conn = sqlite3.connect('leave_requests.db')

    # Create a cursor object
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

# Initialize the database (this will create the table if it doesn't exist)
init_leave_requests_db()
