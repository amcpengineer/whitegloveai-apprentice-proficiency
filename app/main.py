#File: app/main.py
"""
Main FastAPI application entry point for WhiteGloveAI Apprentice Proficiency API.
"""

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.routers.submit import router as part1_router
from app.routers.analyze_tech_documents import router as part2_router

# Initialize FastAPI application with metadata for OpenAPI documentation
app = FastAPI(
    title="WhiteGloveAI Apprentice Proficiency",
    description="FastAPI client demonstrating API integration proficiency",
    version="1.0.0",
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
       Custom exception handler for request validation errors.

       Transforms Pydantic validation errors into a cleaner, more user-friendly
       JSON response format with 400 Bad Request status.

       Args:
           request: The incoming HTTP request that triggered the error.
           exc: The RequestValidationError containing validation failure details.

       Returns:
           JSONResponse with structured error details including field names,
           error messages, and error types.
       """
    errors = []
    for error in exc.errors():
        field = " -> ".join(str(loc) for loc in error["loc"] if loc != "body")
        errors.append({
            "field": field,
            "message": error["msg"],
            "type": error["type"]
        })

    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "status": "validation_error",
            "message": "Invalid application data message was not sent",
            "errors": errors
        }
    )

# Register routers for different API sections
app.include_router(part1_router) #submition
app.include_router(part2_router) #technical analyze document submission

@app.get("/health", tags=["health"])
def health_check():
    """
       Health check endpoint for monitoring and load balancer probes.

       Returns:
           Simple status object indicating the service is operational.
       """
    return {"status": "ok"}