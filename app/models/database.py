from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, index=True)
    device_type = Column(Integer)
    location_type = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_active = Column(DateTime, default=datetime.utcnow)
    preferences = Column(JSON)

    interactions = relationship("UserInteraction", back_populates="user")

class Video(Base):
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True)
    external_id = Column(String, unique=True, index=True)
    title = Column(String)
    description = Column(String)
    category = Column(String, index=True)
    video_metadata = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    interactions = relationship("UserInteraction", back_populates="video")

class UserInteraction(Base):
    __tablename__ = "user_interactions"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    video_id = Column(Integer, ForeignKey("videos.id"))
    interaction_type = Column(String)  # view, like, inspire, rate
    value = Column(Float, nullable=True)  # For ratings
    created_at = Column(DateTime, default=datetime.utcnow)
    context = Column(JSON)  # Store context features

    user = relationship("User", back_populates="interactions")
    video = relationship("Video", back_populates="interactions")

class RecommendationCache(Base):
    __tablename__ = "recommendation_cache"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    recommendations = Column(JSON)
    context = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_valid = Column(Boolean, default=True)

class MoodBasedCache(Base):
    __tablename__ = "mood_based_cache"

    id = Column(Integer, primary_key=True)
    mood = Column(String, index=True)
    recommendations = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_valid = Column(Boolean, default=True) 