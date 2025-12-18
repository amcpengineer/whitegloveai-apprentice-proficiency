#File: app/client.py
"""
WhiteGloveAI API Client

HTTP client wrapper for interacting with the WhiteGloveAI external API.
Handles authentication, request formatting, and response parsing for
both Phase 1 (application submission) and Phase 2 (technical analysis) endpoints.
"""

import httpx
from app.config import settings
from app.models import ApplicationRequest, TechnicalAnalysisRequest

class WGAIClient:
    """
        Synchronous HTTP client for WhiteGloveAI API integration.

        Provides methods for submitting job applications and analyzing
        technical documents through WGAI's RESTful endpoints.

        Attributes:
            base_url: Root URL for all WGAI API requests.

        Raises:
            ValueError: If required environment variables are not configured.

        Example:
            >>> client = WGAIClient()
            >>> result = client.submit_application(application_payload)
        """

    def __init__(self):
        """
                Initialize the WGAI client with configuration validation.

                Validates that all required environment variables are present
                before allowing client instantiation. Fails fast to prevent
                runtime errors during API calls.
                """
        if not settings.WGAI_BASE_URL:
            raise ValueError("WGAI_BASE_URL is not configured")

        if not settings.API_KEY_PHASE1:
            raise ValueError("WGAI_API_KEY_PHASE1 is not configured")

        if not settings.API_KEY_PHASE2:
            raise ValueError("WGAI_API_KEY_PHASE2 is not configured")

        self.base_url = settings.WGAI_BASE_URL

    def _headers(self, api_key: str) -> dict:
        """
                Build request headers with authentication.

                Args:
                    api_key: WGAI API key for the target endpoint phase.

                Returns:
                    Dictionary containing auth and content-type headers.
                """
        return {
        "X-Auth-Key": api_key,
        "Content-Type": "application/json",
        }

    def submit_application(self, payload: ApplicationRequest, api_key: str | None = None) -> dict:
        """
                Submit a job application to WGAI Phase 1 endpoint.

                Args:
                    payload: Validated application data (personal info, skills, etc.).
                    api_key: Optional API key override. Defaults to API_KEY_PHASE1
                             from environment. Useful for testing or multi-tenant scenarios.

                Returns:
                    Parsed JSON response from WGAI containing submission
                    confirmation and processing status.

                Raises:
                    httpx.TimeoutException: If request exceeds timeout threshold.
                    httpx.HTTPStatusError: If WGAI returns 4xx/5xx response.
                    httpx.ConnectError: If WGAI service is unreachable.
                """
        key = api_key if api_key is not None else settings.API_KEY_PHASE1

        url =f"{self.base_url}/v1/api/hire/me"
        with httpx.Client(timeout=10.0) as client:
            response = client.post(
                url,
                headers=self._headers(key),
                json=payload.model_dump(),
            )

        response.raise_for_status()
        return response.json()

    def analyze_technical_document(self, payload: TechnicalAnalysisRequest, api_key: str | None = None) -> dict:
        """
                Submit a technical document for AI analysis via WGAI Phase 2 endpoint.

                Args:
                    payload: Validated document data including synopsis, key concepts,
                             technical details, and preliminary analysis.
                    api_key: Optional API key override. Defaults to API_KEY_PHASE2
                             from environment.

                Returns:
                    Parsed JSON response containing WGAI's technical analysis
                    results and document evaluation.

                Raises:
                    httpx.TimeoutException: If request exceeds timeout threshold.
                    httpx.HTTPStatusError: If WGAI returns 4xx/5xx response.
                    httpx.ConnectError: If WGAI service is unreachable.

                Note:
                    Phase 2 uses a different API key than Phase 1, reflecting
                    WGAI's tiered access control model.
                """
        key = api_key if api_key is not None else settings.API_KEY_PHASE2

        url = f"{self.base_url}/v2/api/analyze/technical-document"

        with httpx.Client(timeout=10.0) as client:
            response = client.post(
                url,
                headers=self._headers(key),
                json=payload.model_dump(),
            )

        response.raise_for_status()
        return response.json()