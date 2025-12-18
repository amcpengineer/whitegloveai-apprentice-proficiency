#File: app/routers/submit.py

"""
Application Submission Router (part 1)

Handles endpoints for submitting job applications to the WhiteGloveAI API.
This module serves as the interface between incoming client requests
and the external WGAI service.
"""

from fastapi import APIRouter, HTTPException
from app.models import ApplicationRequest
from app.client import WGAIClient

router = APIRouter(
    prefix="/submit",
    tags=["application"],
)


@router.post("/application")
def submit_application(payload: ApplicationRequest):
    """
        Submit a job application to the WhiteGloveAI system.

        Validates the incoming application data and forwards it to the
        external WGAI API for processing.

        Args:
            payload: Validated application data including personal info,
                     skills, and experience details.

        Returns:
            dict: Response from WGAI API containing submission confirmation
                  and any additional processing details.

        Raises:
            HTTPException (400): When payload validation fails (handled by FastAPI).
            HTTPException (500): When WGAI API communication fails.
        """


    client = WGAIClient()

    try:
        result = client.submit_application(payload)
        return result
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc)
        )