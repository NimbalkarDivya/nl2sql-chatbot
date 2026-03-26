import sqlite3
import random
from datetime import datetime, timedelta
from faker import Faker

fake = Faker()

conn = sqlite3.connect("clinic.db")
cursor = conn.cursor()

# ------------------ TABLES ------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS patients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT,
    last_name TEXT,
    email TEXT,
    phone TEXT,
    date_of_birth DATE,
    gender TEXT,
    city TEXT,
    registered_date DATE
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS doctors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    specialization TEXT,
    department TEXT,
    phone TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS appointments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER,
    doctor_id INTEGER,
    appointment_date DATETIME,
    status TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS treatments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    appointment_id INTEGER,
    treatment_name TEXT,
    cost REAL,
    duration_minutes INTEGER
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS invoices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER,
    invoice_date DATE,
    total_amount REAL,
    paid_amount REAL,
    status TEXT
)
""")

# ------------------ DATA ------------------

cities = ["Pune", "Mumbai", "Delhi", "Nagpur", "Nashik", "Bangalore", "Hyderabad"]
specializations = ["Dermatology", "Cardiology", "Orthopedics", "General", "Pediatrics"]

# Doctors
for _ in range(15):
    cursor.execute("INSERT INTO doctors (name, specialization, department, phone) VALUES (?, ?, ?, ?)",
                   (fake.name(), random.choice(specializations), "Dept", fake.phone_number()))

# Patients
for _ in range(200):
    cursor.execute("""
    INSERT INTO patients (first_name, last_name, email, phone, date_of_birth, gender, city, registered_date)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        fake.first_name(),
        fake.last_name(),
        fake.email() if random.random() > 0.2 else None,
        fake.phone_number() if random.random() > 0.2 else None,
        fake.date_of_birth(),
        random.choice(["M", "F"]),
        random.choice(cities),
        fake.date_between(start_date='-1y', end_date='today')
    ))

# Appointments
for _ in range(500):
    cursor.execute("""
    INSERT INTO appointments (patient_id, doctor_id, appointment_date, status)
    VALUES (?, ?, ?, ?)
    """, (
        random.randint(1, 200),
        random.randint(1, 15),
        fake.date_time_between(start_date='-1y', end_date='now'),
        random.choice(["Scheduled", "Completed", "Cancelled", "No-Show"])
    ))

# Treatments
for _ in range(350):
    cursor.execute("""
    INSERT INTO treatments (appointment_id, treatment_name, cost, duration_minutes)
    VALUES (?, ?, ?, ?)
    """, (
        random.randint(1, 500),
        fake.word(),
        random.uniform(50, 5000),
        random.randint(10, 120)
    ))

# Invoices
for _ in range(300):
    total = random.uniform(100, 5000)
    paid = total if random.random() > 0.3 else random.uniform(0, total)

    cursor.execute("""
    INSERT INTO invoices (patient_id, invoice_date, total_amount, paid_amount, status)
    VALUES (?, ?, ?, ?, ?)
    """, (
        random.randint(1, 200),
        fake.date_between(start_date='-1y', end_date='today'),
        total,
        paid,
        "Paid" if paid == total else random.choice(["Pending", "Overdue"])
    ))

conn.commit()
conn.close()

print("Database created successfully!")