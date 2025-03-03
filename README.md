# Video Recommendation Engine

A sophisticated recommendation system that suggests personalized video content based on user preferences and engagement patterns using deep neural networks. The system is designed to work with the Empowerverse App platform and provides intelligent content recommendations.

## 🎯 Features

- Personalized content recommendations using deep neural networks
- Mood-based recommendations for cold start problems
- Category-based filtering
- Trending content detection
- Efficient data caching and pagination
- Real-time API integration with Empowerverse platform

## 🎥 Demo

Check out this video demonstration of our API endpoints in action:

https://github.com/Shravya016/assignment/blob/main/demo/Screen%20Recording%202025-03-03%20130819.mp4

The demo showcases:
- Authentication using Flic-Token
- Fetching personalized video recommendations
- Getting trending videos
- Retrieving mood-based recommendations
- Interacting with user and video endpoints

## 🛠️ Technology Stack

- **Backend Framework**: FastAPI
- **Machine Learning**: TensorFlow
- **Documentation**: Swagger/OpenAPI
- **Database**: SQLite (configurable)
- **API Integration**: aiohttp

## 📋 Prerequisites

- Python 3.8+
- Virtual environment (recommended)
- Flic-Token for API authentication

## 🚀 Getting Started

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Shravya016/assignment.git
   cd video-recommendation-engine
   ```

2. **Set Up Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**
   Create a `.env` file in the root directory with the following content:
   ```
   FLIC_TOKEN=flic_11d3da28e403d182c36a3530453e290add87d0b4a40ee50f17611f180d47956f
   API_BASE_URL=https://api.socialverseapp.com
   DATABASE_URL=sqlite:///./video_recommendation.db 
   ```

5. **Start the Server**
   ```bash
   uvicorn app.main:app --reload
   ```

## 📊 API Endpoints

### Main Recommendation Endpoints

- **Get Personalized Feed**
  ```
  GET /api/v1/feed?username={username}
  ```
  Returns personalized video recommendations for a specific user.

- **Get Category-based Feed**
  ```
  GET /api/v1/feed?username={username}&category_id={category_id}
  ```
  Returns category-specific video recommendations for a user.

- **Get Trending Videos**
  ```
  GET /api/v1/trending?timeframe={timeframe}
  ```
  Returns trending videos based on recent engagement.

- **Get Mood-based Recommendations**
  ```
  GET /api/v1/mood-based?mood={mood}
  ```
  Returns recommendations based on user's current mood.

### Data Collection Endpoints

- **Get Viewed Posts**
  ```
  GET /api/v1/posts/viewed
  ```

- **Get Liked Posts**
  ```
  GET /api/v1/posts/liked
  ```

- **Get Inspired Posts**
  ```
  GET /api/v1/posts/inspired
  ```

- **Get Rated Posts**
  ```
  GET /api/v1/posts/rated
  ```

## 🧮 Algorithm Implementation

The recommendation engine uses a Deep Neural Network (DNN) architecture with the following components:

### Data Preprocessing
- Feature engineering
- Data normalization
- Missing value handling
- Categorical encoding

### Model Architecture
- Embedding layers for categorical features
- Dense layers with ReLU activation
- Dropout for regularization
- Output layer with appropriate activation

### Cold Start Handling
- Mood-based initial recommendations
- Content-based filtering fallback
- Popularity-based recommendations

## 📝 API Documentation

Once the server is running, you can access the interactive API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 🔒 Security

- All API endpoints require authentication using the Flic-Token header
- Environment variables are used for sensitive configuration
- Input validation and sanitization
- Rate limiting implemented


## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details. 
