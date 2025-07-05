CREATE TABLE books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    price REAL,
    rating INTEGER,
    availability TEXT,
    category TEXT,
    description TEXT,
    image_url TEXT,
    book_url TEXT,
    page_number INTEGER,
    scraped_at TEXT
);