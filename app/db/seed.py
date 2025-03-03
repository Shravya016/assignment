import json
import random
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from ..models.database import User, Video, UserInteraction, RecommendationCache, MoodBasedCache
from .session import SessionLocal

# Sample data for seeding
USERS = [
    {"username": "john_doe", "device_type": 1, "location_type": 2, "preferences": {"categories": ["motivation", "fitness", "business"]}},
    {"username": "jane_smith", "device_type": 2, "location_type": 1, "preferences": {"categories": ["mindfulness", "health", "creativity"]}},
    {"username": "alex_wilson", "device_type": 1, "location_type": 3, "preferences": {"categories": ["productivity", "technology", "science"]}},
    {"username": "emma_brown", "device_type": 3, "location_type": 2, "preferences": {"categories": ["relationships", "spirituality", "personal-growth"]}},
    {"username": "michael_johnson", "device_type": 2, "location_type": 1, "preferences": {"categories": ["leadership", "finance", "entrepreneurship"]}},
]

VIDEOS = [
    {
        "external_id": "vid_001", 
        "title": "Finding Your Purpose", 
        "description": "An inspiring talk about discovering your life's purpose and passion.",
        "category": "motivation",
        "video_metadata": {"duration": 420, "tags": ["purpose", "inspiration", "motivation"], "speaker": "John Maxwell"}
    },
    {
        "external_id": "vid_002", 
        "title": "Mindfulness Meditation Guide", 
        "description": "A calming guide to mindfulness meditation practices for beginners.",
        "category": "mindfulness",
        "video_metadata": {"duration": 600, "tags": ["meditation", "mindfulness", "peace"], "speaker": "Sarah Wilson"}
    },
    {
        "external_id": "vid_003", 
        "title": "Building Healthy Relationships", 
        "description": "Learn the keys to building and maintaining healthy relationships in your life.",
        "category": "relationships",
        "video_metadata": {"duration": 540, "tags": ["relationships", "communication", "love"], "speaker": "Dr. Emily Johnson"}
    },
    {
        "external_id": "vid_004", 
        "title": "Entrepreneurship 101", 
        "description": "Essential lessons for aspiring entrepreneurs and business leaders.",
        "category": "entrepreneurship",
        "video_metadata": {"duration": 720, "tags": ["business", "startup", "entrepreneurship"], "speaker": "Mark Cuban"}
    },
    {
        "external_id": "vid_005", 
        "title": "Daily Fitness Routine", 
        "description": "A simple yet effective daily fitness routine you can do at home.",
        "category": "fitness",
        "video_metadata": {"duration": 480, "tags": ["fitness", "health", "exercise"], "speaker": "Alex Fitness"}
    },
    {
        "external_id": "vid_006", 
        "title": "Productivity Hacks", 
        "description": "Simple productivity hacks to transform your work and life.",
        "category": "productivity",
        "video_metadata": {"duration": 510, "tags": ["productivity", "time-management", "efficiency"], "speaker": "Tim Ferriss"}
    },
    {
        "external_id": "vid_007", 
        "title": "Financial Freedom", 
        "description": "Steps to achieve financial freedom and build wealth.",
        "category": "finance",
        "video_metadata": {"duration": 660, "tags": ["finance", "wealth", "investing"], "speaker": "Robert Kiyosaki"}
    },
    {
        "external_id": "vid_008", 
        "title": "Leadership Principles", 
        "description": "Core principles of effective leadership in any organization.",
        "category": "leadership",
        "video_metadata": {"duration": 540, "tags": ["leadership", "management", "success"], "speaker": "Simon Sinek"}
    },
    {
        "external_id": "vid_009", 
        "title": "Spiritual Growth", 
        "description": "Exploring the path to spiritual growth and enlightenment.",
        "category": "spirituality",
        "video_metadata": {"duration": 600, "tags": ["spirituality", "growth", "enlightenment"], "speaker": "Deepak Chopra"}
    },
    {
        "external_id": "vid_010", 
        "title": "Technology Trends", 
        "description": "Exploring the latest trends in technology and their impact on society.",
        "category": "technology",
        "video_metadata": {"duration": 480, "tags": ["technology", "innovation", "future"], "speaker": "Elon Musk"}
    },
]

INTERACTION_TYPES = ["view", "like", "inspire", "rate"]

def seed_database():
    """Seed the database with initial data"""
    db = SessionLocal()
    try:
        # Check if data already exists
        if db.query(User).count() > 0:
            print("Database already seeded. Skipping...")
            return
        
        # Seed users
        db_users = []
        for user_data in USERS:
            user = User(
                username=user_data["username"],
                device_type=user_data["device_type"],
                location_type=user_data["location_type"],
                preferences=user_data["preferences"],
                created_at=datetime.utcnow(),
                last_active=datetime.utcnow()
            )
            db.add(user)
            db_users.append(user)
        db.commit()
        
        # Seed videos
        db_videos = []
        for video_data in VIDEOS:
            video = Video(
                external_id=video_data["external_id"],
                title=video_data["title"],
                description=video_data["description"],
                category=video_data["category"],
                video_metadata=video_data["video_metadata"],
                created_at=datetime.utcnow() - timedelta(days=random.randint(1, 30))
            )
            db.add(video)
            db_videos.append(video)
        db.commit()
        
        # Seed user interactions
        for user in db_users:
            # Each user interacts with a random subset of videos
            for video in random.sample(db_videos, random.randint(3, 7)):
                # Generate 1-3 random interactions per video
                for _ in range(random.randint(1, 3)):
                    interaction_type = random.choice(INTERACTION_TYPES)
                    value = random.uniform(3.0, 5.0) if interaction_type == "rate" else None
                    
                    # Create context data
                    context = {
                        "time_of_day": random.randint(0, 23),
                        "day_of_week": random.randint(0, 6),
                        "device_type": user.device_type,
                        "location_type": user.location_type,
                        "session_duration": random.randint(60, 3600)
                    }
                    
                    interaction = UserInteraction(
                        user_id=user.id,
                        video_id=video.id,
                        interaction_type=interaction_type,
                        value=value,
                        created_at=datetime.utcnow() - timedelta(days=random.randint(0, 14)),
                        context=context
                    )
                    db.add(interaction)
        db.commit()
        
        # Seed mood-based cache
        moods = ["happy", "sad", "motivated", "stressed", "relaxed"]
        for mood in moods:
            # Select random videos for each mood
            mood_videos = random.sample(db_videos, random.randint(3, 5))
            recommendations = [
                {
                    "video_id": video.id,
                    "title": video.title,
                    "score": random.uniform(0.7, 0.95)
                }
                for video in mood_videos
            ]
            
            mood_cache = MoodBasedCache(
                mood=mood,
                recommendations=recommendations,
                created_at=datetime.utcnow(),
                is_valid=True
            )
            db.add(mood_cache)
        db.commit()
        
        print("Database seeded successfully!")
    
    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_database() 