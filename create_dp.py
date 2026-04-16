import sqlite3

conn = sqlite3.connect("database.db")
cur = conn.cursor()

conn.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT,
    password TEXT,
    role TEXT
)
""")

# Default users
conn.execute("INSERT INTO users (email,password,role) VALUES ('adicharlasainayan@gmail.com','1234','student')")
conn.execute("INSERT INTO users (email,password,role) VALUES ('pullemlaabhinav@gmail.com','1234','teacher')")
conn.commit()

# STUDENTS
cur.execute("""
CREATE TABLE IF NOT EXISTS students(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
email TEXT,
parent_email TEXT
)
""")

# ATTENDANCE
cur.execute("""
CREATE TABLE IF NOT EXISTS attendance(
student_id INTEGER,
date TEXT,
status TEXT
)
""")

# EVENTS
cur.execute("""
CREATE TABLE IF NOT EXISTS events(
id INTEGER PRIMARY KEY AUTOINCREMENT,
title TEXT,
description TEXT,
date TEXT
)
""")

# MARKS
cur.execute("""
CREATE TABLE IF NOT EXISTS marks(
student_id INTEGER,
subject TEXT,
marks INTEGER
)
""")

# TIMETABLE
cur.execute("""
CREATE TABLE IF NOT EXISTS timetable(
day TEXT,
period TEXT,
subject TEXT
)
""")

# ALUMNI
cur.execute("""
CREATE TABLE IF NOT EXISTS alumni(
name TEXT,
package TEXT,
year TEXT
)
""")

conn.commit()
conn.close()
print("All tables created")