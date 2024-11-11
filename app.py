from flask import Flask, render_template, request, redirect, url_for, flash
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

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
        employee_data = {
            "first_name": request.form.get("first_name"),
            "last_name": request.form.get("last_name"),
            "dob": request.form.get("dob"),
            "gender": request.form.get("gender"),
            "email": request.form.get("email"),
            "phone": request.form.get("phone"),
            "address": request.form.get("address"),
            "job_title": request.form.get("job_title"),
            "department": request.form.get("department"),
            "salary": request.form.get("salary"),
            "emergency_contact_name": request.form.get("emergency_contact_name"),
            "emergency_contact_phone": request.form.get("emergency_contact_phone"),
        }
        
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
        return redirect(url_for("hr_services"))

    return render_template("leave_request.html")

if __name__ == "__main__":
    app.run(debug=True)
