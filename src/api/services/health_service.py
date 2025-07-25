from utils.database_manager import DatabaseManager
from logging import getLogger, basicConfig, INFO
from pathlib import Path
import os

FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
DB_PATH = os.path.join(os.path.dirname(__file__), "../../../tmp/bookonthetable.db")
DB_PATH = os.path.abspath(DB_PATH)
manager = DatabaseManager(str(DB_PATH))

logger = getLogger(__name__)
basicConfig(level=INFO, format=FORMAT)


def check_health() -> dict:
    """
    Check the health of the API and database connection.
    Returns:
        dict: A dictionary indicating the health status of the API and database.
    """
    try:
        manager.select("SELECT 1")
        return {"status": "ok", "message": "API is healthy and database is connected."}
    except Exception as e:
        return {"status": "error", "message": f"Database connection failed: {e}"}
