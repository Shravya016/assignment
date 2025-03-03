from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
from ..models.database import RecommendationCache, MoodBasedCache
from datetime import datetime, timedelta

class RecommendationRepository:
    def __init__(self, db: Session):
        self.db = db
        self.cache_ttl = 3600  # Default cache TTL in seconds (1 hour)

    def set_cache_ttl(self, seconds: int) -> None:
        """Set the cache time-to-live in seconds"""
        self.cache_ttl = seconds

    def get_user_recommendations_cache(self, user_id: int) -> Optional[RecommendationCache]:
        """Get cached recommendations for a user if they exist and are valid"""
        cutoff_time = datetime.utcnow() - timedelta(seconds=self.cache_ttl)
        
        cache = self.db.query(RecommendationCache).filter(
            RecommendationCache.user_id == user_id,
            RecommendationCache.is_valid == True,
            RecommendationCache.created_at >= cutoff_time
        ).order_by(RecommendationCache.created_at.desc()).first()
        
        return cache

    def cache_user_recommendations(
        self, 
        user_id: int, 
        recommendations: List[Dict[str, Any]],
        context: Optional[Dict[str, Any]] = None
    ) -> RecommendationCache:
        """Cache recommendations for a user"""
        # Invalidate existing caches for this user
        self._invalidate_user_caches(user_id)
        
        # Create new cache entry
        cache = RecommendationCache(
            user_id=user_id,
            recommendations=recommendations,
            context=context or {},
            created_at=datetime.utcnow(),
            is_valid=True
        )
        self.db.add(cache)
        self.db.commit()
        self.db.refresh(cache)
        return cache

    def _invalidate_user_caches(self, user_id: int) -> None:
        """Invalidate all existing caches for a user"""
        self.db.query(RecommendationCache).filter(
            RecommendationCache.user_id == user_id,
            RecommendationCache.is_valid == True
        ).update({"is_valid": False})
        self.db.commit()

    def get_mood_based_recommendations(self, mood: str) -> Optional[MoodBasedCache]:
        """Get cached mood-based recommendations if they exist and are valid"""
        cutoff_time = datetime.utcnow() - timedelta(seconds=self.cache_ttl)
        
        cache = self.db.query(MoodBasedCache).filter(
            MoodBasedCache.mood == mood,
            MoodBasedCache.is_valid == True,
            MoodBasedCache.created_at >= cutoff_time
        ).order_by(MoodBasedCache.created_at.desc()).first()
        
        return cache

    def cache_mood_based_recommendations(
        self, 
        mood: str, 
        recommendations: List[Dict[str, Any]]
    ) -> MoodBasedCache:
        """Cache mood-based recommendations"""
        # Invalidate existing caches for this mood
        self._invalidate_mood_caches(mood)
        
        # Create new cache entry
        cache = MoodBasedCache(
            mood=mood,
            recommendations=recommendations,
            created_at=datetime.utcnow(),
            is_valid=True
        )
        self.db.add(cache)
        self.db.commit()
        self.db.refresh(cache)
        return cache

    def _invalidate_mood_caches(self, mood: str) -> None:
        """Invalidate all existing caches for a mood"""
        self.db.query(MoodBasedCache).filter(
            MoodBasedCache.mood == mood,
            MoodBasedCache.is_valid == True
        ).update({"is_valid": False})
        self.db.commit()

    def clear_all_caches(self) -> None:
        """Clear all recommendation caches"""
        self.db.query(RecommendationCache).update({"is_valid": False})
        self.db.query(MoodBasedCache).update({"is_valid": False})
        self.db.commit() 