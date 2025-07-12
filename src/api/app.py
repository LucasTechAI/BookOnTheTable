from .routes import auth, books, categories, health, stats, home, logs
from src.api.middleware.logging_middleware import LoggingMiddleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from uvicorn import run

app = FastAPI(
    title="BookOnTheTable API",
    description="Public REST API for accessing book data scraped from books.toscrape.com",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(LoggingMiddleware)

app.include_router(home.router) 
app.include_router(auth.router)
app.include_router(books.router)
app.include_router(categories.router)
app.include_router(health.router)
app.include_router(stats.router)
app.include_router(logs.router)



if __name__ == "__main__":
    run("api.app:app", host="127.0.0.1", port=8001, reload=True)
