import sys
print(f"Python version: {sys.version}")
print(f"Python executable: {sys.executable}")
print(f"Python path: {sys.path}")

try:
    import requests
    print(f"Requests version: {requests.__version__}")
except ImportError:
    print("Failed to import requests")

try:
    import uvicorn
    print(f"Uvicorn version: {uvicorn.__version__}")
except ImportError:
    print("Failed to import uvicorn")

try:
    import fastapi
    print(f"FastAPI version: {fastapi.__version__}")
except ImportError:
    print("Failed to import fastapi")

try:
    import sqlalchemy
    print(f"SQLAlchemy version: {sqlalchemy.__version__}")
except ImportError:
    print("Failed to import sqlalchemy")

try:
    import alembic
    print(f"Alembic version: {alembic.__version__}")
except ImportError:
    print("Failed to import alembic")

try:
    import pydantic_settings
    print(f"Pydantic-settings version: {pydantic_settings.__version__}")
except ImportError:
    print("Failed to import pydantic_settings")

try:
    import dotenv
    print(f"Python-dotenv version: {dotenv.__version__}")
except ImportError:
    print("Failed to import dotenv") 