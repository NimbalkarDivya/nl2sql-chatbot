from dotenv import load_dotenv
import os

load_dotenv()

from vanna import Agent
from vanna.core.registry import ToolRegistry
from vanna.core.user import UserResolver, User
from vanna.tools import RunSqlTool, VisualizeDataTool
from vanna.integrations.sqlite import SqliteRunner
from vanna.integrations.local.agent_memory import DemoAgentMemory
from vanna.integrations.google import GeminiLlmService


# ---------------- USER ----------------
class DefaultUserResolver(UserResolver):
    def resolve_user(self, request):
        return User(user_id="default_user")


# ---------------- AGENT ----------------
def get_agent():

    # ✅ ADD SYSTEM PROMPT WITH SCHEMA (VERY IMPORTANT)
    system_prompt = """
You are an expert SQL assistant.

Database schema:

patients(id, first_name, last_name, email, phone, date_of_birth, gender, city, registered_date)

doctors(id, name, specialization, department, phone)

appointments(id, patient_id, doctor_id, appointment_date, status)

treatments(id, appointment_id, treatment_name, cost, duration_minutes)

invoices(id, patient_id, invoice_date, total_amount, paid_amount, status)

Rules:
- Only generate valid SQLite SQL
- Only use SELECT queries
- Use correct table and column names
- Return SQL query clearly
"""

    llm = GeminiLlmService(
        api_key=os.getenv("GOOGLE_API_KEY"),
        model="gemini-2.5-flash",
        system_prompt=system_prompt   # ✅ FIX HERE
    )

    sql_runner = SqliteRunner("clinic.db")

    registry = ToolRegistry([
        RunSqlTool(sql_runner),
        VisualizeDataTool()
    ])

    memory = DemoAgentMemory()

    agent = Agent(
        llm,
        registry,
        DefaultUserResolver(),
        memory
    )

    return agent