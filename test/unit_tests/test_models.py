# File: test/unit_tests/test_models.py
import pytest
from pydantic import ValidationError
from app.models import ApplicationRequest, TechnicalAnalysisRequest


class TestApplicationRequest:
    """Unit tests for ApplicationRequest Pydantic model."""

    def test_valid_application_creates_instance(self):
        """Test that valid data creates a model instance."""
        app = ApplicationRequest(
            github_url="https://github.com/angelatest",
            background="A" * 50,
            full_name="Angela Test",
            email="angela@example.com",
            years_experience=3,
            skills=["Python", "FastAPI"],
            position_applied="Developer"
        )

        assert app.full_name == "Angela Test"
        assert app.years_experience == 3

    def test_invalid_github_url_raises_validation_error(self):
        """Test that non-GitHub URL raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            ApplicationRequest(
                github_url="https://gitlab.com/user",  # Wrong domain
                background="A" * 50,
                full_name="Angela Test",
                email="angela@example.com",
                years_experience=3,
                skills=["Python"],
                position_applied="Developer"
            )

        errors = exc_info.value.errors()
        assert any(err["loc"] == ("github_url",) for err in errors)

    def test_background_too_short_raises_validation_error(self):
        """Test that background under 50 chars raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            ApplicationRequest(
                github_url="https://github.com/angelatest",
                background="Too short",
                full_name="Angela Test",
                email="angela@example.com",
                years_experience=3,
                skills=["Python"],
                position_applied="Developer"
            )

        errors = exc_info.value.errors()
        assert any(err["loc"] == ("background",) for err in errors)

    def test_invalid_email_raises_validation_error(self):
        """Test that invalid email raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            ApplicationRequest(
                github_url="https://github.com/angelatest",
                background="A" * 50,
                full_name="Angela Test",
                email="not-an-email",
                years_experience=3,
                skills=["Python"],
                position_applied="Developer"
            )

        errors = exc_info.value.errors()
        assert any(err["loc"] == ("email",) for err in errors)

    def test_negative_years_experience_raises_validation_error(self):
        """Test that negative years raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            ApplicationRequest(
                github_url="https://github.com/angelatest",
                background="A" * 50,
                full_name="Angela Test",
                email="angela@example.com",
                years_experience=-1,
                skills=["Python"],
                position_applied="Developer"
            )

        errors = exc_info.value.errors()
        assert any(err["loc"] == ("years_experience",) for err in errors)

    def test_empty_skills_raises_validation_error(self):
        """Test that empty skills array raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            ApplicationRequest(
                github_url="https://github.com/angelatest",
                background="A" * 50,
                full_name="Angela Test",
                email="angela@example.com",
                years_experience=3,
                skills=[],
                position_applied="Developer"
            )

        errors = exc_info.value.errors()
        assert any(err["loc"] == ("skills",) for err in errors)


class TestTechnicalAnalysisRequest:
    """Unit tests for TechnicalAnalysisRequest Pydantic model."""

    def test_valid_technical_analysis_creates_instance(self):
        """Test that valid data creates a model instance."""
        doc = TechnicalAnalysisRequest(
            synopsis="A" * 100,
            key_concepts=["Concept1", "Concept2", "Concept3"],
            technical_details=["Detail1", "Detail2", "Detail3"],
            analysis="A" * 200,
            submitted_by="angela@example.com"
        )

        assert len(doc.key_concepts) == 3

    def test_synopsis_too_short_raises_validation_error(self):
        """Test that synopsis under 100 chars raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            TechnicalAnalysisRequest(
                synopsis="Too short",
                key_concepts=["A", "B", "C"],
                technical_details=["X", "Y", "Z"],
                analysis="A" * 200,
                submitted_by="angela@example.com"
            )

        errors = exc_info.value.errors()
        assert any(err["loc"] == ("synopsis",) for err in errors)

    def test_empty_string_in_key_concepts_raises_validation_error(self):
        """Test custom validator catches empty strings."""
        with pytest.raises(ValidationError) as exc_info:
            TechnicalAnalysisRequest(
                synopsis="A" * 100,
                key_concepts=["Valid", "", "Also Valid"],  # Empty string
                technical_details=["X", "Y", "Z"],
                analysis="A" * 200,
                submitted_by="angela@example.com"
            )

        errors = exc_info.value.errors()
        assert any(err["loc"] == ("key_concepts",) for err in errors)