from fastapi import FastAPI, Depends, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import os
from dotenv import load_dotenv

from .routers import recommendations, data_collection
from .core.config import settings
from .core.security import verify_token

load_dotenv()

app = FastAPI(
    title="Video Recommendation Engine",
    description="A sophisticated recommendation system for personalized video content",
    version="1.0.0"
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(recommendations.router, prefix="/api/v1", tags=["recommendations"])
app.include_router(data_collection.router, prefix="/api/v1", tags=["data-collection"])

@app.get("/")
async def root():
    return {"message": "Welcome to Video Recommendation Engine API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"} 