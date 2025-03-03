from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import List, Dict, Any, Optional
from ..models.database import Video, UserInteraction
from datetime import datetime, timedelta

class VideoRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_video_by_id(self, video_id: int) -> Optional[Video]:
        """Get a video by ID"""
        return self.db.query(Video).filter(Video.id == video_id).first()

    def get_video_by_external_id(self, external_id: str) -> Optional[Video]:
        """Get a video by external ID"""
        return self.db.query(Video).filter(Video.external_id == external_id).first()

    def create_video(self, external_id: str, title: str, description: str, category: str, video_metadata: Dict) -> Video:
        """Create a new video"""
        video = Video(
            external_id=external_id,
            title=title,
            description=description,
            category=category,
            video_metadata=video_metadata,
            created_at=datetime.utcnow()
        )
        self.db.add(video)
        self.db.commit()
        self.db.refresh(video)
        return video

    def update_video(self, video_id: int, **kwargs) -> Optional[Video]:
        """Update video attributes"""
        video = self.get_video_by_id(video_id)
        if video:
            for key, value in kwargs.items():
                if hasattr(video, key):
                    setattr(video, key, value)
            self.db.commit()
            self.db.refresh(video)
            return video
        return None

    def get_videos_by_category(self, category: str, skip: int = 0, limit: int = 20) -> List[Video]:
        """Get videos by category"""
        return self.db.query(Video).filter(Video.category == category).offset(skip).limit(limit).all()

    def get_all_videos(self, skip: int = 0, limit: int = 100) -> List[Video]:
        """Get all videos with pagination"""
        return self.db.query(Video).offset(skip).limit(limit).all()

    def get_trending_videos(self, timeframe_days: int = 7, category: Optional[str] = None, limit: int = 20) -> List[Dict[str, Any]]:
        """Get trending videos based on interaction count within a timeframe"""
        cutoff_date = datetime.utcnow() - timedelta(days=timeframe_days)
        
        # Base query to count interactions per video
        query = self.db.query(
            Video,
            func.count(UserInteraction.id).label('interaction_count')
        ).join(
            UserInteraction, 
            UserInteraction.video_id == Video.id
        ).filter(
            UserInteraction.created_at >= cutoff_date
        )
        
        # Apply category filter if specified
        if category:
            query = query.filter(Video.category == category)
        
        # Group by video and order by interaction count
        results = query.group_by(Video.id).order_by(desc('interaction_count')).limit(limit).all()
        
        # Format results
        trending_videos = []
        for video, count in results:
            video_dict = {
                "id": video.id,
                "external_id": video.external_id,
                "title": video.title,
                "description": video.description,
                "category": video.category,
                "interaction_count": count,
                "video_metadata": video.video_metadata
            }
            trending_videos.append(video_dict)
        
        return trending_videos

    def search_videos(self, query: str, skip: int = 0, limit: int = 20) -> List[Video]:
        """Search videos by title or description"""
        search_pattern = f"%{query}%"
        return self.db.query(Video).filter(
            (Video.title.ilike(search_pattern)) | 
            (Video.description.ilike(search_pattern))
        ).offset(skip).limit(limit).all()

    def get_video_interactions(self, video_id: int, interaction_type: Optional[str] = None) -> List[UserInteraction]:
        """Get all interactions for a video, optionally filtered by type"""
        query = self.db.query(UserInteraction).filter(UserInteraction.video_id == video_id)
        if interaction_type:
            query = query.filter(UserInteraction.interaction_type == interaction_type)
        return query.order_by(UserInteraction.created_at.desc()).all() 