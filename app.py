from flask import Flask,render_template,request,redirect
import sqlite3,os

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("login.html")

# LOGIN
@app.route("/login",methods=["POST"])
def login():
    role=request.form["role"]
    if role=="student":
        return redirect("/student")
    else:
        return redirect("/teacher")

# ---------------- STUDENT ----------------
@app.route('/student')
def student():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    # Attendance calculation
    cur.execute("SELECT present, total FROM attendance WHERE student_email=?", (session['email'],))
    row = cur.fetchone()

    if row:
        present, total = row
        percent = int((present / total) * 100)
    else:
        percent = 0

    # Events
    cur.execute("SELECT * FROM events")
    events = cur.fetchall()

    # Marks
    cur.execute("SELECT * FROM marks WHERE student_email=?", (session['email'],))
    marks = cur.fetchall()

    conn.close()

    return render_template(
        "student_dashboard.html",
        percent=percent,
        events=events,
        marks=marks
    )

# ---------------- TEACHER ----------------
@app.route("/teacher")
def teacher():
    return render_template("teacher_dashboard.html")

# ATTENDANCE
@app.route("/attendance",methods=["GET","POST"])
def attendance():
    conn=sqlite3.connect("database.db")
    cur=conn.cursor()

    cur.execute("SELECT * FROM students")
    students=cur.fetchall()

    if request.method=="POST":
        date=request.form["date"]
        for s in students:
            status=request.form.get(f"s{s[0]}")
            cur.execute("INSERT INTO attendance VALUES (?,?,?)",(s[0],date,status))
        conn.commit()

    conn.close()
    return render_template("attendance.html",students=students)
@app.route("/view_attendance")
def view_attendance():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM attendance")
    data = cur.fetchall()
    conn.close()
    return render_template("view_attendance.html", data=data)

# EVENTS
@app.route("/events",methods=["GET","POST"])
def events():
    conn=sqlite3.connect("database.db")
    cur=conn.cursor()

    if request.method=="POST":
        cur.execute(
            "INSERT INTO events(title,description,date) VALUES (?,?,?)",
            (request.form["title"],
             request.form["desc"],
             request.form["date"])
        )
        conn.commit()

    cur.execute("SELECT * FROM events")
    events=cur.fetchall()
    conn.close()
    return render_template("events.html",events=events)

# MARKS
@app.route("/add_marks",methods=["GET","POST"])
def add_marks():
    if request.method=="POST":
        conn=sqlite3.connect("database.db")
        cur=conn.cursor()
        cur.execute("INSERT INTO marks VALUES (?,?,?)",
                    (request.form["sid"],request.form["sub"],request.form["marks"]))
        conn.commit()
        conn.close()
    return render_template("add_marks.html")
@app.route("/cgpa")
def cgpa():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("SELECT subject, marks FROM marks WHERE student_id=1")
    rows = cur.fetchall()

    subjects = []
    total_points = 0

    for sub, mark in rows:
        if mark >= 90: gp = 10
        elif mark >= 80: gp = 9
        elif mark >= 70: gp = 8
        elif mark >= 60: gp = 7
        elif mark >= 50: gp = 6
        else: gp = 5

        subjects.append((sub, mark, gp))
        total_points += gp

    cgpa = round(total_points / len(subjects), 2) if subjects else 0

    conn.close()
    return render_template("cgpa.html", subjects=subjects, cgpa=cgpa)

# TIMETABLE
@app.route("/add_timetable", methods=["POST"])
def add_timetable():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO timetable VALUES (?,?,?)",
                (request.form["day"],
                 request.form["period"],
                 request.form["subject"]))
    conn.commit()
    conn.close()
    return redirect("/timetable")

# ALUMNI
@app.route("/alumni")
def alumni():
    conn=sqlite3.connect("database.db")
    cur=conn.cursor()
    cur.execute("SELECT * FROM alumni")
    data=cur.fetchall()
    conn.close()
    return render_template("alumni.html",data=data)

# TOP10
@app.route("/top10")
@app.route("/top10")
def top10():
    conn=sqlite3.connect("database.db")
    cur=conn.cursor()
    cur.execute("""
        SELECT student_id, SUM(marks) as total
        FROM marks
        GROUP BY student_id
        ORDER BY total DESC
        LIMIT 10
    """)
    data=cur.fetchall()
    conn.close()
    return render_template("top10.html",data=data)
@app.route("/add_alumni", methods=["GET","POST"])
def add_alumni():
    if request.method=="POST":
        conn=sqlite3.connect("database.db")
        cur=conn.cursor()
        cur.execute("INSERT INTO alumni VALUES (?,?,?)",
                    (request.form["name"],
                     request.form["package"],
                     request.form["year"]))
        conn.commit()
        conn.close()
    return render_template("add_alumni.html")

if __name__=="__main__":
    app.run()