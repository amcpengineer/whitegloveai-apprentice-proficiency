"""
Technical Document Analysis Router (part 2)

Handles endpoints for analyzing technical documents through the WhiteGloveAI API.
This module processes document synopses, extracts key concepts, and returns
AI-generated technical analysis.
"""

#File: app/routers/submit.py
from fastapi import APIRouter, HTTPException
from app.models import TechnicalAnalysisRequest
from app.client import WGAIClient

router = APIRouter(
    prefix="/analyze",
    tags=["tech-documents"],
)


@router.post("/tech-documents")
def analyze_tech_docs(payload: TechnicalAnalysisRequest):
    """
        Submit a technical document for AI-powered analysis.

        Accepts document metadata including synopsis, key concepts, and technical
        details, then forwards to WGAI's Phase 2 API for processing.

        Args:
            payload: Validated technical document data containing:
                - synopsis: Document summary (min 100 chars)
                - key_concepts: Core topics covered (min 3 items)
                - technical_details: Implementation specifics (min 3 items)
                - analysis: Detailed technical breakdown (min 200 chars)
                - submitted_by: Submitter's email for tracking

        Returns:
            dict: WGAI analysis response containing processed insights
                  and document evaluation results.

        Raises:
            HTTPException (400): When payload fails validation constraints.
            HTTPException (500): When WGAI API is unreachable or returns an error.

        Note:
            This endpoint uses API_KEY_PHASE2 for authentication,
            distinct from the application submission endpoint.
        """
    client = WGAIClient()

    try:
        result = client.analyze_technical_document(payload)
        return result
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc)
        )