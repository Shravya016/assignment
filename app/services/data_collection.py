import aiohttp
import asyncio
from typing import Dict, List, Any, Optional
from ..core.config import settings
import json
from datetime import datetime, timedelta

class DataCollectionService:
    def __init__(self):
        self.base_url = settings.API_BASE_URL
        self.headers = {"Flic-Token": settings.FLIC_TOKEN}

    async def _make_request(self, endpoint: str, params: Optional[Dict] = None) -> Dict:
        """Make an HTTP request to the API"""
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.base_url}/{endpoint}",
                headers=self.headers,
                params=params
            ) as response:
                if response.status != 200:
                    raise Exception(f"API request failed: {await response.text()}")
                return await response.json()

    async def get_user_data(self, username: str) -> Dict[str, Any]:
        """Get user data and interaction history"""
        # Get basic user info
        users = await self._make_request(
            "users/get_all",
            {"page": 1, "page_size": 1000}
        )
        user = next((u for u in users if u["username"] == username), None)
        if not user:
            raise Exception(f"User {username} not found")

        # Get user's interaction history
        viewed_posts = await self._make_request(
            "posts/view",
            {
                "page": 1,
                "page_size": 1000,
                "resonance_algorithm": "resonance_algorithm_cjsvervb7dbhss8bdrj89s44jfjdbsjd0xnjkbvuire8zcjwerui3njfbvsujc5if"
            }
        )
        
        liked_posts = await self._make_request(
            "posts/like",
            {
                "page": 1,
                "page_size": 1000,
                "resonance_algorithm": "resonance_algorithm_cjsvervb7dbhss8bdrj89s44jfjdbsjd0xnjkbvuire8zcjwerui3njfbvsujc5if"
            }
        )
        
        inspired_posts = await self._make_request(
            "posts/inspire",
            {
                "page": 1,
                "page_size": 1000,
                "resonance_algorithm": "resonance_algorithm_cjsvervb7dbhss8bdrj89s44jfjdbsjd0xnjkbvuire8zcjwerui3njfbvsujc5if"
            }
        )

        # Combine user data
        now = datetime.now()
        return {
            "user_id": user["id"],
            "username": username,
            "time_of_day": now.hour,
            "day_of_week": now.weekday(),
            "device_type": user.get("device_type", 0),
            "location_type": user.get("location_type", 0),
            "session_duration": 0,  # This should be tracked in real-time
            "has_history": bool(viewed_posts or liked_posts or inspired_posts),
            "viewed_posts": viewed_posts,
            "liked_posts": liked_posts,
            "inspired_posts": inspired_posts
        }

    async def get_video_data(self, video_id: int) -> Dict[str, Any]:
        """Get video metadata"""
        posts = await self._make_request(
            "posts/summary/get",
            {"page": 1, "page_size": 1000}
        )
        video = next((p for p in posts if p["id"] == video_id), None)
        if not video:
            raise Exception(f"Video {video_id} not found")
        return video

    async def get_item_category(self, item_id: int) -> str:
        """Get category for a specific item"""
        video = await self.get_video_data(item_id)
        return video.get("category", "unknown")

    async def get_trending_videos(
        self,
        timeframe: str,
        category_id: Optional[str] = None,
        page: int = 1,
        page_size: int = 20
    ) -> List[Dict[str, Any]]:
        """Get trending videos based on recent engagement"""
        # Calculate time window
        now = datetime.now()
        time_windows = {
            "hour": now - timedelta(hours=1),
            "day": now - timedelta(days=1),
            "week": now - timedelta(weeks=1),
            "month": now - timedelta(days=30)
        }
        since = time_windows[timeframe]

        # Get all interactions
        posts = await self._make_request(
            "posts/summary/get",
            {"page": page, "page_size": page_size}
        )

        # Filter by category if specified
        if category_id:
            posts = [p for p in posts if p.get("category") == category_id]

        # Sort by engagement score
        posts.sort(key=lambda x: (
            x.get("views", 0) + 
            x.get("likes", 0) * 2 + 
            x.get("inspires", 0) * 3
        ), reverse=True)

        return posts[:page_size]

    async def get_mood_based_recommendations(
        self,
        mood: str,
        page: int = 1,
        page_size: int = 20
    ) -> List[Dict[str, Any]]:
        """Get recommendations based on user's mood"""
        # Get all posts
        posts = await self._make_request(
            "posts/summary/get",
            {"page": page, "page_size": page_size}
        )

        # Filter and score posts based on mood
        mood_keywords = {
            "happy": ["inspiring", "motivational", "uplifting", "positive"],
            "sad": ["comforting", "peaceful", "calming", "supportive"],
            "motivated": ["energetic", "ambitious", "goal-oriented", "success"],
            "stressed": ["relaxing", "meditation", "mindfulness", "peaceful"],
            # Add more moods and associated keywords
        }

        keywords = mood_keywords.get(mood.lower(), [])
        
        # Score posts based on mood relevance
        scored_posts = []
        for post in posts:
            score = sum(
                1 for keyword in keywords 
                if keyword.lower() in post.get("description", "").lower()
            )
            if score > 0:
                scored_posts.append((score, post))

        # Sort by relevance score
        scored_posts.sort(key=lambda x: x[0], reverse=True)
        
        # Return top matching posts
        return [post for _, post in scored_posts[:page_size]] 