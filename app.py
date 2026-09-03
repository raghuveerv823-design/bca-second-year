
import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, session

app = Flask(__name__)
app.secret_key = 'bca_second_year_secret_key'

ADMIN_PASSWORD = "veerji9301"
SOLUTIONS_FOLDER = 'solutions'

# All 8 BCA 2nd Year Subjects Mapping
SUBJECTS = {
    "data_comm": "1. Data Communication and Computer Network (Core-4)",
    "dbms": "2. Database Management Systems Using PL/SQL (Core-5)",
    "computer_graphics": "3. Computer Graphics (DSE-1(A))",
    "python": "4. Python Programming (DSE-2(A))",
    "optimization": "5. Optimization Technique (M-3)",
    "artificial_intelligence": "6. Artificial Intelligence (M-4)",
    "web_designing": "7. Web Designing (MD-2)",
    "ecommerce": "8. E-Commerce (SEC)"
}

# Create main solutions folder and subfolders for each subject
os.makedirs(SOLUTIONS_FOLDER, exist_ok=True)
for subj_key in SUBJECTS.keys():
    os.makedirs(os.path.join(SOLUTIONS_FOLDER, subj_key), exist_ok=True)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/syllabus')
def syllabus():
    return render_template('syllabus.html')

@app.route('/solutions')
def solutions():
    # Gather files grouped by subject
    subjects_data = {}
    for subj_key, subj_name in SUBJECTS.items():
        subj_path = os.path.join(SOLUTIONS_FOLDER, subj_key)
        files = os.listdir(subj_path) if os.path.exists(subj_path) else []
        subjects_data[subj_key] = {
            'name': subj_name,
            'files': files
        }
    return render_template('solutions.html', subjects_data=subjects_data)

@app.route('/solutions/<subject>/<filename>')
def uploaded_file(subject, filename):
    subj_path = os.path.join(SOLUTIONS_FOLDER, subject)
    return send_from_directory(subj_path, filename)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    message = ""
    if request.method == 'POST':
        password = request.form.get('password')
        
        if password == ADMIN_PASSWORD:
            session['logged_in'] = True
        elif not session.get('logged_in') and password:
            return render_template('admin_login.html', error="Wrong Password!", subjects=SUBJECTS)

        if session.get('logged_in'):
            subject = request.form.get('subject')
            if 'file' in request.files and subject in SUBJECTS:
                file = request.files['file']
                if file and file.filename != '':
                    subj_dir = os.path.join(SOLUTIONS_FOLDER, subject)
                    filepath = os.path.join(subj_dir, file.filename)
                    file.save(filepath)
                    message = f"Solution PDF successfully uploaded to {SUBJECTS[subject]}!"

            return render_template('admin_dashboard.html', subjects=SUBJECTS, message=message)

    if session.get('logged_in'):
        return render_template('admin_dashboard.html', subjects=SUBJECTS)
        
    return render_template('admin_login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('admin'))

if __name__ == '__main__':
    app.run(debug=True)
    
