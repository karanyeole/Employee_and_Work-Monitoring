from flask import Flask, render_template
app=Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/faq')
def faq():
    return render_template('faq.html')

@app.route('/gallary')
def gallary():
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
if __name__=="__main__":
    app.run(debug=True)
