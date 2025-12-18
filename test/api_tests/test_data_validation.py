#File: tests/api_test/test_data_validation.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

class TestValidationErrorHandler:
    """Tests for the custom validation exception handler."""

    def test_invalid_github_url_returns_400(self):
        """Test that invalid GitHub URL returns 400 with proper error structure."""
        payload = {
            "github_url": "https://gitlab.com/user",  # Wrong domain
            "background": "A" * 50,
            "full_name": "Angela Test",
            "email": "angela@example.com",
            "years_experience": 3,
            "skills": ["Python"],
            "position_applied": "Developer"
        }

        response = client.post("/submit/application", json=payload)

        assert response.status_code == 400
        data = response.json()
        assert data["status"] == "validation_error"
        assert data["message"] == "Invalid application data"
        assert isinstance(data["errors"], list)
        assert any(err["field"] == "github_url" for err in data["errors"])

    def test_background_too_short_returns_400(self):
        """Test that background under 50 chars returns 400."""
        payload = {
            "github_url": "https://github.com/angelatest",
            "background": "Too short",  # Less than 50 chars
            "full_name": "Angela Test",
            "email": "angela@example.com",
            "years_experience": 3,
            "skills": ["Python"],
            "position_applied": "Developer"
        }

        response = client.post("/submit/application", json=payload)

        assert response.status_code == 400
        data = response.json()
        assert data["status"] == "validation_error"
        assert any(err["field"] == "background" for err in data["errors"])

    def test_invalid_email_returns_400(self):
        """Test that invalid email format returns 400."""
        payload = {
            "github_url": "https://github.com/angelatest",
            "background": "A" * 50,
            "full_name": "Angela Test",
            "email": "not-an-email",  # Invalid email
            "years_experience": 3,
            "skills": ["Python"],
            "position_applied": "Developer"
        }

        response = client.post("/submit/application", json=payload)

        assert response.status_code == 400
        data = response.json()
        assert data["status"] == "validation_error"
        assert any(err["field"] == "email" for err in data["errors"])

    def test_negative_years_experience_returns_400(self):
        """Test that negative years_experience returns 400."""
        payload = {
            "github_url": "https://github.com/angelatest",
            "background": "A" * 50,
            "full_name": "Angela Test",
            "email": "angela@example.com",
            "years_experience": -1,  # Negative value
            "skills": ["Python"],
            "position_applied": "Developer"
        }

        response = client.post("/submit/application", json=payload)

        assert response.status_code == 400
        data = response.json()
        assert data["status"] == "validation_error"
        assert any(err["field"] == "years_experience" for err in data["errors"])

    def test_empty_skills_returns_400(self):
        """Test that empty skills array returns 400."""
        payload = {
            "github_url": "https://github.com/angelatest",
            "background": "A" * 50,
            "full_name": "Angela Test",
            "email": "angela@example.com",
            "years_experience": 3,
            "skills": [],  # Empty array
            "position_applied": "Developer"
        }

        response = client.post("/submit/application", json=payload)

        assert response.status_code == 400
        data = response.json()
        assert data["status"] == "validation_error"
        assert any(err["field"] == "skills" for err in data["errors"])

    def test_missing_required_field_returns_400(self):
        """Test that missing required field returns 400."""
        payload = {
            "github_url": "https://github.com/angelatest",
            "background": "A" * 50,
            # missing full_name
            "email": "angela@example.com",
            "years_experience": 3,
            "skills": ["Python"],
            "position_applied": "Developer"
        }

        response = client.post("/submit/application", json=payload)

        assert response.status_code == 400
        data = response.json()
        assert data["status"] == "validation_error"
        assert any(err["field"] == "full_name" for err in data["errors"])

    def test_multiple_errors_returns_all(self):
        """Test that multiple validation errors are all returned."""
        payload = {
            "github_url": "invalid-url",
            "background": "Short",
            "full_name": "A",  # Too short
            "email": "bad-email",
            "years_experience": -5,
            "skills": [],
            "position_applied": ""
        }

        response = client.post("/submit/application", json=payload)

        assert response.status_code == 400
        data = response.json()
        assert data["status"] == "validation_error"
        assert len(data["errors"]) > 1  # Multiple errors returned

    def test_error_structure_has_required_keys(self):
        """Test that each error has field, message, and type keys."""
        payload = {
            "github_url": "invalid",
            "background": "A" * 50,
            "full_name": "Angela Test",
            "email": "angela@example.com",
            "years_experience": 3,
            "skills": ["Python"],
            "position_applied": "Developer"
        }

        response = client.post("/submit/application", json=payload)

        assert response.status_code == 400
        data = response.json()

        for error in data["errors"]:
            assert "field" in error
            assert "message" in error
            assert "type" in error

