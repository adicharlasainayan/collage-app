import sqlite3

conn = sqlite3.connect('database.db')
cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS students(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,email TEXT,password TEXT)''')

cur.execute('''CREATE TABLE IF NOT EXISTS teachers(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,email TEXT,password TEXT)''')

cur.execute('''CREATE TABLE IF NOT EXISTS attendance(
student_id INTEGER,date TEXT,status TEXT,late INTEGER)''')

cur.execute('''CREATE TABLE IF NOT EXISTS marks(
student_id INTEGER,subject TEXT,marks INTEGER,credit INTEGER)''')

cur.execute('''CREATE TABLE IF NOT EXISTS alumni(
name TEXT,year TEXT,department TEXT,package INTEGER)''')

cur.execute('''CREATE TABLE IF NOT EXISTS events(
title TEXT,date TEXT,description TEXT)''')

# test users
cur.execute("INSERT INTO students (name,email,password) VALUES ('Sainayan','adicharlasainayan@gmail.com','1234')")
cur.execute("INSERT INTO teachers (name,email,password) VALUES ('Abhinav','pullemlaabhinav@gmail.com','1234')")

conn.commit()
conn.close()