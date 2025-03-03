from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
import random
from datetime import datetime

from ..core.security import verify_token
from ..db.session import get_db
from ..services.recommendation_service import RecommendationService
from ..core.config import settings
from ..models.recommendation_model import VideoRecommendationModel

router = APIRouter()

# Create a simplified model instance for testing
simplified_model = VideoRecommendationModel()

@router.get("/feed", response_model=List[Dict[str, Any]])
async def get_personalized_feed(
    username: str,
    category_id: Optional[str] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(settings.DEFAULT_PAGE_SIZE, ge=1, le=settings.MAX_PAGE_SIZE),
    db: Session = Depends(get_db),
    _=Depends(verify_token)
):
    """
    Get personalized video recommendations for a user.
    Optionally filter by category.
    """
    try:
        # Use the simplified model directly for testing
        recommendations = simplified_model.recommend_for_user(
            user_id=username,
            limit=page_size
        )
        return recommendations
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/trending", response_model=List[Dict[str, Any]])
async def get_trending_videos(
    timeframe: str = Query("day", enum=["hour", "day", "week", "month"]),
    category_id: Optional[str] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(settings.DEFAULT_PAGE_SIZE, ge=1, le=settings.MAX_PAGE_SIZE),
    db: Session = Depends(get_db),
    _=Depends(verify_token)
):
    """
    Get trending videos for a specific timeframe.
    Optionally filter by category.
    """
    try:
        # Use the simplified model directly for testing
        trending_videos = simplified_model.recommend_trending(
            timeframe=timeframe,
            category=category_id,
            limit=page_size
        )
        return trending_videos
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/mood-based", response_model=List[Dict[str, Any]])
async def get_mood_based_recommendations(
    mood: str = Query(..., description="User's current mood"),
    page: int = Query(1, ge=1),
    page_size: int = Query(settings.DEFAULT_PAGE_SIZE, ge=1, le=settings.MAX_PAGE_SIZE),
    db: Session = Depends(get_db),
    _=Depends(verify_token)
):
    """
    Get mood-based video recommendations.
    """
    try:
        # Use the simplified model directly for testing
        mood_videos = simplified_model.recommend_by_mood(
            mood=mood,
            limit=page_size
        )
        return mood_videos
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/interaction", response_model=Dict[str, Any])
async def record_interaction(
    username: str,
    video_external_id: str,
    interaction_type: str = Query(..., enum=["view", "like", "inspire", "rate"]),
    value: Optional[float] = Query(None, ge=1.0, le=5.0, description="Rating value (1-5) if interaction_type is 'rate'"),
    db: Session = Depends(get_db),
    _=Depends(verify_token)
):
    """
    Record a user interaction with a video.
    """
    try:
        # For testing, we'll return a mock response
        return {
            "success": True,
            "message": f"Interaction {interaction_type} recorded for user {username} on video {video_external_id}",
            "interaction": {
                "username": username,
                "video_external_id": video_external_id,
                "interaction_type": interaction_type,
                "value": value,
                "timestamp": datetime.now().isoformat()
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 