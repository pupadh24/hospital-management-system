from flask import Flask, render_template, request, redirect, session
import mysql.connector
import os
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()

db_config = {
    'host': os.getenv('DB_HOST'),
    'port': int(os.getenv('DB_PORT')),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME')
}

app.secret_key = os.getenv('SECRET_KEY')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        user = request.form['username']
        pw = request.form['password']
        name = request.form['name']
        dob = request.form['dob']
        blood = request.form['blood']
        phone = request.form['phone']
        
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        sql = "INSERT INTO patients (username, password, full_name, dob, blood_group, emergency_contact) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (user, pw, name, dob, blood, phone))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect('/login')
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['username']
        pw = request.form['password']
        
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        cursor.execute("SELECT id, full_name FROM patients WHERE username = %s AND password = %s", (user, pw))
        patient = cursor.fetchone()
        if patient:
            session['loggedin'], session['user_id'], session['name'], session['role'] = True, patient[0], patient[1], 'patient'
            return redirect('/')

        cursor.execute("SELECT id, name FROM doctors WHERE username = %s AND password = %s", (user, pw))
        doctor = cursor.fetchone()
        if doctor:
            session['loggedin'], session['user_id'], session['name'], session['role'] = True, doctor[0], doctor[1], 'doctor'
            return redirect('/doctor_dash')

        cursor.execute("SELECT id, full_name FROM admins WHERE username = %s AND password = %s", (user, pw))
        admin = cursor.fetchone()
        if admin:
            session['loggedin'], session['user_id'], session['name'], session['role'] = True, admin[0], admin[1], 'admin'
            return redirect('/admin_dashboard')

        return "Invalid credentials"
    return render_template('login.html')

@app.route('/')
def index():
    if not session.get('loggedin'):
        return redirect('/login')
    if session.get('role') != 'patient':
        return redirect('/login')
    
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM patients WHERE id = %s", (session['user_id'],))
    patient_info = cursor.fetchone()
    
    sql = """
        SELECT a.id, a.appointment_date, d.name, d.specialization 
        FROM appointments a
        JOIN doctors d ON a.doctor_id = d.id
        WHERE a.patient_id = %s
        ORDER BY a.appointment_date ASC"""
    
    cursor.execute(sql, (session['user_id'],))
    my_appts = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template('index.html', p=patient_info, appointments=my_appts)

@app.route('/book', methods=['GET', 'POST'])
def book():
    if not session.get('loggedin'):
        return redirect('/login')
    if session.get('role') != 'patient':
        return redirect('/login')

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    if request.method == 'POST':
        doc_id = request.form['doctor_id']
        date = request.form['date']
        time = request.form['time']
        pat_id = session['user_id']
        full_datetime = f"{date} {time}"
        
        cursor.execute("INSERT INTO appointments (patient_id, doctor_id, appointment_date) VALUES (%s, %s, %s)", (pat_id, doc_id, full_datetime))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect('/')

    cursor.execute("SELECT id, name, specialization FROM doctors")
    all_doctors = cursor.fetchall()

    selected_date = request.args.get('date')
    selected_doc = request.args.get('doctor_id')
    
    slots = []
    for hour in range(8, 17):
        slots.append(f"{hour:02d}:00")
        slots.append(f"{hour:02d}:30")

    if selected_date and selected_doc:
        cursor.execute("SELECT DATE_FORMAT(appointment_date, '%H:%i') FROM appointments WHERE doctor_id = %s AND DATE(appointment_date) = %s", (selected_doc, selected_date))
        raw_booked = cursor.fetchall()
        
        booked_slots = []
        for row in raw_booked:
            booked_slots.append(row[0])
            
        available_slots = []
        for s in slots:
            if s not in booked_slots:
                available_slots.append(s)
        slots = available_slots

    cursor.close()
    conn.close()
    return render_template('book.html', doctors=all_doctors, slots=slots, selected_date=selected_date, selected_doc=selected_doc)

@app.route('/cancel/<int:appointment_id>')
def cancel_appointment(appointment_id):
    if not session.get('loggedin'):
        return redirect('/login')
        
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    
    user_role = session.get('role')
    user_id = session.get('user_id')

    if user_role == 'admin':
        cursor.execute("DELETE FROM appointments WHERE id = %s", (appointment_id,))
    elif user_role == 'patient':
        cursor.execute("DELETE FROM appointments WHERE id = %s AND patient_id = %s", (appointment_id, user_id))
    elif user_role == 'doctor':
        cursor.execute("DELETE FROM appointments WHERE id = %s AND doctor_id = %s", (appointment_id, user_id))
        
    conn.commit()
    cursor.close()
    conn.close()
    
    if user_role == 'doctor':
        return redirect('/doctor_dash')
    elif user_role == 'admin':
        return redirect('/admin_dashboard')
    return redirect('/')

@app.route('/doctor_dash')
def doctor_dash():
    if not session.get('loggedin'):
        return redirect('/login')
    if session.get('role') != 'doctor':
        return redirect('/login')
    
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    
    sql = """
        SELECT a.id, a.appointment_date, p.full_name, p.blood_group, p.emergency_contact 
        FROM appointments a
        JOIN patients p ON a.patient_id = p.id
        WHERE a.doctor_id = %s
        ORDER BY a.appointment_date ASC"""
    
    cursor.execute(sql, (session['user_id'],))
    my_appointments = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template('doctor_dash.html', appointments=my_appointments)

@app.route('/admin_dashboard')
def admin_dashboard():
    if not session.get('loggedin'):
        return redirect('/login')
    if session.get('role') != 'admin':
        return redirect('/login')

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    search_query = request.args.get('search')

    cursor.execute("SELECT id, name, specialization, contact, salary FROM doctors")
    all_doctors = cursor.fetchall()

    if search_query:
        sql = "SELECT id, full_name, username, blood_group FROM patients WHERE full_name LIKE %s OR id LIKE %s"
        formatted_query = f"%{search_query}%"
        cursor.execute(sql, (formatted_query, formatted_query))
    else:
        cursor.execute("SELECT id, full_name, username, blood_group FROM patients")
    all_patients = cursor.fetchall()

    cursor.execute("""
        SELECT a.id, a.appointment_date, p.full_name, d.name 
        FROM appointments a
        JOIN patients p ON a.patient_id = p.id
        JOIN doctors d ON a.doctor_id = d.id
        ORDER BY a.appointment_date DESC""")
    
    all_appointments = cursor.fetchall()

    cursor.close()
    conn.close()
    return render_template('admin_dash.html', doctors=all_doctors, patients=all_patients, appointments=all_appointments)

@app.route('/admin/delete/<string:user_type>/<int:user_id>')
def admin_delete_user(user_type, user_id):
    if not session.get('loggedin') or session.get('role') != 'admin':
        return redirect('/login')
        
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    
    if user_type == 'doctor':
        cursor.execute("DELETE FROM appointments WHERE doctor_id = %s", (user_id,))
        cursor.execute("DELETE FROM doctors WHERE id = %s", (user_id,))
    elif user_type == 'patient':
        cursor.execute("DELETE FROM appointments WHERE patient_id = %s", (user_id,))
        cursor.execute("DELETE FROM patients WHERE id = %s", (user_id,))
        
    conn.commit()
    cursor.close()
    conn.close()
    return redirect('/admin_dashboard')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(host='0.0.0.0', port=port)