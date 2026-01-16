from dotenv import load_dotenv
import os
from pathlib import Path

# Option 1: Relative path from current file
load_dotenv(dotenv_path='.env', encoding='latin-1')

# Option 2: Absolute path
load_dotenv(dotenv_path='/mnt/c/Users/hp/Desktop/Urban-ETA-ML-Platform/.env', encoding='latin-1')

# Option 3: Using Path (recommended - works cross-platform)
BASE_DIR = Path(__file__).resolve().parent.parent  # Goes up to project root
ENV_PATH = BASE_DIR / '.env'
load_dotenv(dotenv_path=ENV_PATH, encoding='latin-1')

# Option 4: Explicit path with os.path
env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
load_dotenv(dotenv_path=env_path, encoding='latin-1')

DB_USER = os.getenv("DB_USER", "postgres")
PASSWORD = os.getenv("PASSWORD")
PORT = os.getenv("PORT", "5432")
HOST = os.getenv("HOST")
DATABASE = os.getenv("DATABASE")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")