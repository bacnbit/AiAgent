"""
Main FastAPI application entry point.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging

from config import settings

logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="AI Agent for ERP Configuration Validation",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """Initialize application on startup."""
    logger.info(f"Starting {settings.app_name} v{settings.app_version}")
    logger.info(f"Log level: {settings.log_level}")
    # TODO: Initialize database
    # TODO: Initialize MCP clients


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    logger.info("Shutting down application")
    # TODO: Close database connections
    # TODO: Close MCP client connections


@app.get("/")
async def root():
    """Root endpoint - health check."""
    return {
        "app": settings.app_name,
        "version": settings.app_version,
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint for K8s."""
    return {"status": "healthy"}


# TODO: Import and include routers
# from api.routes import router as api_router
# from api.websocket import router as ws_router
# app.include_router(api_router, prefix="/api")
# app.include_router(ws_router, prefix="/ws")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=True,
        log_level=settings.log_level.lower()
    )
