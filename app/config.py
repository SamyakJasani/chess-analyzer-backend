import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "change-me")
    FRONTEND_ORIGINS = [
        origin.strip()
        for origin in os.getenv(
            "FRONTEND_ORIGINS", "http://localhost:4200"
        ).split(",")
        if origin.strip()
    ]
    EXTERNAL_API_BASE_URL = os.getenv(
        "EXTERNAL_API_BASE_URL", "https://api.chess.com/pub"
    ).rstrip("/")
    EXTERNAL_API_TIMEOUT = float(os.getenv("EXTERNAL_API_TIMEOUT", "10"))
