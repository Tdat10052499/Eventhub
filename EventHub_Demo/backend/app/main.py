"""
FastAPI Application Main Entry Point
EventHub - Teambuilding Management System
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from app.config import settings

# Create FastAPI app
app = FastAPI(
    title="EventHub API",
    description="API for Teambuilding Management System",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost",
        "http://localhost:80",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount uploads directory for static file serving
uploads_dir = settings.UPLOAD_DIR
if not os.path.exists(uploads_dir):
    os.makedirs(uploads_dir)
app.mount("/uploads", StaticFiles(directory=uploads_dir), name="uploads")

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "EventHub API",
        "version": "1.0.0"
    }

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to EventHub API",
        "docs": "/docs",
        "health": "/health"
    }

# Import and include routers
from app.routers import auth, teambuildings, events, registrations, upload, dashboard

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(teambuildings.router, prefix="/teambuildings", tags=["Teambuildings"])
app.include_router(events.router, prefix="/events", tags=["Events"])
app.include_router(registrations.router, prefix="/registrations", tags=["Registrations"])
app.include_router(upload.router, prefix="/upload", tags=["Upload"])
app.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
