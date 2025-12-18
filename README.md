# WhiteGloveAI Apprentice Proficiency

FastAPI client demonstrating API integration proficiency

---

## Table of Contents
- Overview
- Tech Stack
- Project Structure
- Installation
- Configuration
- Running the Project
- Usage
- Testing
- Author

---

## Overview
Explain the purpose of the project in more detail.

---

## Tech Stack
- Python 3.13
- Framework: FastAPI
- Testing: pytest

---

## Project Structure
    project_name/
        ├── app/
        │ ├── routers/
        │ ├── services/
        │ ├── clients/
        │ ├── models/
        │ └── main.py
        ├── tests/
        ├── requirements.txt
        └── README.md

  - `app/`: Contains the main application code.
  - `routers/`: API route definitions.
  - `services/`: Business logic and service layer.
  - `clients/`: External API clients.
  - `models/`: Data models and schemas.
  - `main.py`: Application entry point.

---

## Installation
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## Configuration
Create a .env file based on .env.example.

---

## Running the Project
```bash
uvicorn app.main:app --reload
```

---

## Testing
```bash
pytest
```

---

## Author
Angela Cortes
