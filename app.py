import os

if not os.path.exists("database.db"):
    import create_db
from flask import Flask, render_template, request
import sqlite3, smtplib
from datetime import datetime

app = Flask(__name__)
@app.route("/")
def home():
    return render_template("login.html")

# ---------- EMAIL FUNCTION ----------
def send_mail(to_email, msg):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login('yourmail@gmail.com', 'your_app_password')
        server.sendmail('yourmail@gmail.com', to_email, msg)
        server.quit()
    except:
        print("Mail failed")

# ---------- LOGIN ----------
@app.route('/', methods=['GET','POST'])
def login():
    if request.method=='POST':
        email=request.form['email']
        password=request.form['password']
        role=request.form['role']

        conn=sqlite3.connect('database.db')
        cur=conn.cursor()

        if role=='student':
            cur.execute("SELECT id FROM students WHERE email=? AND password=?",(email,password))
            data=cur.fetchone()
            if data:
                return render_template('student_dashboard.html',sid=data[0])

        if role=='teacher':
            cur.execute("SELECT * FROM teachers WHERE email=? AND password=?",(email,password))
            if cur.fetchone():
                return render_template('teacher_dashboard.html')

        return "Invalid Details"
    return render_template('login.html')

# ---------- BULK ATTENDANCE + EMAIL ----------
@app.route('/attendance',methods=['GET','POST'])
def attendance():
    conn=sqlite3.connect('database.db')
    cur=conn.cursor()

    if request.method=='POST':
        date=request.form['date']
        cur.execute("SELECT id,email FROM students")
        students=cur.fetchall()

        for s in students:
            sid=s[0]
            email=s[1]
            status=request.form.get(f'status_{sid}')
            late=request.form.get(f'late_{sid}')

            cur.execute("INSERT INTO attendance VALUES (?,?,?,?)",(sid,date,status,late))

            if late=='1':
                send_mail(email,"You were marked LATE today.")

        conn.commit()
        conn.close()
        return "Attendance Marked"

    cur.execute("SELECT id,name FROM students")
    students=cur.fetchall()
    conn.close()
    return render_template('attendance.html',students=students)

# ---------- VIEW ATTENDANCE % + ALERT ----------
@app.route('/view_attendance/<int:sid>')
def view_attendance(sid):
    conn=sqlite3.connect('database.db')
    cur=conn.cursor()

    cur.execute("SELECT COUNT(*) FROM attendance WHERE student_id=?",(sid,))
    total=cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM attendance WHERE student_id=? AND status='Present'",(sid,))
    present=cur.fetchone()[0]

    percent= round((present/total)*100,2) if total>0 else 0

    cur.execute("SELECT email FROM students WHERE id=?",(sid,))
    email=cur.fetchone()[0]

    if percent<65:
        send_mail(email,"Warning! Attendance below 65%.")

    conn.close()
    return render_template('view_attendance.html',
                           present=present,total=total,percent=percent)

# ---------- ADD MARKS ----------
@app.route('/add_marks',methods=['GET','POST'])
def add_marks():
    if request.method=='POST':
        sid=request.form['sid']
        subject=request.form['subject']
        marks=request.form['marks']
        credit=request.form['credit']

        conn=sqlite3.connect('database.db')
        cur=conn.cursor()
        cur.execute("INSERT INTO marks VALUES (?,?,?,?)",(sid,subject,marks,credit))
        conn.commit()
        conn.close()
        return "Marks Added"
    return render_template('add_marks.html')

# ---------- STUDENT CGPA PAGE ----------
@app.route('/cgpa/<int:sid>')
def cgpa(sid):
    conn=sqlite3.connect('database.db')
    cur=conn.cursor()

    cur.execute("SELECT subject,marks,credit FROM marks WHERE student_id=?",(sid,))
    rows=cur.fetchall()

    total= sum(r[1]*r[2] for r in rows)
    credits= sum(r[2] for r in rows)
    cgpa= round(total/credits,2) if credits>0 else 0

    conn.close()
    return render_template('cgpa.html',rows=rows,cgpa=cgpa)

# ---------- TOP10 ----------
@app.route('/top10')
def top10():
    conn=sqlite3.connect('database.db')
    cur=conn.cursor()
    query="""
    SELECT students.name,
    SUM(marks*credit)/SUM(credit) as cgpa
    FROM marks
    JOIN students ON students.id=marks.student_id
    GROUP BY student_id
    ORDER BY cgpa DESC
    LIMIT 10
    """
    cur.execute(query)
    data=cur.fetchall()
    conn.close()
    return render_template('top10.html',data=data)

# ---------- ADD ALUMNI ----------
@app.route('/add_alumni',methods=['GET','POST'])
def add_alumni():
    if request.method=='POST':
        name=request.form['name']
        year=request.form['year']
        dept=request.form['dept']
        package=request.form['package']

        conn=sqlite3.connect('database.db')
        cur=conn.cursor()
        cur.execute("INSERT INTO alumni VALUES (?,?,?,?)",(name,year,dept,package))
        conn.commit()
        conn.close()
        return "Alumni Added"
    return render_template('add_alumni.html')

# ---------- VIEW ALUMNI ----------
@app.route('/alumni')
def alumni():
    conn=sqlite3.connect('database.db')
    cur=conn.cursor()
    cur.execute("SELECT * FROM alumni ORDER BY package DESC")
    data=cur.fetchall()
    conn.close()
    return render_template('alumni.html',data=data)

# ---------- EVENTS ----------
@app.route('/events', methods=['GET','POST'])
def events():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    if request.method == 'POST':
        title = request.form['title']
        desc  = request.form['desc']
        date  = request.form['date']

        cur.execute(
            "INSERT INTO events (title, description, date) VALUES (?,?,?)",
            (title, desc, date)
        )
        conn.commit()

    cur.execute("SELECT * FROM events ORDER BY date DESC")
    events = cur.fetchall()
    conn.close()

    return render_template('events.html', events=events)
# ---------- TIMETABLE (simple clash check) ----------
@app.route('/timetable',methods=['GET','POST'])
def timetable():
    conn=sqlite3.connect('database.db')
    cur=conn.cursor()

    if request.method=='POST':
        day=request.form['day']
        start=request.form['start']
        end=request.form['end']
        subject=request.form['subject']

        cur.execute("""SELECT * FROM timetable
                       WHERE day=? AND
                       (start_time < ? AND end_time > ?)""",
                       (day,end,start))
        if cur.fetchone():
            return "Time Clash Detected!"

        cur.execute("INSERT INTO timetable VALUES (?,?,?,?)",
                    (day,start,end,subject))
        conn.commit()

    cur.execute("SELECT * FROM timetable")
    data=cur.fetchall()
    conn.close()
    return render_template('timetable.html',data=data)


import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)