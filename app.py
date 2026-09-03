from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__, template_folder='templates', static_folder='templates')
app.secret_key = 'bca_secret_key'  # Session secure rakhne ke liye

# Admin ka password (aap ise apne hisab se badal sakte hain)
ADMIN_PASSWORD = "admin123"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/syllabus')
def syllabus():
    return render_template('syllabus.html')

# Admin Login Route
@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        password = request.form.get('password')
        if password == ADMIN_PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            return render_template('admin_login.html', error="Galat Password! Dobara koshish karein.")
    return render_template('admin_login.html')

# Admin Dashboard Route (Jahan se PDF upload hogi)
@app.route('/admin/dashboard', methods=['GET', 'POST'])
def admin_dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('admin_login'))
    
    if request.method == 'POST':
        if 'pdf_file' in request.files:
            file = request.files['pdf_file']
            if file.filename != '':
                # File ko seedha templates folder mein save kar denge
                file.save(os.path.join('templates', file.filename))
                return render_template('admin_dashboard.html', success="PDF Safalpurvak Upload Ho Gayi!")
                
    return render_template('admin_dashboard.html')

# Logout Route
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('admin_login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
  
