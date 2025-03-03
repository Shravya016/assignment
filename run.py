import uvicorn
import os
import logging
from app.db.seed import seed_database

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    try:
        # Seed the database with initial data
        print("Seeding database...")
        seed_database()
        
        # Print environment info
        print(f"Python path: {os.environ.get('PYTHONPATH', 'Not set')}")
        print(f"Current working directory: {os.getcwd()}")
        print(f"Running on port: {os.getenv('PORT', 8000)}")
        
        # Run the application
        print("Starting the application...")
        uvicorn.run(
            "app.main:app", 
            host="0.0.0.0", 
            port=int(os.getenv("PORT", 8000)), 
            reload=True,
            log_level="debug"
        )
    except Exception as e:
        logger.exception(f"Application failed to start: {e}") 