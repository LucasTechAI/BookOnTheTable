from utils.database_manager import DatabaseManager
from logging import getLogger, basicConfig, INFO
from src.api.utils.cache import cache_with_logs
from json import loads, dumps
from re import sub, IGNORECASE
from pathlib import Path
FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
DB_PATH = Path(__file__).resolve().parents[3] / "tmp" / "bookonthetable.db"
SENSITIVE_KEYS = {"access_token", "refresh_token", "username", "password"}

manager = DatabaseManager(str(DB_PATH))
logger = getLogger(__name__)
basicConfig(level=INFO, format=FORMAT)

def mask_sensitive_data(request_body: str) -> str:
    try:
        data = loads(request_body)
        for key in SENSITIVE_KEYS:
            if key in data:
                data[key] = "***"
        return dumps(data, indent=2)
    except Exception:
        for key in SENSITIVE_KEYS:
            request_body = sub(
                rf'("{key}"\s*:\s*")[^"]*(")', rf'\1***\2', request_body, flags=IGNORECASE
            )
        return request_body

@cache_with_logs
def get_all_logs(limit: int = 100) -> list:
    """
    Get all logs from the database, limited to the specified number.
    Args:
        limit (int): The maximum number of logs to retrieve. Default is 100.
    Returns:
        list: A list of dictionaries, each representing a log entry.
    """
    try:
        logger.info(f"Retrieving the last {limit} logs from the database.")
        query = "SELECT * FROM logs ORDER BY timestamp DESC LIMIT ?"
        logs = manager.select(query, (limit,))
        logs = [dict(row) for row in logs]
        # Mask sensitive data in request_body
        for log in logs:
            if "request_body" in log:
                log["request_body"] = mask_sensitive_data(log["request_body"])
        return logs
    except Exception as e:
        logger.error(f"Error retrieving logs: {e}")
        return None


def delete_all_logs() -> str:
    """
    Delete all logs from the database.
    Returns:
        str: A message indicating the number of logs deleted or an error message if the operation fails
    """
    try:
        logger.info("Deleting all logs from the database.")
        query = "DELETE FROM logs"
        rowcount = manager.delete(query, ())
        logger.info(f"Deleted {rowcount} log entries.")
        return f"{rowcount} logs deleted successfully."
    except Exception as e:
        logger.error(f"Error deleting logs: {e}")
        return f"Error deleting logs: {str(e)}"
