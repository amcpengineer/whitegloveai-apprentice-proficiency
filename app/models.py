#File: models.py
"""
Pydantic models for request validation and serialization.

This module defines the data models used for validating incoming API requests,
ensuring data integrity and type safety across the application.
"""

from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import List

class ApplicationRequest(BaseModel):
    """
        Model for job application submission requests.

        Validates applicant information including contact details,
        experience, and technical skills before processing.
        """

    github_url: str = Field(...,
        description="Github profile endpoint, should match valid GitHub profile format")
    background: str = Field(...,
        min_length=50,
        description="Technical background summary (minimum 50 characters)")
    full_name: str = Field(
        ...,
        min_length=2,
        description="Full designation (minimum 2 characters)")
    email: EmailStr = Field(...,
        description="Communication endpoint (valid email format)")
    years_experience: int = Field(...,
        ge=0,
        description="Experience metric (non-negative integer)")
    skills: List[str] = Field(
        ...,
        min_length=1,
        description="Technical capability array (non-empty)")
    position_applied: str = Field(...,
         min_length=1,
         description="Target role designation")

    @field_validator("github_url")
    @classmethod
    def validate_github_url(cls, v: str) -> str:
        """
               Validate GitHub URL format.

               Ensures the URL follows the pattern: https://github.com/username
               where username contains valid GitHub username characters.

               Args:
                   v: The GitHub URL string to validate.

               Returns:
                   The validated URL if format is correct.

               Raises:
                   ValueError: If URL doesn't match expected GitHub profile format.
               """

        import re
        # Pattern: https://github.com/ followed by valid username
        # Username rules: alphanumeric, hyphens, underscores; cannot start/end with hyphen
        pattern = r"^https://github\.com/[a-zA-Z0-9]([a-zA-Z0-9-_]*[a-zA-Z0-9])?$"
        if not re.match(pattern, v):
            raise ValueError(
                "Invalid GitHub URL. Must be format: https://github.com/username"
            )
        return v

    @field_validator("skills")
    @classmethod
    def validate_skills_not_empty_strings(cls, v: List[str]) -> List[str]:
        """
                Validate that skills list contains no empty or whitespace-only strings.

                Args:
                    v: List of skill strings to validate.

                Returns:
                    The validated skills list if all entries are non-empty.

                Raises:
                    ValueError: If any skill string is empty or whitespace-only.
                """
        if not all(skill.strip() for skill in v):
            raise ValueError("Skills cannot contain empty strings")
        return v

class TechnicalAnalysisRequest(BaseModel):
    """
       Model for technical document analysis submission requests.

       Captures structured analysis of technical documents including
       synopsis, key concepts, details, and comprehensive analysis.
       """
    synopsis: str = Field(
        ...,
        min_length=100,
        description="Technical document synopsis (minimum 100 characters)"
    )
    key_concepts: List[str] = Field(
        ...,
        min_length=3,
        description="Key concepts array (minimum 3 items)"
    )
    technical_details: List[str] = Field(
        ...,
        min_length=3,
        description="Technical details array (minimum 3 items)"
    )
    analysis: str = Field(
        ...,
        min_length=200,
        description="Technical analysis (minimum 200 characters)"
    )
    submitted_by: EmailStr = Field(
        ...,
        description="Submitter email address"
    )

    @field_validator("key_concepts")
    @classmethod
    def validate_key_concepts(cls, v: List[str]) -> List[str]:
        """
               Validate that key concepts list contains no empty strings.

               Args:
                   v: List of key concept strings to validate.

               Returns:
                   The validated list if all entries are non-empty.

               Raises:
                   ValueError: If any concept string is empty or whitespace-only.
               """
        if not all(item.strip() for item in v):
            raise ValueError("Key concepts cannot contain empty strings")
        return v

    @field_validator("technical_details")
    @classmethod
    def validate_technical_details(cls, v: List[str]) -> List[str]:
        """
               Validate that technical details list contains no empty strings.

               Args:
                   v: List of technical detail strings to validate.

               Returns:
                   The validated list if all entries are non-empty.

               Raises:
                   ValueError: If any detail string is empty or whitespace-only.
               """
        if not all(item.strip() for item in v):
            raise ValueError("Technical details cannot contain empty strings")
        return v
