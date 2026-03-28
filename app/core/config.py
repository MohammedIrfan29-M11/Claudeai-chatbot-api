import os
from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

if not ANTHROPIC_API_KEY:
    raise ValueError("ANTHROPIC_API_KEY is not set in .env file")


# Centralized validation constants which can be updated at any time in the application
MAX_MESSAGE_LENGTH = 2000
MIN_MESSAGE_LENGTH = 1
MAX_HISTORY_LENGTH = 20
RATE_LIMIT_REQUESTS = 10
RATE_LIMIT_WINDOW = 60
