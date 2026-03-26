# NL2SQL Chatbot (Vanna 2.0)

## Setup
Install dependencies:

pip install -r requirements.txt

## Add API Key
Create a .env file in the project root directory and add your Gemini API key:
GOOGLE_API_KEY = your_api_key_here # give your api key here
If no API key is provided, the system may not function correctly as it relies on Gemini API for SQL generation.

## Run
python setup_database.py
python seed_memory.py
python -m uvicorn main:app --reload


## API
POST /chat
{
 "question": "How many patients?"
}

## Project Structure
PROJECT/
│
├── main.py # FastAPI application
├── vanna_setup.py # Vanna agent setup
├── setup_database.py # Create database + dummy data
├── seed_memory.py # Memory seeding (training examples)
├── clinic.db # SQLite database
├── requirements.txt # Dependencies
├── README.md # Documentation
├── RESULTS.md # Test results
└── .env # API key 


## Architecture
User Question
      ↓
Vanna Agent (LLM)
      ↓
SQL Query
      ↓
SQLite Database
      ↓
Result → API Response
