from utils.database_manager import DatabaseManager
from src.api.utils.cache import cache_with_default
from logging import getLogger, basicConfig, INFO
from pathlib import Path

FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
DB_PATH = Path(__file__).resolve().parents[3] / "instance" / "bookonthetable.db"
manager = DatabaseManager(str(DB_PATH))


logger = getLogger(__name__)
basicConfig(level=INFO, format=FORMAT)


@cache_with_default
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
        return logs
    except Exception as e:
        logger.error(f"Error retrieving logs: {e}")
        return []


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
