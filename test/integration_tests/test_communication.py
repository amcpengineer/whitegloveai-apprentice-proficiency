#File: test/integration_tests/test_communication.py
import os
from fastapi.testclient import TestClient
from app.main import app
from app.config import settings

client = TestClient(app)

def test_submit_application_api_integration():
    """
      Integration test for the application submission endpoint.
      Requires a valid API_KEY_PHASE1 to run against the real API.
      """
    if not settings.API_KEY_PHASE1:
        import pytest
        pytest.skip("Integration test requires real API key")

    payload = {
        "github_url": "https://github.com/realuser",
        "background": "Real background with more than fifty characters...",
        "full_name": "Real User",
        "email": "real@example.com",
        "years_experience": 5,
        "skills": ["Python", "FastAPI"],
        "position_applied": "AI Engineer"
    }

    response = client.post("/submit/application", json=payload)

    assert response.status_code == 200
    assert "id" in response.json()

def test_tech_documents_api_integration():
    if not settings.API_KEY_PHASE2:
        import pytest
        pytest.skip("Integration test requires real API key")

    payload = {
        "synopsis": "This is a detailed synopsis of the technical document, exceeding one hundred characters to meet validation requirements.",
        "key_concepts": ["Concept1", "Concept2", "Concept3"],
        "technical_details": ["Detail1", "Detail2", "Detail3"],
        "analysis": "This is an in-depth technical analysis that goes beyond two hundred characters to ensure it meets the validation criteria set forth in the model definition.",
        "submitted_by": "amcp.engineer@gmail.cpom"
    }

    response = client.post("/submit/application", json=payload)

    assert response.status_code == 200
    assert "id" in response.json()