from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
from ..models.database import User, UserInteraction
from datetime import datetime

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_username(self, username: str) -> Optional[User]:
        """Get a user by username"""
        return self.db.query(User).filter(User.username == username).first()

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get a user by ID"""
        return self.db.query(User).filter(User.id == user_id).first()

    def create_user(self, username: str, device_type: int = 0, location_type: int = 0, preferences: Dict = None) -> User:
        """Create a new user"""
        user = User(
            username=username,
            device_type=device_type,
            location_type=location_type,
            preferences=preferences or {},
            created_at=datetime.utcnow(),
            last_active=datetime.utcnow()
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update_user_activity(self, user_id: int) -> None:
        """Update user's last active timestamp"""
        user = self.get_user_by_id(user_id)
        if user:
            user.last_active = datetime.utcnow()
            self.db.commit()

    def update_user_preferences(self, user_id: int, preferences: Dict) -> Optional[User]:
        """Update user preferences"""
        user = self.get_user_by_id(user_id)
        if user:
            user.preferences = preferences
            self.db.commit()
            self.db.refresh(user)
            return user
        return None

    def get_user_interactions(self, user_id: int, interaction_type: Optional[str] = None) -> List[UserInteraction]:
        """Get all interactions for a user, optionally filtered by type"""
        query = self.db.query(UserInteraction).filter(UserInteraction.user_id == user_id)
        if interaction_type:
            query = query.filter(UserInteraction.interaction_type == interaction_type)
        return query.order_by(UserInteraction.created_at.desc()).all()

    def get_all_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Get all users with pagination"""
        return self.db.query(User).offset(skip).limit(limit).all()

    def get_active_users(self, days: int = 7, limit: int = 100) -> List[User]:
        """Get users active in the last X days"""
        cutoff_date = datetime.utcnow() - datetime.timedelta(days=days)
        return self.db.query(User).filter(User.last_active >= cutoff_date).limit(limit).all() 