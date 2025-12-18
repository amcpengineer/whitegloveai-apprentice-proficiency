#File: test/integration_tests/test_exceptions.py
import pytest
import httpx
from app.client import WGAIClient
from app.models import ApplicationRequest, TechnicalAnalysisRequest

client = WGAIClient()

def test_submit_application_wrong_api_key():
    payload = ApplicationRequest(
        github_url="https://github.com/realuser",
        background="Real background with more than fifty characters...",
        full_name="Real User",
        email="real@example.com",
        years_experience=5,
        skills=["Python", "FastAPI"],
        position_applied="AI Engineer"
    )

    with pytest.raises(httpx.HTTPStatusError) as exc_info:
        client.analyze_technical_document(payload, api_key="wrong-key-for-testing")

    assert exc_info.value.response.status_code == 401

def test_technical_analysis_wrong_api_key():
    payload = TechnicalAnalysisRequest(
        synopsis="This document provides a comprehensive overview of microservices architecture patterns, focusing on service decomposition strategies, inter-service communication protocols, and deployment considerations for cloud-native applications.",
        key_concepts=[
            "Service decomposition",
            "API gateway pattern",
            "Event-driven architecture",
            "Container orchestration"
        ],
        technical_details=[
            "REST and gRPC for synchronous communication",
            "Apache Kafka for asynchronous messaging",
            "Kubernetes for container orchestration",
            "Istio service mesh for traffic management"
        ],
        analysis="The microservices architecture presents significant advantages for scalability and team autonomy, allowing independent deployment cycles and technology flexibility per service. However, it introduces complexity in distributed system management, requiring robust observability tooling, careful API versioning strategies, and comprehensive testing approaches.",
        submitted_by="angela.developer@example.com"
    )

    with pytest.raises(httpx.HTTPStatusError) as exc_info:
        client.submit_application(payload, api_key="wrong-key-for-testing")

    assert exc_info.value.response.status_code == 401
