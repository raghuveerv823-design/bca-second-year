import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, session

app = Flask(__name__)
app.secret_key = 'bca_second_year_secret_key'

ADMIN_PASSWORD = "veerji9301"
SOLUTIONS_FOLDER = 'solutions'
os.makedirs(SOLUTIONS_FOLDER, exist_ok=True)
app.config['SOLUTIONS_FOLDER'] = SOLUTIONS_FOLDER

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/syllabus')
def syllabus():
    return render_template('syllabus.html')

@app.route('/solutions')
def solutions():
    files = os.listdir(app.config['SOLUTIONS_FOLDER'])
    return render_template('solutions.html', files=files)

@app.route('/solutions/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['SOLUTIONS_FOLDER'], filename)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    message = ""
    if request.method == 'POST':
        password = request.form.get('password')
        if password == ADMIN_PASSWORD:
            session['logged_in'] = True
        elif not session.get('logged_in'):
            return render_template('admin_login.html', error="Wrong Password!")

        if session.get('logged_in') and 'file' in request.files:
            file = request.files['file']
            if file and file.filename != '':
                filepath = os.path.join(app.config['SOLUTIONS_FOLDER'], file.filename)
                file.save(filepath)
                message = "Solution PDF uploaded successfully!"

        if session.get('logged_in'):
            return render_template('admin_dashboard.html', message=message)

    if session.get('logged_in'):
        return render_template('admin_dashboard.html')
        
    return render_template('admin_login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('admin'))

if __name__ == '__main__':
    app.run(debug=True)
    
