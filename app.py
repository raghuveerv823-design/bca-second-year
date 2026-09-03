
from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__, template_folder='templates', static_folder='templates')
app.secret_key = 'bca_secret_key_veer'

# Naya Admin Password
ADMIN_PASSWORD = "veerji9301"

# 8 Subjects ki list
SUBJECTS = {
    'network': 'Data Communication and Computer Networks',
    'dbms': 'Database Management Systems Using PL/SQL',
    'graphics': 'Computer Graphics',
    'python': 'Python Programming',
    'optimization': 'Optimization Technique',
    'ai': 'Artificial Intelligence',
    'web': 'Web Designing',
    'ecommerce': 'E-Commerce'
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/syllabus')
def syllabus():
    return render_template('syllabus.html')

# Public Solutions & Notes Page (Subject-wise subheadings)
@app.route('/solutions')
def solutions():
    sol_dir = os.path.join('templates', 'solutions')
    if not os.path.exists(sol_dir):
        os.makedirs(sol_dir)
    
    files = os.listdir(sol_dir)
    
    # Files ko unke subject ke hisab se group karna
    categorized = {k: [] for k in SUBJECTS.keys()}
    for f in files:
        for code in SUBJECTS.keys():
            if f.startswith(code + '_'):
                categorized[code].append(f)
                
    return render_template('solutions.html', subjects=SUBJECTS, categorized=categorized)

# Private Admin Login Page (Solutions & Notes Admin)
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

# Admin Dashboard (Subject select karke PDF upload karne ke liye)
@app.route('/admin/dashboard', methods=['GET', 'POST'])
def admin_dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('admin_login'))
    
    sol_dir = os.path.join('templates', 'solutions')
    if not os.path.exists(sol_dir):
        os.makedirs(sol_dir)
        
    if request.method == 'POST':
        subject_code = request.form.get('subject')
        if 'pdf_file' in request.files and subject_code in SUBJECTS:
            file = request.files['pdf_file']
            if file.filename != '':
                # File name ke aage subject code jod kar save karenge
                filename = f"{subject_code}_{file.filename}"
                file.save(os.path.join(sol_dir, filename))
                return render_template('admin_dashboard.html', subjects=SUBJECTS, success="Solution/Note Safalpurvak Upload Ho Gaya!")
                
    return render_template('admin_dashboard.html', subjects=SUBJECTS)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('admin_login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    
