# import tensorflow as tf
import numpy as np
import json
import os
import random
from datetime import datetime

class VideoRecommendationModel:
    """
    A simplified recommendation model that doesn't require TensorFlow for testing.
    This is a temporary solution until TensorFlow is properly installed.
    """
    def __init__(self):
        self.is_initialized = True
        print("Initialized simplified recommendation model")
    
    def recommend_for_user(self, user_id, preferences=None, location=None, time_of_day=None, recent_interactions=None, limit=10):
        """
        Return random recommendations for testing
        """
        # Simulate video recommendations with random data
        sample_videos = []
        
        # Create some sample videos
        for i in range(limit):
            video_id = f"vid_{i+1:03d}"
            sample_videos.append({
                "id": video_id,
                "external_id": video_id,
                "title": f"Sample Video {i+1}",
                "description": f"This is a sample video description for testing purposes #{i+1}",
                "url": f"https://example.com/videos/{video_id}",
                "thumbnail_url": f"https://example.com/thumbnails/{video_id}.jpg",
                "category": random.choice(["Entertainment", "Music", "Sports", "News", "Education"]),
                "tags": ["sample", "testing", f"tag{i}"],
                "duration": random.randint(60, 600),  # 1-10 minutes
                "views": random.randint(100, 10000),
                "likes": random.randint(10, 1000),
                "created_at": datetime.now().isoformat(),
                "publisher": f"Publisher {i % 5 + 1}",
                "confidence_score": round(random.uniform(0.5, 0.99), 2)
            })
        
        return sample_videos
    
    def recommend_trending(self, timeframe="day", category=None, limit=10):
        """
        Return random trending videos for testing
        """
        # Similar to recommend_for_user but with higher view counts
        trending_videos = []
        
        for i in range(limit):
            video_id = f"trending_{i+1:03d}"
            trending_videos.append({
                "id": video_id,
                "external_id": video_id,
                "title": f"Trending Video {i+1}",
                "description": f"This is a trending video description for {timeframe} #{i+1}",
                "url": f"https://example.com/videos/{video_id}",
                "thumbnail_url": f"https://example.com/thumbnails/{video_id}.jpg",
                "category": category or random.choice(["Entertainment", "Music", "Sports", "News", "Education"]),
                "tags": ["trending", timeframe, f"tag{i}"],
                "duration": random.randint(60, 600),  # 1-10 minutes
                "views": random.randint(10000, 1000000),  # Higher view counts
                "likes": random.randint(1000, 100000),
                "created_at": datetime.now().isoformat(),
                "publisher": f"Popular Publisher {i % 5 + 1}",
                "trending_score": round(random.uniform(0.7, 0.99), 2)
            })
        
        return trending_videos
    
    def recommend_by_mood(self, mood, limit=10):
        """
        Return mood-based recommendations for testing
        """
        mood_videos = []
        
        # Create videos that match the specified mood
        mood_categories = {
            "happy": ["Comedy", "Music", "Entertainment"],
            "sad": ["Drama", "Documentary", "Music"],
            "excited": ["Sports", "Action", "Adventure"],
            "relaxed": ["Nature", "Meditation", "ASMR"],
            "focused": ["Education", "Science", "Technology"]
        }
        
        categories = mood_categories.get(mood.lower(), ["General"])
        
        for i in range(limit):
            video_id = f"{mood}_{i+1:03d}"
            mood_videos.append({
                "id": video_id,
                "external_id": video_id,
                "title": f"{mood.capitalize()} Video {i+1}",
                "description": f"This video is perfect for a {mood} mood #{i+1}",
                "url": f"https://example.com/videos/{video_id}",
                "thumbnail_url": f"https://example.com/thumbnails/{video_id}.jpg",
                "category": random.choice(categories),
                "tags": [mood, "recommendation", f"tag{i}"],
                "duration": random.randint(60, 600),  # 1-10 minutes
                "views": random.randint(1000, 50000),
                "likes": random.randint(100, 5000),
                "created_at": datetime.now().isoformat(),
                "publisher": f"Mood Publisher {i % 5 + 1}",
                "mood_match_score": round(random.uniform(0.6, 0.95), 2)
            })
        
        return mood_videos