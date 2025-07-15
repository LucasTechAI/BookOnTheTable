from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from pathlib import Path
from time import time, strftime, gmtime
from json import dumps
from typing import Optional
from utils.database_manager import DatabaseManager
from src.api.utils.jwt_handler import decode_token

DB_PATH = Path(__file__).resolve().parents[3] / "instance" / "bookonthetable.db"


class Logger:
    def __init__(self, db_path: Path):
        self.manager = DatabaseManager(str(db_path))

    def log(
        self,
        timestamp: str,
        method: str,
        endpoint: str,
        status_code: int,
        response_time_ms: float,
        user_agent: str,
        ip_address: str,
        username: Optional[str],
        query_params: str,
        request_body: str,
    ):
        self.manager.insert(
            """
            INSERT INTO logs (
                timestamp, method, endpoint, status_code, response_time_ms,
                user_agent, ip_address, username, query_params, request_body
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                timestamp,
                method,
                endpoint,
                status_code,
                response_time_ms,
                user_agent,
                ip_address,
                username,
                query_params,
                request_body[:500],
            ),
        )


class RequestSanitizer:
    AUTH_PATH_PREFIX = "/api/v1/auth"

    @staticmethod
    async def sanitize_request_body(request: Request) -> str:
        """
        Sanitiza o corpo da requisição para rotas sensíveis (ex: auth).
        Retorna "***REDACTED***" para rotas de auth, senão o corpo real.
        """
        if request.url.path.startswith(RequestSanitizer.AUTH_PATH_PREFIX):
            return "***REDACTED***"
        try:
            body = await request.body()
            return body.decode("utf-8")
        except Exception:
            return ""


class LoggingMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.logger = Logger(DB_PATH)

    async def dispatch(self, request: Request, call_next):
        start_time = time()

        response = await call_next(request)
        process_time = (time() - start_time) * 1000

        timestamp = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        method = request.method
        endpoint = request.url.path
        status_code = response.status_code
        user_agent = request.headers.get("user-agent", "unknown")
        ip_address = request.client.host if request.client else "unknown"

        body_str = await RequestSanitizer.sanitize_request_body(request)
        query_params = dict(request.query_params)
        query_str = dumps(query_params)

        username = None
        auth_header = request.headers.get("authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            try:
                payload = decode_token(token)
                username = payload.get("username")
            except Exception:
                pass

        self.logger.log(
            timestamp,
            method,
            endpoint,
            status_code,
            process_time,
            user_agent,
            ip_address,
            username,
            query_str,
            body_str,
        )

        return response
