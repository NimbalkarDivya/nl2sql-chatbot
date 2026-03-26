from vanna_setup import get_agent

# Initialize agent
agent = get_agent()

# ------------------ SAMPLE Q&A (for reference/testing) ------------------
examples = [
    ("How many patients do we have?",
     "SELECT COUNT(*) AS total_patients FROM patients"),

    ("List all doctors and their specializations",
     "SELECT name, specialization FROM doctors"),

    ("Show appointments for last month",
     "SELECT * FROM appointments WHERE appointment_date >= date('now','-1 month')"),

    ("Which doctor has the most appointments?",
     "SELECT doctor_id, COUNT(*) AS total FROM appointments GROUP BY doctor_id ORDER BY total DESC LIMIT 1"),

    ("What is total revenue?",
     "SELECT SUM(total_amount) FROM invoices"),

    ("Show revenue by doctor",
     """SELECT d.name, SUM(i.total_amount)
        FROM invoices i
        JOIN appointments a ON i.patient_id = a.patient_id
        JOIN doctors d ON d.id = a.doctor_id
        GROUP BY d.name"""),

    ("Which city has most patients?",
     "SELECT city, COUNT(*) FROM patients GROUP BY city ORDER BY COUNT(*) DESC LIMIT 1"),

    ("Show unpaid invoices",
     "SELECT * FROM invoices WHERE status != 'Paid'"),

    ("Top 5 patients by spending",
     """SELECT p.first_name, p.last_name, SUM(i.total_amount) AS total
        FROM patients p
        JOIN invoices i ON p.id = i.patient_id
        GROUP BY p.id
        ORDER BY total DESC LIMIT 5"""),

    ("Average treatment cost",
     "SELECT AVG(cost) FROM treatments"),

    ("Appointments count by month",
     """SELECT strftime('%Y-%m', appointment_date) AS month, COUNT(*)
        FROM appointments GROUP BY month"""),

    ("Patients with more than 3 visits",
     """SELECT patient_id, COUNT(*) as visits
        FROM appointments
        GROUP BY patient_id
        HAVING visits > 3"""),

    ("No-show percentage",
     """SELECT 
        (COUNT(CASE WHEN status='No-Show' THEN 1 END) * 100.0 / COUNT(*)) 
        FROM appointments"""),

    ("Average appointment duration by doctor",
     """SELECT doctor_id, AVG(duration_minutes)
        FROM treatments
        JOIN appointments ON treatments.appointment_id = appointments.id
        GROUP BY doctor_id"""),

    ("Patients with overdue invoices",
     """SELECT p.first_name, p.last_name
        FROM patients p
        JOIN invoices i ON p.id = i.patient_id
        WHERE i.status='Overdue'""")
]

# ------------------ DISPLAY / VERIFY ------------------
print("✅ Agent initialized successfully")
print(f"📊 Loaded {len(examples)} reference Q&A pairs")

print("\n📌 Sample Questions:")
for i, (q, _) in enumerate(examples[:5], 1):
    print(f"{i}. {q}")

print("\n⚠️ Note:")
print("This Vanna version does not support manual memory seeding.")
print("The agent will learn dynamically during usage.")

print("\n🚀 You can now start FastAPI and test queries!")