import requests
import json
import sys

# Base URL for the API
BASE_URL = "http://127.0.0.1:8000"

# Test the health endpoint
def test_health():
    try:
        print("Attempting to connect to health endpoint...")
        response = requests.get(f"{BASE_URL}/health")
        print(f"Health Check Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error connecting to health endpoint: {e}")
    
# Test the API documentation
def test_docs():
    try:
        print("Attempting to connect to docs endpoint...")
        response = requests.get(f"{BASE_URL}/docs")
        print(f"Docs Status: {response.status_code}")
        print(f"Docs available: {response.status_code == 200}")
    except Exception as e:
        print(f"Error connecting to docs endpoint: {e}")

# Test getting all users
def test_get_users():
    try:
        print("Attempting to get users...")
        headers = {"Flic-Token": "flic_11d3da28e403d182c36a3530453e290add87d0b4a40ee50f17611f180d47956f"}
        response = requests.get(f"{BASE_URL}/api/v1/users", headers=headers)
        print(f"Get Users Status: {response.status_code}")
        if response.status_code == 200:
            users = response.json()
            print(f"Number of users: {len(users)}")
            if len(users) > 0:
                print(f"First user: {users[0]['username']}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Error connecting to users endpoint: {e}")

# Test getting trending videos
def test_trending_videos():
    try:
        print("Attempting to get trending videos...")
        headers = {"Flic-Token": "flic_11d3da28e403d182c36a3530453e290add87d0b4a40ee50f17611f180d47956f"}
        response = requests.get(f"{BASE_URL}/api/v1/trending?timeframe=day", headers=headers)
        print(f"Trending Videos Status: {response.status_code}")
        if response.status_code == 200:
            videos = response.json()
            print(f"Number of trending videos: {len(videos)}")
            if len(videos) > 0:
                print(f"First trending video: {videos[0]['title']}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Error connecting to trending endpoint: {e}")

# Test getting personalized feed
def test_personalized_feed():
    try:
        print("Attempting to get personalized feed...")
        headers = {"Flic-Token": "flic_11d3da28e403d182c36a3530453e290add87d0b4a40ee50f17611f180d47956f"}
        response = requests.get(f"{BASE_URL}/api/v1/feed?username=john_doe", headers=headers)
        print(f"Personalized Feed Status: {response.status_code}")
        if response.status_code == 200:
            recommendations = response.json()
            print(f"Number of recommendations: {len(recommendations)}")
            if len(recommendations) > 0:
                print(f"First recommendation: {recommendations[0]['title']}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Error connecting to feed endpoint: {e}")

# Test recording an interaction
def test_record_interaction():
    try:
        print("Attempting to record interaction...")
        headers = {"Flic-Token": "flic_11d3da28e403d182c36a3530453e290add87d0b4a40ee50f17611f180d47956f"}
        response = requests.post(
            f"{BASE_URL}/api/v1/interaction?username=john_doe&video_external_id=vid_001&interaction_type=view", 
            headers=headers
        )
        print(f"Record Interaction Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"Interaction recorded: {result}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Error connecting to interaction endpoint: {e}")

if __name__ == "__main__":
    print("Testing Video Recommendation Engine API...")
    print(f"Python version: {sys.version}")
    print(f"Requests version: {requests.__version__}")
    
    print("\n1. Health Check:")
    test_health()
    
    print("\n2. API Documentation:")
    test_docs()
    
    print("\n3. Get Users:")
    test_get_users()
    
    print("\n4. Trending Videos:")
    test_trending_videos()
    
    print("\n5. Personalized Feed:")
    test_personalized_feed()
    
    print("\n6. Record Interaction:")
    test_record_interaction()
    
    print("\nAPI Testing Complete!") 