import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

SERVICE_NAME = os.getenv("SERVICE_NAME", "checking")
BASE_DIR = Path(__file__).resolve().parent.parent
LOGS_DIR = BASE_DIR / "logs" / SERVICE_NAME

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///database.sqlite3")
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017?replicaSet=rs0")

LOGIN_LOGOUT_SERVICE_TOKEN = os.getenv("LOGIN_LOGOUT_SERVICE_TOKEN", "SecretToken")
LOGIN_LOGOUT_SERVICE_HEADER_NAME = "x-auth-token"

TEST_DATABASE_URL = "sqlite:///:memory:"
