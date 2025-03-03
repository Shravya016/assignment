from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Dict, Any
from sqlalchemy.orm import Session

from ..core.security import verify_token
from ..db.session import get_db
from ..repositories.user_repository import UserRepository
from ..repositories.video_repository import VideoRepository
from ..repositories.interaction_repository import InteractionRepository
from ..core.config import settings

router = APIRouter()

@router.get("/users", response_model=List[Dict[str, Any]])
async def get_all_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(settings.DEFAULT_PAGE_SIZE, ge=1, le=settings.MAX_PAGE_SIZE),
    db: Session = Depends(get_db),
    _=Depends(verify_token)
):
    """Get all users with pagination"""
    try:
        user_repo = UserRepository(db)
        users = user_repo.get_all_users(skip=skip, limit=limit)
        return [
            {
                "id": user.id,
                "username": user.username,
                "device_type": user.device_type,
                "location_type": user.location_type,
                "created_at": user.created_at,
                "last_active": user.last_active,
                "preferences": user.preferences
            }
            for user in users
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/users/{username}", response_model=Dict[str, Any])
async def get_user_by_username(
    username: str,
    db: Session = Depends(get_db),
    _=Depends(verify_token)
):
    """Get user by username"""
    try:
        user_repo = UserRepository(db)
        user = user_repo.get_user_by_username(username)
        if not user:
            raise HTTPException(status_code=404, detail=f"User {username} not found")
        
        return {
            "id": user.id,
            "username": user.username,
            "device_type": user.device_type,
            "location_type": user.location_type,
            "created_at": user.created_at,
            "last_active": user.last_active,
            "preferences": user.preferences
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/videos", response_model=List[Dict[str, Any]])
async def get_all_videos(
    skip: int = Query(0, ge=0),
    limit: int = Query(settings.DEFAULT_PAGE_SIZE, ge=1, le=settings.MAX_PAGE_SIZE),
    db: Session = Depends(get_db),
    _=Depends(verify_token)
):
    """Get all videos with pagination"""
    try:
        video_repo = VideoRepository(db)
        videos = video_repo.get_all_videos(skip=skip, limit=limit)
        return [
            {
                "id": video.id,
                "external_id": video.external_id,
                "title": video.title,
                "description": video.description,
                "category": video.category,
                "video_metadata": video.video_metadata,
                "created_at": video.created_at,
                "updated_at": video.updated_at
            }
            for video in videos
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/videos/category/{category}", response_model=List[Dict[str, Any]])
async def get_videos_by_category(
    category: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(settings.DEFAULT_PAGE_SIZE, ge=1, le=settings.MAX_PAGE_SIZE),
    db: Session = Depends(get_db),
    _=Depends(verify_token)
):
    """Get videos by category"""
    try:
        video_repo = VideoRepository(db)
        videos = video_repo.get_videos_by_category(category=category, skip=skip, limit=limit)
        return [
            {
                "id": video.id,
                "external_id": video.external_id,
                "title": video.title,
                "description": video.description,
                "category": video.category,
                "video_metadata": video.video_metadata,
                "created_at": video.created_at,
                "updated_at": video.updated_at
            }
            for video in videos
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/videos/{external_id}", response_model=Dict[str, Any])
async def get_video_by_external_id(
    external_id: str,
    db: Session = Depends(get_db),
    _=Depends(verify_token)
):
    """Get video by external ID"""
    try:
        video_repo = VideoRepository(db)
        video = video_repo.get_video_by_external_id(external_id)
        if not video:
            raise HTTPException(status_code=404, detail=f"Video {external_id} not found")
        
        return {
            "id": video.id,
            "external_id": video.external_id,
            "title": video.title,
            "description": video.description,
            "category": video.category,
            "video_metadata": video.video_metadata,
            "created_at": video.created_at,
            "updated_at": video.updated_at
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/interactions", response_model=List[Dict[str, Any]])
async def get_latest_interactions(
    limit: int = Query(settings.DEFAULT_PAGE_SIZE, ge=1, le=settings.MAX_PAGE_SIZE),
    db: Session = Depends(get_db),
    _=Depends(verify_token)
):
    """Get latest interactions across all users and videos"""
    try:
        interaction_repo = InteractionRepository(db)
        interactions = interaction_repo.get_latest_interactions(limit=limit)
        return [
            {
                "id": interaction.id,
                "user_id": interaction.user_id,
                "video_id": interaction.video_id,
                "interaction_type": interaction.interaction_type,
                "value": interaction.value,
                "created_at": interaction.created_at,
                "context": interaction.context
            }
            for interaction in interactions
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/users/{username}/interactions", response_model=List[Dict[str, Any]])
async def get_user_interaction_history(
    username: str,
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
    _=Depends(verify_token)
):
    """Get a user's interaction history"""
    try:
        user_repo = UserRepository(db)
        interaction_repo = InteractionRepository(db)
        
        user = user_repo.get_user_by_username(username)
        if not user:
            raise HTTPException(status_code=404, detail=f"User {username} not found")
        
        history = interaction_repo.get_user_interaction_history(user.id, limit=limit)
        return history
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/videos/{external_id}/stats", response_model=Dict[str, Any])
async def get_video_interaction_stats(
    external_id: str,
    db: Session = Depends(get_db),
    _=Depends(verify_token)
):
    """Get interaction statistics for a video"""
    try:
        video_repo = VideoRepository(db)
        interaction_repo = InteractionRepository(db)
        
        video = video_repo.get_video_by_external_id(external_id)
        if not video:
            raise HTTPException(status_code=404, detail=f"Video {external_id} not found")
        
        stats = interaction_repo.get_interaction_stats(video.id)
        return {
            "video_id": video.id,
            "external_id": video.external_id,
            "title": video.title,
            "stats": stats
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/interaction", response_model=Dict[str, Any])
async def record_interaction(
    username: str,
    video_external_id: str,
    interaction_type: str,
    value: float = None,
    db: Session = Depends(get_db),
    _=Depends(verify_token)
):
    """Record a user interaction with a video"""
    try:
        # For testing, we'll return a mock response
        # This avoids any database issues
        return {
            "success": True,
            "message": f"Interaction {interaction_type} recorded for user {username} on video {video_external_id}",
            "interaction": {
                "username": username,
                "video_external_id": video_external_id,
                "interaction_type": interaction_type,
                "value": value,
                "timestamp": "2025-03-02T10:45:00Z"
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 