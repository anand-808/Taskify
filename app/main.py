from fastapi import FastAPI
from app.routes import router
from datetime import datetime, timezone

app = FastAPI(
    title="Taskify - Task Management API",
    description="A simple task management API built with FastAPI and MongoDB",
    version="1.0.0"
)

#Include the router from app.routes
app.include_router(router, prefix="/api/v1", )

# Health check endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to Taskify API! Visit /docs for Swagger UI"}

@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "version": "1.0.0"
    }
