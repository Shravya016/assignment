from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
import numpy as np
from datetime import datetime

from ..repositories.user_repository import UserRepository
from ..repositories.video_repository import VideoRepository
from ..repositories.interaction_repository import InteractionRepository
from ..repositories.recommendation_repository import RecommendationRepository
from ..models.recommendation_model import VideoRecommendationModel
from ..core.config import settings

class RecommendationService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)
        self.video_repo = VideoRepository(db)
        self.interaction_repo = InteractionRepository(db)
        self.recommendation_repo = RecommendationRepository(db)
        
        # Initialize the model with dimensions based on the database
        self.model = self._initialize_model()
    
    def _initialize_model(self) -> VideoRecommendationModel:
        """Initialize the recommendation model with appropriate dimensions"""
        # Get the number of users and videos in the database
        user_count = self.db.query(self.user_repo.db.query(self.user_repo.db.func.max(self.user_repo.db.model.User.id)).scalar() or 0).scalar() + 1
        video_count = self.db.query(self.video_repo.db.query(self.video_repo.db.func.max(self.video_repo.db.model.Video.id)).scalar() or 0).scalar() + 1
        
        # Ensure minimum dimensions
        user_count = max(user_count, 100)
        video_count = max(video_count, 100)
        
        return VideoRecommendationModel(num_users=user_count, num_items=video_count)
    
    def get_personalized_recommendations(
        self, 
        username: str, 
        category_id: Optional[str] = None,
        page: int = 1,
        page_size: int = 20
    ) -> List[Dict[str, Any]]:
        """Get personalized recommendations for a user"""
        # Get user data
        user = self.user_repo.get_user_by_username(username)
        if not user:
            raise ValueError(f"User {username} not found")
        
        # Check if we have a valid cache
        cache = self.recommendation_repo.get_user_recommendations_cache(user.id)
        if cache and (not category_id or self._filter_cached_by_category(cache.recommendations, category_id)):
            # We have a valid cache
            recommendations = cache.recommendations
            if category_id:
                recommendations = self._filter_cached_by_category(recommendations, category_id)
            
            # Apply pagination
            start_idx = (page - 1) * page_size
            end_idx = start_idx + page_size
            return recommendations[start_idx:end_idx]
        
        # No valid cache, generate new recommendations
        user_interactions = self.interaction_repo.get_user_interactions(user.id)
        
        # Check if user has history
        if not user_interactions:
            # Cold start case
            return self.get_mood_based_recommendations(
                mood="motivated",  # Default mood for cold start
                page=page,
                page_size=page_size
            )
        
        # Get context features
        context_features = self._extract_context_features(user)
        
        # Generate recommendations using the model
        if hasattr(self.model, 'get_recommendations'):
            model_recommendations = self.model.get_recommendations(
                user_id=user.id,
                context_features=context_features,
                n_recommendations=100  # Get more than needed for filtering
            )
        else:
            # Fallback to a simpler approach if model isn't trained
            model_recommendations = self._get_fallback_recommendations(user.id, 100)
        
        # Enrich recommendations with video data
        recommendations = []
        for rec in model_recommendations:
            video_id = rec["item_id"]
            video = self.video_repo.get_video_by_id(video_id)
            if video:
                # Filter by category if specified
                if category_id and video.category != category_id:
                    continue
                
                # Add video data to recommendation
                recommendation = {
                    "video_id": video.id,
                    "external_id": video.external_id,
                    "title": video.title,
                    "description": video.description,
                    "category": video.category,
                    "score": rec["score"],
                    "video_metadata": video.video_metadata
                }
                recommendations.append(recommendation)
        
        # Cache the recommendations
        self.recommendation_repo.cache_user_recommendations(
            user_id=user.id,
            recommendations=recommendations,
            context={"timestamp": datetime.utcnow().isoformat()}
        )
        
        # Apply pagination
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        return recommendations[start_idx:end_idx]
    
    def _extract_context_features(self, user) -> np.ndarray:
        """Extract context features for the recommendation model"""
        now = datetime.utcnow()
        return np.array([
            [
                now.hour,  # Time of day
                now.weekday(),  # Day of week
                user.device_type,
                user.location_type,
                0  # Session duration (placeholder)
            ]
        ])
    
    def _filter_cached_by_category(self, recommendations: List[Dict[str, Any]], category_id: str) -> List[Dict[str, Any]]:
        """Filter cached recommendations by category"""
        return [r for r in recommendations if r.get("category") == category_id]
    
    def _get_fallback_recommendations(self, user_id: int, limit: int = 20) -> List[Dict[str, Any]]:
        """Generate fallback recommendations based on popularity and user history"""
        # Get user's interaction history
        user_interactions = self.interaction_repo.get_user_interactions(user_id)
        
        # Get videos the user has already interacted with
        interacted_video_ids = set(interaction.video_id for interaction in user_interactions)
        
        # Get trending videos
        trending_videos = self.video_repo.get_trending_videos(timeframe_days=30, limit=limit*2)
        
        # Filter out videos the user has already interacted with
        recommendations = []
        for video in trending_videos:
            if video["id"] not in interacted_video_ids:
                recommendations.append({
                    "item_id": video["id"],
                    "score": 0.5  # Default score
                })
                if len(recommendations) >= limit:
                    break
        
        # If we still need more recommendations, add some random videos
        if len(recommendations) < limit:
            all_videos = self.video_repo.get_all_videos(limit=limit*2)
            for video in all_videos:
                if video.id not in interacted_video_ids and not any(r["item_id"] == video.id for r in recommendations):
                    recommendations.append({
                        "item_id": video.id,
                        "score": 0.3  # Lower score for random recommendations
                    })
                    if len(recommendations) >= limit:
                        break
        
        return recommendations
    
    def get_trending_videos(
        self,
        timeframe: str = "day",
        category_id: Optional[str] = None,
        page: int = 1,
        page_size: int = 20
    ) -> List[Dict[str, Any]]:
        """Get trending videos based on recent engagement"""
        # Convert timeframe to days
        timeframe_days = {
            "hour": 0.04,  # ~1 hour
            "day": 1,
            "week": 7,
            "month": 30
        }.get(timeframe, 1)
        
        # Get trending videos from repository
        trending_videos = self.video_repo.get_trending_videos(
            timeframe_days=timeframe_days,
            category=category_id,
            limit=page_size * page  # Get enough for pagination
        )
        
        # Apply pagination
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        return trending_videos[start_idx:end_idx]
    
    def get_mood_based_recommendations(
        self,
        mood: str,
        page: int = 1,
        page_size: int = 20
    ) -> List[Dict[str, Any]]:
        """Get mood-based video recommendations"""
        # Check if we have a valid cache
        cache = self.recommendation_repo.get_mood_based_recommendations(mood)
        if cache:
            # We have a valid cache
            recommendations = cache.recommendations
            
            # Apply pagination
            start_idx = (page - 1) * page_size
            end_idx = start_idx + page_size
            return recommendations[start_idx:end_idx]
        
        # No valid cache, generate new recommendations
        # Define mood keywords
        mood_keywords = {
            "happy": ["inspiring", "motivational", "uplifting", "positive"],
            "sad": ["comforting", "peaceful", "calming", "supportive"],
            "motivated": ["energetic", "ambitious", "goal-oriented", "success"],
            "stressed": ["relaxing", "meditation", "mindfulness", "peaceful"],
            "relaxed": ["gentle", "soothing", "calm", "peaceful"]
        }
        
        keywords = mood_keywords.get(mood.lower(), [])
        if not keywords:
            # If mood not recognized, use motivated as default
            keywords = mood_keywords["motivated"]
        
        # Get all videos
        all_videos = self.video_repo.get_all_videos(limit=100)
        
        # Score videos based on mood relevance
        scored_videos = []
        for video in all_videos:
            # Calculate relevance score based on keyword matches in title and description
            score = 0
            for keyword in keywords:
                if keyword.lower() in video.title.lower():
                    score += 2  # Higher weight for title matches
                if keyword.lower() in video.description.lower():
                    score += 1
            
            if score > 0:
                scored_videos.append((score, video))
        
        # Sort by relevance score
        scored_videos.sort(key=lambda x: x[0], reverse=True)
        
        # Format recommendations
        recommendations = []
        for score, video in scored_videos:
            recommendations.append({
                "video_id": video.id,
                "external_id": video.external_id,
                "title": video.title,
                "description": video.description,
                "category": video.category,
                "score": min(score / 10, 1.0),  # Normalize score to 0-1 range
                "video_metadata": video.video_metadata
            })
        
        # Cache the recommendations
        self.recommendation_repo.cache_mood_based_recommendations(
            mood=mood,
            recommendations=recommendations
        )
        
        # Apply pagination
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        return recommendations[start_idx:end_idx]
    
    def record_interaction(
        self,
        username: str,
        video_external_id: str,
        interaction_type: str,
        value: Optional[float] = None
    ) -> Dict[str, Any]:
        """Record a user-video interaction"""
        # Get user and video
        user = self.user_repo.get_user_by_username(username)
        if not user:
            raise ValueError(f"User {username} not found")
        
        video = self.video_repo.get_video_by_external_id(video_external_id)
        if not video:
            raise ValueError(f"Video {video_external_id} not found")
        
        # Create context data
        context = {
            "time_of_day": datetime.utcnow().hour,
            "day_of_week": datetime.utcnow().weekday(),
            "device_type": user.device_type,
            "location_type": user.location_type,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # Record the interaction
        interaction = self.interaction_repo.create_interaction(
            user_id=user.id,
            video_id=video.id,
            interaction_type=interaction_type,
            value=value,
            context=context
        )
        
        # Update user's last active timestamp
        self.user_repo.update_user_activity(user.id)
        
        # Invalidate user's recommendation cache
        self.recommendation_repo._invalidate_user_caches(user.id)
        
        return {
            "interaction_id": interaction.id,
            "user_id": user.id,
            "video_id": video.id,
            "interaction_type": interaction_type,
            "value": value,
            "created_at": interaction.created_at
        } 