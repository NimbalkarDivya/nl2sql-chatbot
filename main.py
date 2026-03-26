from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
import google.generativeai as genai
import os
from dotenv import load_dotenv
import time

# ---------------- LOAD ENV ----------------
load_dotenv()

# ---------------- GEMINI SETUP ----------------
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")

# ---------------- FASTAPI ----------------
app = FastAPI()

# ✅ CACHE (IMPORTANT)
cache = {}


class Query(BaseModel):
    question: str


# ---------------- SQL VALIDATION ----------------
def validate_sql(sql):
    if not sql:
        return False

    sql_lower = sql.lower().strip()

    if not sql_lower.startswith("select"):
        return False

    if "from" not in sql_lower:
        return False

    forbidden = ["drop", "delete", "insert", "update", "alter"]
    return not any(word in sql_lower for word in forbidden)


# ---------------- RETRY FUNCTION ----------------
def generate_sql_with_retry(prompt):
    try:
        return model.generate_content(prompt).text
    except Exception as e:
        if "429" in str(e):
            print("⚠️ Rate limit hit. Waiting 60 seconds...")
            time.sleep(60)
            return model.generate_content(prompt).text
        else:
            raise e


# ---------------- SCHEMA ----------------
SCHEMA = """
Tables:

patients(id, first_name, last_name, email, phone, date_of_birth, gender, city, registered_date)

doctors(id, name, specialization, department, phone)

appointments(id, patient_id, doctor_id, appointment_date, status)

treatments(id, appointment_id, treatment_name, cost, duration_minutes)

invoices(id, patient_id, invoice_date, total_amount, paid_amount, status)
"""


# ---------------- CHAT API ----------------
@app.post("/chat")
async def chat(query: Query):
    try:
        question = query.question.strip()

        # ❗ Empty check
        if not question:
            return {"error": "Question cannot be empty"}

        # ✅ CACHE CHECK (VERY IMPORTANT)
        if question in cache:
            return cache[question]

        # 🔥 PROMPT
        prompt = f"""
You are an expert SQLite SQL generator.

Convert the question into a COMPLETE valid SQLite SQL query.

Database schema:
{SCHEMA}

Rules:
- ONLY return SQL
- MUST start with SELECT
- MUST include FROM clause
- NEVER return partial SQL
- NO explanation
- NO markdown

Examples:
Q: How many patients?
A: SELECT COUNT(*) FROM patients

Q: Top 5 patients
A: SELECT * FROM patients LIMIT 5

Question: {question}
"""

        # ---------------- GENERATE SQL ----------------
        sql = generate_sql_with_retry(prompt).strip()

        # ---------------- CLEAN SQL ----------------
        sql = sql.replace("```sql", "").replace("```", "").strip()
        sql = sql.split("\n")[-1].strip()
        sql = sql.rstrip(";")

        # ---------------- VALIDATE ----------------
        if not validate_sql(sql):
            return {
                "error": "Invalid or incomplete SQL generated",
                "generated_sql": sql
            }

        # ---------------- EXECUTE SQL ----------------
        conn = sqlite3.connect("clinic.db")
        cursor = conn.cursor()

        cursor.execute(sql)
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]

        conn.close()

        # ---------------- RESULT ----------------
        result = {
            "message": "Query executed successfully",
            "sql_query": sql,
            "columns": columns,
            "rows": rows,
            "row_count": len(rows)
        }

        # ✅ SAVE TO CACHE
        cache[question] = result

        return result

    except Exception as e:
        return {"error": str(e)}


# ---------------- HEALTH ----------------
@app.get("/health")
def health():
    return {
        "status": "ok",
        "cached_queries": len(cache)
    }