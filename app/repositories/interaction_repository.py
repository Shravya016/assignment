from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
from ..models.database import UserInteraction, User, Video
from datetime import datetime

class InteractionRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_interaction(
        self, 
        user_id: int, 
        video_id: int, 
        interaction_type: str,
        value: Optional[float] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> UserInteraction:
        """Create a new user-video interaction"""
        interaction = UserInteraction(
            user_id=user_id,
            video_id=video_id,
            interaction_type=interaction_type,
            value=value,
            context=context or {},
            created_at=datetime.utcnow()
        )
        self.db.add(interaction)
        self.db.commit()
        self.db.refresh(interaction)
        return interaction

    def get_interaction_by_id(self, interaction_id: int) -> Optional[UserInteraction]:
        """Get an interaction by ID"""
        return self.db.query(UserInteraction).filter(UserInteraction.id == interaction_id).first()

    def get_user_video_interactions(
        self, 
        user_id: int, 
        video_id: int,
        interaction_type: Optional[str] = None
    ) -> List[UserInteraction]:
        """Get interactions between a specific user and video"""
        query = self.db.query(UserInteraction).filter(
            UserInteraction.user_id == user_id,
            UserInteraction.video_id == video_id
        )
        if interaction_type:
            query = query.filter(UserInteraction.interaction_type == interaction_type)
        return query.order_by(UserInteraction.created_at.desc()).all()

    def get_latest_interactions(self, limit: int = 100) -> List[UserInteraction]:
        """Get the latest interactions across all users and videos"""
        return self.db.query(UserInteraction).order_by(UserInteraction.created_at.desc()).limit(limit).all()

    def get_interaction_stats(self, video_id: int) -> Dict[str, int]:
        """Get interaction statistics for a video"""
        stats = {}
        for interaction_type in ["view", "like", "inspire", "rate"]:
            count = self.db.query(UserInteraction).filter(
                UserInteraction.video_id == video_id,
                UserInteraction.interaction_type == interaction_type
            ).count()
            stats[interaction_type] = count
        
        # Calculate average rating if applicable
        ratings = self.db.query(UserInteraction).filter(
            UserInteraction.video_id == video_id,
            UserInteraction.interaction_type == "rate"
        ).all()
        
        if ratings:
            avg_rating = sum(r.value for r in ratings if r.value is not None) / len(ratings)
            stats["average_rating"] = round(avg_rating, 1)
        else:
            stats["average_rating"] = 0
            
        return stats

    def delete_interaction(self, interaction_id: int) -> bool:
        """Delete an interaction by ID"""
        interaction = self.get_interaction_by_id(interaction_id)
        if interaction:
            self.db.delete(interaction)
            self.db.commit()
            return True
        return False

    def get_user_interaction_history(self, user_id: int, limit: int = 50) -> List[Dict[str, Any]]:
        """Get a user's interaction history with detailed video information"""
        interactions = self.db.query(
            UserInteraction, Video
        ).join(
            Video, UserInteraction.video_id == Video.id
        ).filter(
            UserInteraction.user_id == user_id
        ).order_by(
            UserInteraction.created_at.desc()
        ).limit(limit).all()
        
        history = []
        for interaction, video in interactions:
            history.append({
                "interaction_id": interaction.id,
                "interaction_type": interaction.interaction_type,
                "value": interaction.value,
                "created_at": interaction.created_at,
                "video_id": video.id,
                "video_title": video.title,
                "video_category": video.category,
                "video_external_id": video.external_id
            })
        
        return history 