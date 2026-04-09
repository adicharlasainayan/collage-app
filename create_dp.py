import sqlite3
import os

DB_PATH = "database.db"

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# ------------------ STUDENTS ------------------
cur.execute("""
CREATE TABLE IF NOT EXISTS students(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT UNIQUE,
    password TEXT,
    branch TEXT,
    year INTEGER
)
""")

# ------------------ TEACHERS ------------------
cur.execute("""
CREATE TABLE IF NOT EXISTS teachers(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT UNIQUE,
    password TEXT,
    subject TEXT
)
""")

# ------------------ ATTENDANCE ------------------
cur.execute("""
CREATE TABLE IF NOT EXISTS attendance(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    date TEXT,
    status TEXT,
    FOREIGN KEY(student_id) REFERENCES students(id)
)
""")

# ------------------ EVENTS / HOLIDAYS ------------------
cur.execute("""
CREATE TABLE IF NOT EXISTS events(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    description TEXT,
    date TEXT
)
""")

# ------------------ MARKS ------------------
cur.execute("""
CREATE TABLE IF NOT EXISTS marks(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    subject TEXT,
    marks INTEGER,
    FOREIGN KEY(student_id) REFERENCES students(id)
)
""")

# ------------------ TIMETABLE ------------------
cur.execute("""
CREATE TABLE IF NOT EXISTS timetable(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    day TEXT,
    period TEXT,
    subject TEXT,
    teacher TEXT
)
""")

# ------------------ PASSED OUT STUDENTS + PACKAGE ------------------
cur.execute("""
CREATE TABLE IF NOT EXISTS passed_out(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    branch TEXT,
    package REAL,
    year INTEGER
)
""")

conn.commit()
conn.close()

print("All tables created successfully ✅")