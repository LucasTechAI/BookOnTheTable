from dotenv import load_dotenv
from os import getenv

load_dotenv()

BASE_URL = "https://book-on-the-table.vercel.app/api/v1"
LOGIN_URL = f"{BASE_URL}/auth/login"
REGISTER_URL = f"{BASE_URL}/auth/register"
REFRESH_URL = f"{BASE_URL}/auth/refresh"
LOGS_URL = f"{BASE_URL}/logs/"

ADMIN_CREDENTIALS = {
    "username": getenv("ADMIN_USERNAME"),
    "password": getenv("ADMIN_PASSWORD")
}

APP_CONFIG = {
    "page_title": "BookOnTheTable - Dashboard",
    "page_icon": "📚",
    "layout": "wide"
}

REQUEST_TIMEOUT = 10
LOGS_TIMEOUT = 15

TOKEN_EXPIRY_MINUTES = 15

DEFAULT_LOG_LIMIT = 1000
AUTO_REFRESH_INTERVAL = 30

IMAGE_PATH = "/home/lucas/BookOnTheTable/src/dashboards/img/my.jpeg"
FALLBACK_IMAGE_URL = "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=200&h=200&fit=crop&crop=face&auto=format&q=80"