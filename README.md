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
- Python 3.11
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
  - `services/`: Business logic and service layer. (* NOT applied to this project yet)
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
![Unit Tests](https://github.com/amcpengineer/whitegloveai-apprentice-proficiency/actions/workflows/unit-tests.yml/badge.svg)
---

## Author
Angela Cortes
